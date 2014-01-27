from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader

def index(request):
    template = loader.get_template('polls/b.html')
    context = Context({
            'latest_poll_list': 'a',
                })
    return HttpResponse(template.render(context))

def detail(request, poll_id):
    return HttpResponse("You're looking at poll %s." % poll_id)

def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on poll %s." % poll_id)

