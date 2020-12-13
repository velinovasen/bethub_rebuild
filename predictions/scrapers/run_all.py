import os
import sys

import django
from django.core.wsgi import get_wsgi_application

sys.path.append('C:\\Users\\Asen\\Desktop\\bethub_rebuild\\bethub_rebuild')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bethub.settings')
django.setup()
application = get_wsgi_application()


from predictions.scrapers import bets_volume, check_results, prediction, get_games


if __name__ == '__main__':
    bets_volume.scrape()

    predictions_scraper = prediction.Predictions()
    predictions_scraper.scrape()

    games = get_games.UpcomingGames()
    games.scrape()

    results = check_results.Results()
    results.scrape()