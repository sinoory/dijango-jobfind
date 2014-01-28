# -*- coding:utf-8 -*-

from django.conf import settings
from django.utils import simplejson
"""
settings.configure( DATABASES = {
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
"""

import sys
sys.path.append("/home/sin/wkspace/webserver/django/mysite/")
sys.path.append("/home/sin/wkspace/soft/python/pub/utility/")
from jobfind.models import Job
from uty import models2json

class JobDbOpr():
    def isJobExist(self,job):
        j=Job.objects.filter(jobu=job.jobu)
        return len(j)>0
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
        j.id=5
        j.job=job
        j.jobu=jburl
        j.local=local
        j.coname=comp
        j.courl=compurl
        j.jd=jobdescribe
        j.updata=updata
        return j


if __name__ == "__main__" :
    jobopr=JobDbOpr()
    #Add
    ed_user = jobopr.initjob('Android', 'http:job','sh', 'HTC','http:htc','write apk','20140101')
    jobopr.add(ed_user)
    jobopr.add(ed_user)
    ed_user = jobopr.initjob('按着', 'http:job2','sh', '一零科技','http:htc','write apk','20140101')
    #jobopr.add(ed_user)
    #jobopr.add(ed_user)
    
    print models2json(ed_user).encode('utf-8')







