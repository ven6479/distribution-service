from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
import pytz
class Distribution(models.Model):
    class Meta:
        verbose_name = _('distribution')
        verbose_name_plural= _('distributions')

    date_start = models.DateTimeField(_('start date mail'))
    date_end = models.DateTimeField(_('end date mail'))
    time_start = models.TimeField(_('start time mail'))
    time_end = models.TimeField(_('end time mail'))
    text = models.CharField(_('message text'),max_length=255)
    tag = models.CharField(_('tag'),max_length=50,blank=True)
    mobile_operator_code = models.CharField(_('mobile operator code'),max_length=3,blank=True)

    @property
    def allowed(self):
        current_date = timezone.now()
        if self.date_start <= current_date <=self.date_end:
            return True
        return False
    def __str__(self):
        return f"id: {self.id} date start: {self.date_start}"
class Client(models.Model):
    class Meta:
        verbose_name = _('client')
        verbose_name_plural = _('clients')
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    phone_validator = RegexValidator(regex=r'^7\d{10}$',
                                     message="Phone number must be in the format 7XXXXXXXXXX (X - number from 0 to 9)")
    mobile_operator_code = models.CharField(_('Mobile operator code'), max_length=3,blank=True)
    phone_number = models.CharField(_('phone number'),validators=[phone_validator],unique=True,max_length=11)
    tag = models.CharField(_('tag'), max_length=50, blank=True)
    timezone = models.CharField(_('timezone'), max_length=50, choices=TIMEZONES, default='UTC')
    def save(self,*args,**kwargs):
        if self.mobile_operator_code:
            return super(Client, self).save(*args,**kwargs)
        self.mobile_operator_code = str(self.phone_number)[1:4]
        return super(Client, self).save()
    def __str__(self):
        return f"Client with phone number = {self.phone_number}"

class Message(models.Model):
    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
    class Status(models.TextChoices):
        HOLD = 'hold', _('hold')
        OUT = 'out', _('out')

    time_create = models.DateTimeField(_('time create'), auto_now_add=True)
    sending_status = models.CharField(_('sending status'), max_length=10, choices=Status.choices)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages')
    distribution = models.ForeignKey(Distribution,on_delete=models.CASCADE,related_name='messages')

    def __str__(self):
        return f'Message: {self.distribution} for {self.client}'

class Contact(models.Model):
    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    def __str__(self):
        return self.name





