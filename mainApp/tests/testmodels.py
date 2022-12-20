from django.utils.timezone import now
from rest_framework.test import APITestCase

from ..models import Distribution,Client, Message,Contact


class TestModel(APITestCase):

    def test_creates_distributions(self):
        distribution= Distribution.objects.create(date_start=now(), date_end=now(), text='Hey hey',
                                         time_start=now().time(), time_end=now().time(), tag='hey',
                                         )
        self.assertIsInstance(distribution, Distribution)
        self.assertEqual(distribution.text, 'Hey hey')

    def test_creates_clients(self):
        client = Client.objects.create(phone_number='71234567890', mobile_operator_code='111',
                                       tag='huhu', timezone='UTC')
        self.assertIsInstance(client, Client)
        self.assertEqual(client.phone_number, '71234567890')

    def test_creates_messages(self):
        message = Message.objects.create(sending_status='hold', mailing_id=1, client_id=1)
        self.assertIsInstance(message, Message)
        self.assertEqual(message.sending_status, 'hold')
    def test_created_contacts(self):
        self.test_creates_distributions()
        self.test_creates_clients()
        self.test_creates_messages()
        contact = Contact.objects.create(name = 'Daddy',email='justDaddy@gmail.com')
        self.assertIsInstance(contact,Contact)
        self.assertEqual(contact.email,'justDaddy@gmail.com')