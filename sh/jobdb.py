# -*- coding:utf-8 -*-

from django.conf import settings
from django.utils import simplejson
import sys,os
sys.path.append("/home/sin/wkspace/webserver/django/mysite/")
sys.path.append("/home/sin/wkspace/soft/python/pub/utility/")

from jangopub import ormsettingconfig

if __name__ == "__main__" :
    ormsettingconfig()

from jobfind.models import Job,JobL,JobCompanyScore
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

class JobOpr():
    mExtraInfoDict={}
    def isJobExist(self,job):
        return False
    def isOutData(self,job):
        return False
    def add(self,job):
        pass
    def update(self,job):
        pass
    def setExtraInfo(self,key,value):
        self.mExtraInfoDict[key]=value
    def needRender(self): #whether need use qtwebkit to render page to get some js result
        return False

class JobCompScoreOpr(JobOpr):
    #local JobCompanyScore store in dicJobCompScr dict{coname,JobCompanyScore}
    def isJobExist(self,job):
        #querry whether the job exist in the local db jobl
        j=JobCompanyScore.objects.filter(coname=job.coname)
        return len(j)>0 
    
    def add(self,job):
        cc=JobCompanyScore(site=job.site,job=job.job,jobu=job.jobu,coname=job.coname,courl=job.courl,score=self.mExtraInfoDict['score'])
        print("adding %s" % (cc))
        cc.save()
    def isOutData(self,job):
        oldscore=JobCompanyScore.objects.filter(coname=job.coname)[0].score
        newscore=self.mExtraInfoDict['score']
        if(int(oldscore) != int(newscore)):
            print "oldscore[%s]!=newscore[%s],need update" %(oldscore,newscore)
            return True
        return False
        #j=JobCompanyScore.objects.filter(coname=job.coname).filter(score__lt=self.mExtraInfoDict['score'])
        
    def needRender(self):
        return True
    def update(self,job):
        print ("updating company %s" %(job.coname))
        JobCompanyScore.objects.filter(coname=job.coname).update(score=self.mExtraInfoDict['score'])

def getCompanyList(minScore):
        res=[]
        ccs=JobCompanyScore.objects.filter(score__gt=minScore).order_by("-score")
        for cc in ccs:
            res.append("%s:%s" %(cc.coname,cc.score))
        return res
         
class JobDbOpr(JobOpr):
    def isJobExist(self,job):
        #querry whether the job exist in the local db jobl
        j=Job.objects.filter(jobu=job.jobu)
        jl=JobL.objects.filter(jobu=job.jobu)
        
        tj=None
        if len(j)>0:
            tj=j[0]
        if len(jl)>0:
            tj=jl[0]
        if not tj is None:
            if tj.coname != job.coname or tj.job != job.job:
                return False
            else:
                return True
                """
                print "XXXXXXXXXXXXXXXXXXXXXXX"
                print "The same job url=%s,but with different coname or jobname" %job.jobu
                print "db job=%s" %tj
                print "net jb=%s" %job
                print "XXXXXXXXXXXXXXXXXXXXXXX"
                exit()
                """
        return False
        #return len(j)>0 or len(jl)>0
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


def tstCcList():
    res=getCompanyList(5000)
    for l in res:
        print l

def tstm():
    j=Job()
    j=JobCompanyScore()
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
    tstCcList()


