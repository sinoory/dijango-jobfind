from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
import sys,traceback

from django import forms
from django.utils import simplejson as json

def index(request):
    print "shoplist index in..."
    return HttpResponse("shoplist in")
