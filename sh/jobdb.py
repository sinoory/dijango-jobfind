# -*- coding:utf-8 -*-

from django.conf import settings
from django.utils import simplejson
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


import sys
sys.path.append("/home/sin/wkspace/webserver/django/mysite/")
from jobfind.models import Job

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
        j.job=job
        j.jobu=jburl
        j.local=local
        j.coname=comp
        j.courl=compurl
        j.jd=jobdescribe
        j.updata=updata
        return j

def models2json(m):
    return simplejson.JSONEncoder().encode(str(obj2dict(m)))

def obj2dict(obj):
    """ 
    summary:
        change object to dict
    """
    memberlist = [m for m in dir(obj)]
    _dict = {}
    exclude_attr=['objects','DoesNotExist','MultipleObjectsReturned','clean','delete','pk','save']
    for m in memberlist:
        if m not in exclude_attr and m.find("_") == -1 and not callable(m):
            print m
            _dict[m] = getattr(obj,m)

    return _dict


if __name__ == "__main__" :
    jobopr=JobDbOpr()
    #Add
    ed_user = jobopr.initjob('Android', 'http:job','sh', 'HTC','http:htc','write apk','20140101')
    jobopr.add(ed_user)
    jobopr.add(ed_user)
    ed_user = jobopr.initjob('按着', 'http:job2','sh', '一零科技','http:htc','write apk','20140101')
    #jobopr.add(ed_user)
    #jobopr.add(ed_user)
    
    print models2json(ed_user)








