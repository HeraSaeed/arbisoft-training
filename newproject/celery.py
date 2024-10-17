from __future__ import absolute_import, unicode_literals
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newproject.settings')

django.setup()

from celery import Celery
from celery.schedules import crontab
from reports.tasks import download_daily_report

app = Celery('newproject')
app.conf.enable_utc = False

app.conf.update(timezone= 'Asia/Karachi')

app.config_from_object('django.conf:settings', namespace='CELERY')


# CELERY Beat Settings
app.conf.beat_schedule = {
    'download_stock_data_every_weekday_at_5_30': {
        'task': 'reports.tasks.download_daily_report',  
        'schedule': crontab(hour=9, minute=00, day_of_week='1-5'),  # Every weekday (Mon-Fri) at 5:30 PM
    },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

    