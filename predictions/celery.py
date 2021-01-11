import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bethub.settings')

app = Celery('bethub',)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'redis://localhost:6379/0'

app.conf.beat_schedule = {
    'check-results-every-2-min': {
        'task': 'predictions.tasks.get_results_celery',
        'schedule': crontab(minute='*/2')
    },
    'get-games-every-10-min': {
        'task': 'predictions.tasks.get_games_celery',
        'schedule': crontab(minute='*/10'),
    },
    'get-bets-volume-every-15-min': {
        'task': 'predictions.tasks.get_volume_celery',
        'schedule': crontab(minute='*/15'),
    },
    'get-predictions-every-3-min': {
        'task': 'predictions.tasks.get_predictions_celery',
        'schedule': crontab(minute='*/3'),
    }
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')