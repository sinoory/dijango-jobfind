from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from jobfind.models import Job
import sys
sys.path.append("/home/sin/wkspace/soft/python/pub/utility/")
from uty import models2json
sys.path.append("/home/sin/wkspace/webserver/django/mysite/sh")
from m import test

from django import forms
from django.utils import simplejson as json

def index(request):
    template = loader.get_template('jobfind/b.html')
    total=Job.objects.count()
    start=Job.objects.all()[0].id
    print("index start=%d total=%d" %(start,total))
    context = Context({
            'start_id': start,
            'total_rcd':total,
                })
    return HttpResponse(template.render(context))

def detail(request, poll_id):
    j=Job.objects.get(id=int(poll_id))
    #print "detail(%s)" %(poll_id)
    if j!=None: 
        res= "%s" %models2json(j)
        
    return HttpResponse("%s" %res)

class QuerryForm(forms.Form):
    searchkey = forms.CharField(required=True)
    locate = forms.CharField(required=True)
    publishday = forms.IntegerField()

def querry(request):
    if not request.is_ajax(): 
        template = loader.get_template('jobfind/q.html')
        total=Job.objects.count()
        start=Job.objects.all()[0].id
        context = Context({
                'start_id': start,
                'total_rcd':total,
                    })
        return HttpResponse(template.render(context))
    else: #ajax
        form = QuerryForm(request.POST)
        searchkey=request.POST.get('searchkey')
        print "post data=%s" %request.POST
        if form.is_valid():
            searchkey=request.POST.get('searchkey')
            print "searchkey=%s" %searchkey
            return HttpResponse(json.dumps({"code":1}))
        test()
        return HttpResponse(json.dumps({"code":0}))
        

