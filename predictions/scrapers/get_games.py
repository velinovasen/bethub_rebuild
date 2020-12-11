import json
import os
import re
import sys
from datetime import timedelta, datetime, date
from json import JSONDecodeError
from time import sleep

import django
from django.core.wsgi import get_wsgi_application
from selenium.webdriver import ChromeOptions, Chrome
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


sys.path.append('C:\\Users\\Asen\\Desktop\\bethub_rebuild\\bethub_rebuild')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bethub.settings')
django.setup()
application = get_wsgi_application()

from predictions.models import Game


def get_tomorrow_date(token):
    datetime.today().strftime('%Y-%m-%d')
    tomorrow_date = (datetime.today() + timedelta(hours=24)).strftime('%Y-%m-%d')
    if token == 'link':
        return "".join(tomorrow_date.split('-'))
    return "-".join(tomorrow_date.split('-'))


class UpcomingGames:
    WEB_LINKS = {
        "today_oddsportal": 'https://www.oddsportal.com/matches/',
        "oddsportal": 'https://www.oddsportal.com/matches/soccer/' + get_tomorrow_date('link')
    }

    REGEX = {
        "score": r'([t][a][b][l][e]\-[s][c][o][r][e]\"\>|[i][n]\-[p][l][a][y][ ][o][d][d][s])',
        "home_away_scheduled": r'(\/\"\>([A-z0-9].+)[ ]\-|[d]\"\>([A-z0-9].+)\<\/[s][p][a])[ ]([A-z0-9].{1,40})\<\/[a]',
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
        the_bulk = []
        for game in games:
            # FIND THE TIME
            score = re.search(self.REGEX['score'], str(game))
            if not score:
                try:
                    # print(game)
                    both_teams = re.search(self.REGEX["home_away_scheduled"], str(game))
                    home_team = str(both_teams.group(2))
                    away_team = str(both_teams.group(4))
                    if '&amp;' in home_team:
                        home_team = home_team.replace('&amp;', 'n')
                    if '&amp;' in away_team:
                        away_team = away_team.replace('&amp;', 'n')
                    if 'Group' in away_team or 'III' in home_team or 'PFL' in home_team:
                        continue
                    else:
                        if link == 'oddsportal':
                            date_model = (date.today() + timedelta(hours=24)).strftime('%Y-%m-%d')
                        else:
                            date_model = date.today().strftime('%Y-%m-%d')
                        time = re.search(self.REGEX["time"], str(game)).group(1)

                        # print(date_model)
                        home_odd, draw_odd, away_odd = '', '', ''
                        try:
                            odds = re.findall(self.REGEX["odds"], str(game))
                            [home_odd, draw_odd, away_odd] = [odds[0][1], odds[2][1], odds[4][1]]

                        except IndexError:
                            continue

                        except ValueError:
                            print('Most likely, we got missing odds')

                        # print(date_model, time, home_team, away_team, home_odd, draw_odd, away_odd)

                        if Game.objects.filter(date=date_model, time=time, home_team=home_team, away_team=away_team):
                            # TO FINISH -> PROBABLY JUST UPDATE THE ODDS
                            game = Game.objects.get(date=date_model, time=time, home_team=home_team, away_team=away_team)
                            if game.home_odd != home_odd or game.draw_odd != draw_odd or game.away_odd != away_odd:
                                game.home_odd = home_odd
                                game.draw_odd = draw_odd
                                game.away_odd = away_odd
                                game.save(update_fields=['home_odd', 'draw_odd', 'away_odd'])
                                print('CHECKED OR UPDATED')
                            pass
                        else:
                            the_bulk.append(Game(date=date_model, time=time, home_team=home_team,
                                                 away_team=away_team, home_odd=home_odd,
                                                 draw_odd=draw_odd, away_odd=away_odd))

                except AttributeError:
                    continue
        try:
            if len(the_bulk) > 0:
                Game.objects.bulk_create(the_bulk)
                print('NEW GAMES')
            else:
                print('NO NEW GAMES')
        except Exception:
            print('PROBLEM WITH DB')
            print(the_bulk)


if __name__ == '__main__':
    tmr = UpcomingGames()
    tmr.scrape()
