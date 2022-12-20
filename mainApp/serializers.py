from rest_framework import serializers
from .models import Distribution, Client, Message,Contact

class DistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        fields = "__all__"




class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'