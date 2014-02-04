from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
import sys,traceback

from django import forms
from django.utils import simplejson as json

def index(request):
    print "shoplist index in..." 
    try:
        template = loader.get_template('shoplist/51.html')
        context = Context({})
        return HttpResponse(template.render(context))
    except Exception,ex:
        print ex
    #return HttpResponse("shoplist in")
