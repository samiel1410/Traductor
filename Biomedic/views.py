from django.shortcuts import render
from django.http import HttpResponse
from .combinacion_12 import traduccion
# Create your views here.


def home(request):

    return render(request, 'biomedic/index2.html',)



