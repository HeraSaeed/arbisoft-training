import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from reports.tasks import download_daily_report

os.environ.setdefault('DJNAGO_SETTING_MODULE', 'newproject.settings')

app = Celery('newproject')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'download_stock_data_every_weekday_at_5_30': {
        'task': 'newproject.reports.tasks.download_daily_report',  
        'schedule': crontab(hour=17, minute=30, day_of_week='1-5'),  # Every weekday (Mon-Fri) at 5:30 PM
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

    