import os
import sys

import django
from django.core.wsgi import get_wsgi_application
from selenium.webdriver import ChromeOptions, Chrome
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import re
from datetime import datetime, timedelta, date

sys.path.append('C:\\Users\\Asen\\Desktop\\bethub_rebuild\\bethub_rebuild')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bethub.settings')
django.setup()
application = get_wsgi_application()

from predictions.models import Game


def get_yesterday_date(for_key=False):
    datetime.today().strftime('%Y-%m-%d')
    tomorrow_date = (datetime.today() - timedelta(hours=24)).strftime('%Y-%m-%d')
    if for_key:                                     # CHECK IF ITS FOR KEY IN THE JSON OR NOT
        return "-".join(tomorrow_date.split('-'))
    else:
        return "".join(tomorrow_date.split('-'))


class Results:
    WEB_LINKS = {
        "today": 'https://www.oddsportal.com/matches/',
        "yesterday": 'https://www.oddsportal.com/matches/soccer/' + get_yesterday_date(),
    }

    REGEX = {
        "score": r'[t][a][b][l][e]\-[s][c][o][r][e]\"\>(\d{1,2}\:\d{1,2})\<\/',
        "both_teams_draw": r'\/\"\>([A-z0-9].{1,40})[ ]\-[ ]([A-z0-9].{1,40})\<\/[a]',
        "home_won": r'[s][p][a][n][ ][c][l][a][s][s]\=\"[b][o][l][d]\"\>([A-z0-9].{1,40})\<\/[s][p][a][n]',
        "home_loosing": r'\/\"\>([A-z0-9].{1,40})[ ]\-[ ]',
        "away_winning": r'[c][l][a][s][s]\=\"[b][o][l][d]\"\>([A-z0-9].{1,40})\<\/[s][p]',
        "away_loosing": r'\<\/[s][p][a][n]\>[ ]\-[ ]([A-z0-9].{1,40})\<\/[a]',
        "time": r'[0]\"\>(\d{1,2}[:]\d{1,2})\<\/[t][d]',
        "odds": r'(\"\>|\=\")(\d{1,2}[.]\d{1,2})(\<\/[a]|\"[ ])',
        "result": r'([c][o][r][e]\"\>(\d{1,2}[:]\d{1,2})([ ][p][e][n]|\<\/[t][d])|[p][o][s][t][p])'
    }

    def scrape(self):
        for link in self.WEB_LINKS.keys():
            # OPEN THE BROWSER
            driver = self.open_the_browser(link)

            # GET THE DATA
            all_games = self.get_the_data(driver)

            # CLEAN DATA
            self.clean_data(all_games, link)

    def open_the_browser(self, link):
        # OPEN THE BROWSER
        options = ChromeOptions()
        options.headless = True  # IF YOU WANT TO SEE THE BROWSER -> FALSE
        driver = Chrome(options=options, executable_path=ChromeDriverManager().install())
        driver.get(self.WEB_LINKS[link])
        sleep(4)
        return driver

    def get_the_data(self, driver):
        # GET THE DATA
        html = driver.execute_script('return document.documentElement.outerHTML;')
        soup = BeautifulSoup(html, 'html.parser')
        driver.close()
        games = soup.find_all('tr')
        return games

    def clean_data(self, games, link):
        # CLEAN THE DATA
        for game in games:
            # print(game)
            score = re.search(self.REGEX['score'], str(game))
            try:
                if score:
                    score = score.group(1)
                    [home_score, away_score] = score.split(':')
                    home_team, away_team = '', ''
                    time = re.search(self.REGEX['time'], str(game)).group(1)
                    if link == 'today':
                        date_model = date.today().strftime('%Y-%m-%d')
                    else:
                        date_model = (date.today() - timedelta(hours=24)).strftime('%Y-%m-%d')

                    if home_score > away_score:
                        home_team = re.search(self.REGEX['home_won'], str(game)).group(1)
                        away_team = re.search(self.REGEX['away_loosing'], str(game)).group(1)
                        #print(f'{home_team} {score} {away_team}')
                    elif home_score == away_score:
                        tokens = re.search(self.REGEX['both_teams_draw'], str(game))
                        home_team, away_team = tokens.group(1), tokens.group(2)
                        #print(f'{home_team} {score} {away_team}')
                    else:
                        home_team = re.search(self.REGEX['home_loosing'], str(game)).group(1)
                        away_team = re.search(self.REGEX['away_winning'], str(game)).group(1)
                        #print(f'{home_team} {score} {away_team}')

                    if Game.objects.get(date=date_model, time=time, home_team=home_team, away_team=away_team):
                        game = Game.objects.get(date=date_model, time=time, home_team=home_team, away_team=away_team)
                        if game.winner == '-':          # UPDATE THE INFO IF ITS FINISHED AND NOT UPDATED
                            if int(home_score) > int(away_score):
                                game.winner = '1'
                            elif int(home_score) < int(away_score):
                                game.winner = '2'
                            else:
                                game.winner = 'X'
                            game.score = score
                            game.status = 'finished'
                            game.save(update_fields=['winner', 'score', 'status'])
                            #print('UPDATED')
                        else:
                            #print('still not finished')
                            pass

                        users_predictions = game.game_predicted.all()        # GET THE USER PREDICTIONS

                        for prediction in users_predictions:     # CHECK THE PREDICTIONS STATUS AND UPDATE
                            print(prediction.status, prediction.odd, prediction.home_team, prediction.away_team)
                            if prediction.status == 'pending':
                                if game.winner == prediction.sign:
                                    prediction.status = 'won'
                                else:
                                    prediction.status = 'lost'
                                prediction.score = score
                            prediction.save()

                        users_bets = game.bet_game.all()  # GET ALL BETS

                        for user_bet in users_bets:              # CHECK THE BETS STATUS AND UPDATE
                            print(user_bet.status)
                            if user_bet.status == 2:
                                if game.winner == user_bet.bet_sign:
                                    user_bet.status = 1
                                    user_bet.bet_user.cash += user_bet.bet_odd * user_bet.amount
                                else:
                                    user_bet.status = 0
                                user_bet.score = score
                            user_bet.save()

            except Exception as e:
                print(e)


# if __name__ == '__main__':
#     tmr = Results()
#     tmr.scrape()
