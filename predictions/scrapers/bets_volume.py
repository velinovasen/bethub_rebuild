import sys, os, django
from selenium.webdriver import ChromeOptions, Chrome
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import re
from django.core.wsgi import get_wsgi_application

sys.path.append('C:\\Users\\Asen\\Desktop\\bethub_rebuild\\bethub_rebuild')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bethub.settings')
django.setup()
application = get_wsgi_application()

from predictions.models import BetsVolume


def scrape():
    WEB_LINKS = {
        "football": "https://www.bahisanaliz14.com/avrupa-en-cok-oynanan-maclar/"
    }

    days_numbered = {
        "Pts": "Monday", "Sal": "Tuesday", "Çar": "Wednesday", "Per": "Thursday",
        "Cum": "Friday", "Cts": "Saturday", "Pzr": "Sunday"
    }

    # OPEN THE WEBSITE AND GET THE DATA
    options = ChromeOptions()
    options.headless = True  # -> FALSE IF YOU WANT TO SEE THE BROWSER BROWSING
    options.add_argument("--lang=en")
    driver = Chrome(options=options, executable_path=ChromeDriverManager().install())
    driver.get(WEB_LINKS["football"])
    sleep(4)
    html = driver.execute_script("return document.documentElement.outerHTML;")
    driver.close()

    # WORK WITH THE DATA AND GO THROUGH VOLUMES
    soup = BeautifulSoup(html, 'html.parser')
    matches = soup.find_all(class_=re.compile('IH2Satir'))

    the_bulk = []

    for game in matches:
        elements = list(game)

        # GET THE TIME
        time_tokens = str(elements[1])
        time_pattern = r'[ ](\d+[:]\d+)\<\/'
        day_pattern = r'\;\"\>(.{3})\,'
        time_raw = re.search(time_pattern, time_tokens)
        day_raw = re.search(day_pattern, time_tokens)
        time = time_raw.group(1)
        day = days_numbered[day_raw.group(1)]

        # GET THE TEAMS
        team_tokens = str(elements[2])
        teams_pattern = r'[o][n][g]\>(.+)\<\/[s][t][r]'
        teams = re.search(teams_pattern, team_tokens)
        home_team, away_team = teams.group(1).split(' - ')

        # GET THE BET POSITION
        position_token = str(elements[3])
        position_pattern = r'[s][p][a][n]\>[ ](\d{1})\<\/[d][i]'
        position = re.search(position_pattern, position_token)
        final_bet = position.group(1)
        if final_bet == '0':
            final_bet = 'X'

        # GET THE ODD
        odds_token = str(elements[4])
        odds_pattern = r'[a][n]\>(\d+\.\d+)\<\/'
        odds_raw = re.search(odds_pattern, odds_token)
        odds = round(float(odds_raw.group(1)), 2)

        # GET THE AMOUNT
        amount_token = str(elements[5])
        amount_pattern = r'[o][n][g]\>(.+)[ ][A-z]+'
        amount = re.search(amount_pattern, amount_token)
        total_amount = amount.group(1)

        the_bulk.append(BetsVolume(day=day, time=time, home_team=home_team,
                                   away_team=away_team, final_bet=final_bet,
                                   odds=odds, amount=total_amount))
    print(the_bulk)
    BetsVolume.objects.all().delete()
    BetsVolume.objects.bulk_create(the_bulk)


# if __name__ == '__main__':
#     scrape()