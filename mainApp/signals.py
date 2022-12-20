from django.dispatch import receiver
from mainApp.models import Distribution,Client,Message,Contact
from django.db.models import Q
from django.db.models.signals import post_save
from .tasks import send_message
from .tasks import send_beat_email
@receiver(signal=post_save,sender = Distribution)
def message(sender,instance,created,**kwargs):
    if created:
        clients = Client.objects.filter(Q(tag = instance.tag) | Q(mobile_operator_code = instance.mobile_operator_code)).all()
        for client in clients:
            Message.objects.create(
                sending_status = "hold",
                client_id = client.id,
                distribution_id = instance.id
            )

            message = Message.objects.filter(distribution_id = instance.id,client_id = client.id).first()
            data = {
                "id":message.id,
                "phone":int(client.phone_number),
                "text":instance.text
                }
            if instance.allowed:
                send_message.apply_async((data,client.timezone,instance.time_start,instance.time_end),expires = instance.date_end)
            else:
                send_message.apply_async(
                    (data,client.timezone,instance.time_start,instance.time_end),
                    eta = instance.date_start,expires = instance.date_end)
