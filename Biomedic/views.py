from django.shortcuts import render
from django.http import HttpResponse
import requests, uuid, json, xmltodict, numpy
import collections
from .traductor import traductor

# Create your views here.


def home(request):
   
    cadena=request.GET.get('dato')
    
    datos=traductor(request,cadena)
    print("SSSSSSSSS",datos)
    return render(request, 'biomedic/index.html', {'data':datos})



