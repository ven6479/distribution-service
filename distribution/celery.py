import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE','distribution.settings')
app = Celery('distribution')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-stats-everyday':{
        'task':'mainApp.tasks.send_beat_email',
        'schedule':crontab(minute=0, hour=0),
    }
}