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
        "score": r'[t][a][b][l][e]\-[s][c][o][r][e]\"\>(\d{1,2}\:\d{1,2}[ ][p][e][n]\.|\d{1,2}\:\d{1,2}|'
                 r'[p][o][s][t][p][.]|\d{1,2}\:\d{1,2}.+)\<\/[t][d]\>.{1,400}\<[t][d]',
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

    @staticmethod
    def check_for_winner(data_str):
        regex = r'[o][d]{2}[s]\-[n][o][w][r][p][ ][r][e][s][u][l][t]\-[o][k]|[o][d]{2}[s]\-[n][o][w][r][p]'
        result = re.findall(regex, str(data_str))
        winner = result.index('odds-nowrp result-ok')
        if winner == 0:
            return '1'
        elif winner == 1:
            return 'X'
        elif winner == 2:
            return '2'
        else:
            return 'pst'

    def clean_data(self, games, link):
        # CLEAN THE DATA
        for game in games:
            score = re.findall(self.REGEX['score'], str(game))
            try:
                if score:
                    # GATHER THE ODDS AND CHECK BY THE CLASS NAME WHICH TEAM IS THE WINNER
                    score = score[0][:20].split('<')[0]
                    home_score, away_score = '', ''
                    home_team, away_team = '', ''
                    if 'pen' in score or 'ET' in score:
                        home_score, away_score = score.split(' ')[0].split(':')
                        print(away_score.split('\xa0'))
                        away_score = away_score.split('\xa0')[0]
                    elif score == 'postp.':
                        score = 'postp.'
                    else:
                        home_score, away_score = score.split(':')
                    time = re.search(self.REGEX['time'], str(game)).group(1)
                    if link == 'today':
                        date_model = date.today().strftime('%Y-%m-%d')
                    else:
                        date_model = (date.today() - timedelta(hours=24)).strftime('%Y-%m-%d')
                    if score != 'postp.':
                        if 'ET' in score or 'pen' in score or int(home_score) == int(away_score):
                            tokens = re.search(self.REGEX['both_teams_draw'], str(game))
                            home_team, away_team = tokens.group(1), tokens.group(2)
                        elif int(home_score) > int(away_score):
                            home_team = re.search(self.REGEX['home_won'], str(game)).group(1)
                            away_team = re.search(self.REGEX['away_loosing'], str(game)).group(1)
                        else:
                            home_team = re.search(self.REGEX['home_loosing'], str(game)).group(1)
                            away_team = re.search(self.REGEX['away_winning'], str(game)).group(1)
                    # GET THE GAMES AND UPDATE THE STATUS AND SCORE

                    if Game.objects.get(date=date_model, time=time, home_team=home_team, away_team=away_team):
                        new_game = Game.objects.get(date=date_model, time=time, home_team=home_team, away_team=away_team)
                        if new_game.status == 'not played':          # UPDATE THE INFO IF ITS FINISHED AND NOT UPDATED
                            new_game.winner = self.check_for_winner(game)
                            new_game.score = score[:6]
                            new_game.status = 'finished'
                            new_game.save(update_fields=['winner', 'score', 'status'])

                        users_bets = new_game.bet_game.all()  # GET ALL BETS
                        for user_bet in users_bets:              # CHECK THE BETS STATUS AND UPDATE
                            total_cash = 0
                            print('VLIZAME')
                            if user_bet.status == 2:
                                if new_game.winner == user_bet.bet_sign:
                                    user_bet.status = 1
                                    curr_amount = float(user_bet.bet_user.cash)
                                    user_bet.bet_user.cash = curr_amount + float(user_bet.bet_odd * float(user_bet.bet_amount))
                                    total_cash = curr_amount + float(user_bet.bet_odd * float(user_bet.bet_amount))
                                elif new_game.winner == 'postp.':
                                    user_bet.status = 1
                                    curr_amount = float(user_bet.bet_user.cash)
                                    user_bet.bet_user.cash = curr_amount + float(1 * float(user_bet.bet_amount))
                                    total_cash = curr_amount + float(1 * float(user_bet.bet_amount))
                                else:
                                    user_bet.status = 0
                                    total_cash = float(user_bet.bet_odd * float(user_bet.bet_amount))
                                if total_cash < 500:
                                    user_bet.bet_user.percent_profit = f'{-(100 - total_cash / 500 * 100):.2f}'
                                else:
                                    user_bet.bet_user.percent_profit = f'{(total_cash / 500 * 100) - 100:.2f}'
                                user_bet.score = score[:6]
                            user_bet.save()
                            user_bet.bet_user.save()

            except Exception as e:
                pass
                # print(e)



if __name__ == '__main__':
    tmr = Results()
    tmr.scrape()



# CURRENTLY REMOVED

# users_predictions = new_game.game_predicted.all()        # GET THE USER PREDICTIONS
#
# for prediction in users_predictions:     # CHECK THE PREDICTIONS STATUS AND UPDATE
#    # print(prediction.status, prediction.odd, prediction.home_team, prediction.away_team)
#     if prediction.status == 'pending':
#         if game.winner == prediction.sign:
#             prediction.status = 'won'
#         elif game.winner == 'postp.':
#             prediction.status = 'won'
#             prediction.odd = 1.00
#         else:
#             prediction.status = 'lost'
#         prediction.score = score
#     prediction.save()
