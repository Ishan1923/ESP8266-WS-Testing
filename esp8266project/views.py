from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .models import sensordata
from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt
@api_view(['post'])
@authentication_classes([TokenAuthentication])

def recieve_sensor_data(request):
    if request.method == 'POST':
        data = request.data
        sensordata.objects.create(
            text = data['text']
        )
    return Response({'status':'success'})


def Home(request):
    latest_log = sensordata.objects.order_by('-timestamp').first()
    return render(request, 'layout.html', {'latest_log':latest_log})
