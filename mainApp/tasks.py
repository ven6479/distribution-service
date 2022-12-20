from distribution.celery import app
from django.core.mail import send_mail
import os
from dotenv import load_dotenv, find_dotenv
import requests
from celery.utils.log import get_task_logger
from django.db.models import Q
from .models import Contact,Message,Distribution,Client
import datetime
import pytz

load_dotenv(find_dotenv())
url = os.getenv('TOKEN')
token = os.getenv('URL')
logger = get_task_logger(__name__)
@app.task(
        bind = True,
        retry_backoff = 5,
        retry_jitter = True,
        retry_kwargs = {'max-retries':7},
        serializer = 'json')
def send_message(self,data,client_timezone,time_start,time_end):
        time_start = datetime.datetime.strptime(time_start, '%H:%M:%S').time()
        time_end = datetime.datetime.strptime(time_end, '%H:%M:%S').time()
        timezone = pytz.timezone(client_timezone)
        now = datetime.datetime.now(timezone).time()
        if time_start<=now<=time_end:
                header = {
                        'Authorization': f'Bearer {token}',
                        'Content-Type': 'application/json'
                }
                try:
                        requests.post(url=url + str(data['id']), headers=header, json=data)
                except requests.exceptions.RequestException as exc:
                        logger.error(f"Message {data['id']} is error")
                        raise self.retry(exc=exc)

                logger.info(f"Message {data['id']} is out")
                Message.objects.filter(pk = data['id']).update(sending_status = 'out')

        else:
                hours = 24-(now.hour-time_start.hour)
                logger.info(f'Current time not for sending\n'
                            f'restarting task after {60*60*hours}')
                raise self.retry(countdown=60*60*hours)

@app.task
def send_beat_email():
        current_date = datetime.datetime.now().date()
        distributions = Distribution.objects.all()
        total = {}
        for dist in distributions:
                if dist.date_start.date()==current_date:
                        messages = Message.objects.filter(Q(distribution_id=dist.id)
                                                         & Q(sending_status='out')).all()
                        if len(messages)>=1:
                                total[f'distribution - {dist.id}'] = f"{len(messages)} messages were sent"
        for contact in Contact.objects.all():
                send_mail(
                        f'Hey {contact.name} It is daily stats',
                        f'Stats for today: {total}',
                        f'mr.nekita798@gmail.com', #need to add your email for sending emails to others
                        [contact.email],
                        fail_silently=False
                )






