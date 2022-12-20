from django.shortcuts import render
from .models import Client,Message,Distribution,Contact
from .serializers import ClientSerializer,MessageSerializer,DistributionSerializer, ContactSerializer
from rest_framework.response import Response
from rest_framework import viewsets
class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

class DistributionViewSet(viewsets.ModelViewSet):
    serializer_class = DistributionSerializer
    queryset = Distribution.objects.all()
    def list(self, request, *args, **kwargs):
        total_distrs = Distribution.objects.all().count()
        distrs_lst_id = Distribution.objects.values('id')
        total = {
            'Total count distribtuions':total_distrs,
            'Total messages sent':'',
        }
        result = {}
        for distr in distrs_lst_id:
            res = {'Total messages': 0, 'Hold': 0, 'Out': 0}
            mail = Message.objects.filter(distribution_id=distr['id']).all()
            hold = len(mail.filter(sending_status='hold').all())
            out = len(mail.filter(sending_status='out').all())
            res['Total messages'] = len(mail)
            res['Hold'] = hold
            res['Out'] = out
            result[f"Distribution: {distr['id']}"] = res
        total['Total messages sent'] = result
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'Distributions':serializer.data,'Statistic':total})
        serializer = self.get_serializer(queryset, many=True)
        return Response({'Distributions':serializer.data,'Statistic':total})
    def retrieve(self, request,*args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        queryset = Message.objects.filter(distribution_id = kwargs['pk']).all()
        serializerMsg = MessageSerializer(queryset,many=True)
        return Response({'distribution':serializer.data,'message':serializerMsg.data})


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()

