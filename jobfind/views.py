from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from jobfind.models import Job
import sys
sys.path.append("/home/sin/wkspace/soft/python/pub/utility/")
from uty import models2json

def index(request):
    template = loader.get_template('jobfind/b.html')
    context = Context({
            'latest_poll_list': 'a',
                })
    return HttpResponse(template.render(context))

def detail(request, poll_id):
    j=Job.objects.get(id=int(poll_id))
    #print "detail(%s)" %(poll_id)
    if j!=None: 
        res= "%s" %models2json(j)
        
    return HttpResponse("%s" %res)

def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on poll %s." % poll_id)

