from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer

# Create your views here.
@api_view(['GET'])
def health(request):
    return Response({'status': 'ok'})

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer