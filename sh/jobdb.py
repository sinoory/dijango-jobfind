# -*- coding:utf-8 -*-

from django.conf import settings
from django.utils import simplejson
import sys,os
sys.path.append("/home/sin/wkspace/webserver/django/mysite/")
sys.path.append("/home/sin/wkspace/soft/python/pub/utility/")
def ormsettingconfig():
    if settings.configured==True: #Lesson: django judge whether setting is configed
        return
    settings.configure( DATABASES = { #Lession : use ORM seprately,must config before import model
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'db_tst_dj',
            'USER': 'root',
            'PASSWORD': 'r',
            'HOST': '',
            'CHARSET':'utf-8',
        }
    }
    )

if __name__ == "__main__" :
    ormsettingconfig()

from jobfind.models import Job,JobL
from uty import models2json,testobj2dict,modelKeys


def mergeTable():
    j=Job()
    keys=modelKeys(j)
    keys.remove('id') #avoid insert error of duplicate primary key
    sqlkeys= "%s" %(",".join(keys))
    cmd="""mysql -uroot --password=r -D db_tst_dj -e "insert into jobfind_jobl("""+sqlkeys+""") select """+sqlkeys+"""  from jobfind_job" """
    print cmd
    os.system(cmd)
    cmd=""" mysql -uroot --password=r -D db_tst_dj -e " delete from jobfind_job " """
    os.system(cmd)

class JobDbOpr():
    def isJobExist(self,job):
        #querry whether the job exist in the local db jobl
        j=Job.objects.filter(jobu=job.jobu)
        jl=JobL.objects.filter(jobu=job.jobu)
        return len(j)>0 or len(jl)>0
    def add(self,job):
        if self.isJobExist(job):
            print ("Exist %s, ignore" %(job))
            return
        print("adding %s" % (job))
        job.save()

    def showAll(self):
        for j in Job.objects.all():
            print j

    def initjob(self,job,jburl,local,comp,compurl,jobdescribe,updata):
        j=Job()
        j.job=job
        j.jobu=jburl
        j.local=local
        j.coname=comp
        j.courl=compurl
        j.jd=jobdescribe
        j.updata=updata
        return j


def tstm():
    j=Job()
    print modelKeys(j)


def testJobDb():
    #configSetting()
    jobopr=JobDbOpr()
    #Add
    ed_user = jobopr.initjob('Android', 'http:job','sh', 'HTC','http:htc','write apk','20140101')
    jobopr.add(ed_user)
    jobopr.add(ed_user)
    #ed_user = jobopr.initjob('按着', 'http:job2','sh', '一零科技','http:htc','write apk','20140101')
    #jobopr.add(ed_user)
    #jobopr.add(ed_user)
    
    #print models2json(ed_user)
    print testobj2dict(ed_user)


if __name__ == "__main__" :
    tstm()



