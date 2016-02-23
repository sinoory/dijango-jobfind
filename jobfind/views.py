from django.shortcuts import render
import os
# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from django.http import HttpResponseRedirect
from jobfind.models import Job,JobL,JobCompanyScore
from django.db.models import Q
import sys,traceback
sys.path.append(os.path.join(os.path.dirname(__file__),"../pypub/utility"))
from uty import *
sys.path.append(os.path.join(os.path.dirname(__file__),"../sh"))
from m import Job51Adder
from jobdb import mergeTable,getCompanyList

from django import forms
from django.utils import simplejson as json

JobDbView=Job #Lesson : varable can point to a class instead of object , like macro in c++
jobAdder=Job51Adder()

JobLocalDbView=JobL

def index(request):
    print "index in..."
    template = loader.get_template('jobfind/b.html')
    total=JobDbView.objects.count()
    if total>0:
        start=JobDbView.objects.all()[0].id
    else:
        start=0
    print("index start=%d total=%d" %(start,total))
    context = Context({
            'start_id': start,
            'total_rcd':total,
                })
    return HttpResponse(template.render(context))


def detail(request, poll_id):
    print "detail in..."
    try:
        j=JobDbView.objects.get(id=int(poll_id))
        if j!=None: 
            jdict=model2dict(j)
            jdict['jobsCnt']=JobDbView.objects.count()
            css="-1"
            cs=None
            try:
                cs=JobCompanyScore.objects.get(coname=j.coname)
            except Exception,ex:
                print "company score not scan yet!"
            if(cs!=None):
                css=cs.score
            jdict['compScore']=css
            res= "%s" %dict2json(jdict)
        return HttpResponse("%s" %res)
    except Exception,ex: 
        print Exception,':',ex
        print traceback.print_exc()
   

def modify(request,rcdid):
    print "modify(%s) in..." %rcdid
    try:
        j=Job.objects.get(id=int(rcdid))
        modifystatus=request.POST.get('status')
        print "modifystatus=%s" %(modifystatus)
        #print "detail(%d)" %(int(poll_id))
        if modifystatus != None and len(modifystatus)>0:#modify the id status
            j.state=modifystatus
            j.save()
        return HttpResponse(json.dumps({"code":0}))
    except Exception,ex: 
        print Exception,':',ex
        print traceback.print_exc()
        return HttpResponse(json.dumps({"code":1}))
    return HttpResponse(json.dumps({"code":1}))

class QuerryForm(forms.Form):
    searchkey = forms.CharField(required=True)
    locate = forms.CharField(required=True)
    publishday = forms.IntegerField()

def querry(request):
    print "querry in..."
    if not request.is_ajax(): 
        template = loader.get_template('jobfind/q.html')
        context = Context({
                'start_id': 0,
                'total_rcd':0,
                    })
        return HttpResponse(template.render(context))
    else: #ajax
        form = QuerryForm(request.POST)
        print "post data=%s" %(request.POST)
        keyword=request.POST.get('searchkey')
        if keyword=="STOP":
            jobAdder.userStopped=True
            return HttpResponse(json.dumps({"code":"STOP"}))
        if request.POST.get('extracmd')=="LIST_HIGH_COMPANY":
            lstr=getCompanyList(int(keyword))
            return HttpResponse(json.dumps({"code":"LIST_HIGH_COMPANY","res":lstr}))
        jobarea=request.POST.get('workarea')
        issuedate=request.POST.get('publishday') 
        jobAdder.setQuerryDict(request.POST)
        if form.is_valid():
            searchkey=request.POST.get('searchkey')
            print "searchkey=%s" %searchkey
            return HttpResponse(json.dumps({"code":0}))
        try:
            #raise Exception("test")
            jobAdder.addJob(keyword,jobarea,issuedate,1,-1)
            jobAdder.userStopped=False
        except Exception,ex: 
            print Exception,':',ex
            print traceback.print_exc()
        return HttpResponse(json.dumps({"code":jobAdder.mFinishReason}))
        

def submitstatus(request):
    try:
        mergeTable() 
        return HttpResponseRedirect("index")
    except Exception,ex:
        print Exception,':',ex
        print traceback.print_exc()
    #if request.is_ajax():
        
def dbg(msg):
    print msg
def viewljobs(request):
    try:
        vlj=ViewLocalJobs()
        if request.method == 'POST':
            return vlj.getPostResponse(request)
        dbg("viewljobs Get")
        return vlj.getGetResponst(request)
    except Exception,ex:
        print Exception,':',ex



class ViewLocalJobs():
    def getLocalList(self):
        locations=(JobLocalDbView.objects.values_list('local').distinct()) #lesson django orm:select on column and distinct
        utflocals=[]
        for l in locations:
            l=list(l)[0].encode('utf8')
            l=l[:l.find('-')]
            if l not in utflocals:
                utflocals.append(l)
        return utflocals      
    def getStatusList(self):
        jobstatus=JobLocalDbView.objects.values_list('state').distinct()
        utfstatus=[]
        for l in jobstatus:
            l=list(l)[0].encode('utf8')
            if l not in utfstatus:
                utfstatus.append(l)
        return utfstatus
   
    def getGetResponst(self,request):
        template = loader.get_template('jobfind/viewljobs.html')
        jobs=JobLocalDbView.objects.filter(Q(state='watch')|Q(state='get')).order_by("-id") #Lesson django,orm querry whith OR
        #jobs=JobL.objects.filter(state='watch')
        dbg("ViewLocalJobs getGetResponst jobs")
        context = Context({
                'jobstatus':self.getStatusList(),
                'joblocals':self.getLocalList(),
                'joblist': jobs,
                    })
        return HttpResponse(template.render(context))
    def getPostResponse(self,request):
        template = loader.get_template('jobfind/viewljobs_table.html')
        print request.POST
        if(request.POST.get('cmd')=="UPDATE_JOB"):
            return self.updateJob(request)
        local=request.POST.get('local')
        jobs=JobLocalDbView.objects.order_by("-id")
        if len(local)>0:
            jobs=jobs.filter(local__contains=local)  #Lesson django orm:querry with sql like :colum__xxx

        status=request.POST.get('status')
        if len(status)>0:
            jobs=jobs.filter(state__exact=status)

        context = Context({
                'jobstatus':self.getStatusList(),
                'joblocals':self.getLocalList(),
                'joblist': jobs,
                    })

        return HttpResponse(template.render(context))

    def updateJob(self,request):
        job=JobLocalDbView.objects.filter(Q(id=request.POST.get("id")))[0] #Lesson django,orm querry whith OR
        qd={'filterkeys':'linux','keywordtype':'100','serverActionType':55}
        jobAdder.setQuerryDict(qd)
        update=jobAdder.getUpdate(job.jobu)
        updateres="not_update"
        if update!=job.udate:
            job.udate=update
            job.save()
            updateres="updated"
        return HttpResponse(json.dumps({"res":updateres,"newDate":update}))
        #jobs=JobLocalDbView.objects.filter(Q(state='watch')|Q(state='get')) #Lesson django,orm querry whith OR
        #return HttpResponse(json.dumps({"code":"post local"}))
  









