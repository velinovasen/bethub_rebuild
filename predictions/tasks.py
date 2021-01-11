from celery import shared_task, Celery
from celery.schedules import crontab

from predictions.scrapers import get_games, check_results, bets_volume, prediction
from predictions.celery import app


@shared_task
def get_games_celery():
    games = get_games.UpcomingGames()
    games.scrape()


@shared_task
def get_volume_celery():
    bets_volume.scrape()


@shared_task
def get_results_celery():
    results = check_results.Results()
    results.scrape()


@shared_task
def get_predictions_celery():
    predictions_scraper = prediction.Predictions()
    predictions_scraper.scrape()

