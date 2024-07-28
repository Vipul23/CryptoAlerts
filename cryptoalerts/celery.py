# from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from celery.schedules import crontab

from datetime import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptoalerts.settings')

app = Celery('cryptoalerts')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'Alerter': {
        'task': 'Alerter',
        'schedule': timedelta(minutes=1),  # This schedules the task to run every minute
    },
}

app.conf.timezone = 'UTC'

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')