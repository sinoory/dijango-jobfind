from django.db import models

class JobCompanyScore(models.Model):
    site=models.CharField(max_length=20)
    job=models.CharField(max_length=100)
    jobu=models.CharField(max_length=100)
    coname=models.CharField(max_length=100)
    courl=models.CharField(max_length=100)
    score=models.IntegerField(default=0)
    def __unicode__(self):
        return "CompanyScore<%s,%s,%s>" %(self.coname,self.score,self.courl)

class AJob(models.Model):
    site=models.CharField(max_length=20) #51job,zhlian,...
    job=models.CharField(max_length=100)
    jobu=models.CharField(max_length=100)
    salary=models.CharField(max_length=50)
    local=models.CharField(max_length=20)
    coname=models.CharField(max_length=100)
    courl=models.CharField(max_length=100)
    jd=models.TextField()
    cd=models.TextField()
    #cd=models.CharField(max_length=100) #company simple describle
    state=models.CharField(max_length=10) #null .get , filter ...
    udate=models.CharField(max_length=10)
    sendate=models.CharField(max_length=10)
    sendcnt=models.IntegerField(default=0)
    user=models.CharField(max_length=20)
    
    def __unicode__(self):
        #return "Job<%s,%s>" %(self.job.decode('utf-8'),self.coname.decode('utf-8'))
        #return "Job<%s,%s>" %(self.job.encode('utf-8'),self.coname.encode('utf-8'))
        return "Job<%s,%s>" %(self.job,self.coname)

    """
    **def __unicode__(self):**
            **return u'%s %s' % (self.first_name, self.last_name)**
    """

    #Lesson Model inherit : define abstract base class
    class Meta:
        abstract = True
# Create your models here.
class Job(AJob):

    """
    def __init__(self,job,jburl,local,comp,compurl,jobdescribe,updata):
        self.job=job
        self.jobu=jburl
        self.local=local
        self.coname=comp
        self.courl=compurl
        self.jd=jobdescribe
        self.updata=updata
        self.state="null"
    """


class JobL(AJob):
    'the local job db which processed already'
    pass

