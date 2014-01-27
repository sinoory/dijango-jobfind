from django.db import models

# Create your models here.
class Job(models.Model):
    site=models.CharField(max_length=20)
    job=models.CharField(max_length=50)
    jobu=models.CharField(max_length=100)
    local=models.CharField(max_length=20)
    coname=models.CharField(max_length=100)
    courl=models.CharField(max_length=100)
    jd=models.CharField(max_length=500)
    state=models.CharField(max_length=10) #null .get , filter ...
    update=models.CharField(max_length=10)
    sendate=models.CharField(max_length=10)
    sendcnt=models.IntegerField(default=0)

        
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
    def __unicode__(self):
        #return "Job<%s,%s>" %(self.job.decode('utf-8'),self.coname.decode('utf-8'))
        #return "Job<%s,%s>" %(self.job.encode('utf-8'),self.coname.encode('utf-8'))
        return "Job<%s,%s>" %(self.job,self.coname)



