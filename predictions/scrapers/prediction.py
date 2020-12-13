import sys, os, django
from selenium.webdriver import ChromeOptions, Chrome, ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import bs4
from time import sleep
import re
from django.core.wsgi import get_wsgi_application

sys.path.append('C:\\Users\\Asen\\Desktop\\bethub_rebuild\\bethub_rebuild')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bethub.settings')
django.setup()
application = get_wsgi_application()

from predictions.models import Prediction


class Predictions:
    WEB_LINKS = {
        'football_today': 'https://m.forebet.com/en/football-tips-and-predictions-for-today',
        'football_tomorrow': 'https://m.forebet.com/en/football-tips-and-predictions-for-tomorrow'
    }

    REGEX = {
        "both_teams": r'[t]\=\"(.{1,60})[ ][v][s][ ](.{1,60})\"[ ]',
        "date_and_time": r'\"\>(\d{1,2}\/\d{1,2}\/\d{4})[ ](\d{1,2}\:\d{1,2})\<\/',
        "probabilities": r'\>(\d{1,2})\<\/([t]|[b])',
        "prediction": r'[r]\"\>([A-z0-9])\<\/',
        "score_prediction": r'\"\>(\d{1,2}[ ]\-[ ]\d{1,2})\<\/',
        "average_goals": r'[y]\"\>(\d{1,3}\.\d{1,2})\<\/',
        "temperature": r'[s]\"\>(\d{1,2}.{1})\<\/',
        "odds_for_prediction": r'\;\"\>(\d{1,2}\.\d{1,2})\<\/',
        "all_odds": r'[n]\>(\d{1,3}\.\d{1,2})\<\/',
    }

    def scrape(self):

        # OPEN THE BROWSERS
        driver, driver_tomorrow = self.open_the_browsers()

        # PRESS [MORE] BUTTON ON THE BOTTOM UNTIL DISAPPEAR
        self.click_on_buttons(driver, driver_tomorrow)

        # GET ALL GAMES
        all_games = self.get_all_games(driver, driver_tomorrow)

        # CLEAN DATA
        self.clean_data(all_games)

    def open_the_browsers(self):
        # OPEN THE WEBSITE AND WORK WITH IT
        options = ChromeOptions()
        options.headless = True  # IF YOU WANT TO SEE THE BROWSER -> FALSE
        driver = Chrome(options=options, executable_path=ChromeDriverManager().install())
        driver_tomorrow = Chrome(options=options, executable_path=ChromeDriverManager().install())
        driver.get(self.WEB_LINKS['football_today'])
        driver_tomorrow.get(self.WEB_LINKS['football_tomorrow'])
        sleep(3)
        return driver, driver_tomorrow

    def clean_data(self, all_games):
        # SEARCH THE DATA WE NEED
        the_bulk = []
        for game in all_games:
            [home_team, away_team, date, time, home_prob, draw_prob, away_prob,
             pred_sign, score_pred, av_goals, temp, odds_for_pred,
             home_odd, draw_odd, away_odd] = ['', '', '', '', '', '', '',
                                              '', '', '', '', '', '', '', '']

            # FIND THE TEAMS
            both_teams = re.search(self.REGEX["both_teams"], str(game))
            try:
                home_team = both_teams.group(1)
                if '&amp;' in home_team or '&' in home_team:
                    home_team = home_team.replace('&amp;', 'and')
                away_team = both_teams.group(2)
                if '&amp;' in away_team or '&' in away_team:
                    away_team = away_team.replace('&amp;', '&')
                # print(f"{items['home_team']} - {items['away_team']}")
            except AttributeError:
                continue

            # FIND THE TIME
            date_and_time = re.search(self.REGEX["date_and_time"], str(game))

            date_t = date_and_time.group(1).split('/')[::-1]
            date = f"{'-'.join(date_t)}"
            time = date_and_time.group(2)

            # PROBABILITIES
            probabilities = re.findall(self.REGEX["probabilities"], str(game))
            try:
                home_prob, draw_prob, away_prob = probabilities[0][0], probabilities[1][0], probabilities[2][0]
            except IndexError:
                print(probabilities)
                continue
            # PREDICTION SIGN
            pred_sign = re.search(self.REGEX["prediction"], str(game)).group(1)

            # SCORE PREDICTION
            try:
                score_pred = re.search(self.REGEX["score_prediction"], str(game)).group(1)
            except AttributeError:
                continue

            # FIND AVERAGE GOALS PER GAME
            av_goals = re.search(self.REGEX["average_goals"], str(game)).group(1)

            # GET THE WEATHER TEMPERATURE
            try:
                temp = re.search(self.REGEX["temperature"], str(game)).group(1)
            except AttributeError:
                temp = '-'

            # GET THE ODDS
            try:
                odds_for_pred = re.search(self.REGEX["odds_for_prediction"], str(game)).group(1)
                all_odds_token = re.findall(self.REGEX["all_odds"], str(game))
                # IF YOU WANT TO TAKE THE LIVE ODDS (IF LIVE) -> THEY ARE AVAILABLE IN THE FULL all_odds_token
                home_odd, draw_odd, away_odd = all_odds_token[:3]
            except AttributeError:
                odds_for_pred = '1.00'
                home_odd, draw_odd, away_odd = ['1.00', '1.00', '1.00']
            except ValueError:
                continue

            the_bulk.append(Prediction(date=date, time=time, home_team=home_team,
                                       away_team=away_team, home_prob=home_prob,
                                       draw_prob=draw_prob, away_prob=away_prob,
                                       bet_sign=pred_sign, score_predict=score_pred,
                                       avg_goals=av_goals, odds_for_prediction=odds_for_pred,
                                       home_odd=home_odd, draw_odd=draw_odd,
                                       away_odd=away_odd, temp=temp))

        print(the_bulk)
        Prediction.objects.all().delete()
        Prediction.objects.bulk_create(the_bulk)

    @staticmethod
    def click_on_buttons(driver, driver_tomorrow):
        while True:
            try:
                sleep(3)
                driver.find_element_by_css_selector('#close-cc-bar').click()
                today_token = driver.find_element_by_css_selector('#mrows > td > span')
                ActionChains(driver).move_to_element(today_token).click(today_token).perform()

                driver_tomorrow.find_element_by_css_selector('#close-cc-bar').click()
                tomorrow_token = driver_tomorrow.find_element_by_css_selector('#mrows > td > span')
                ActionChains(driver_tomorrow).move_to_element(tomorrow_token).click(tomorrow_token).perform()
            except Exception:
                sleep(3)
                break

    @staticmethod
    def get_all_games(driver, driver_tomorrow):
        # GET THE DATA
        html_today = driver.execute_script('return document.documentElement.outerHTML;')
        html_tomorrow = driver_tomorrow.execute_script('return document.documentElement.outerHTML;')

        # CLOSE THE BROWSERS
        driver_tomorrow.close()
        driver.close()

        # WORK WITH THE DATA
        today_soup = bs4.BeautifulSoup(html_today, 'html.parser')
        tomorrow_soup = bs4.BeautifulSoup(html_tomorrow, 'html.parser')
        matches_one_today = today_soup.find_all(class_='tr_0')
        matches_two_today = today_soup.find_all(class_='tr_1')
        matches_one_tomorrow = tomorrow_soup.find_all(class_='tr_0')
        matches_two_tomorrow = tomorrow_soup.find_all(class_='tr_1')
        all_games = []
        all_games += [list(game) for game in matches_one_today] + [list(game) for game in matches_two_today]
        all_games += [list(game) for game in matches_one_tomorrow] + [list(game) for game in matches_two_tomorrow]
        return all_games


# if __name__ == '__main__':
#     scraper = Predictions()
#     scraper.scrape()
