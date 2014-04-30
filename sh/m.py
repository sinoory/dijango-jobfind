# -*- coding:utf-8 -*-
#!/usr/bin/python
import sys
sys.path.append("/home/sin/wkspace/soft/python/pub/web/")
sys.path.append("/home/sin/wkspace/soft/python/pub/utility/")
from getPage import HtmlReader
from QtPage import Render,WebkitRender
from uty import *
import urllib

from bs4 import BeautifulSoup

#from jobdb import ormsettingconfig
from jangopub import ormsettingconfig


if __name__=='__main__':
    print "config ormsettingconfig"
    ormsettingconfig()

from jobdb import Job,JobDbOpr,JobCompScoreOpr
import re

class BadUrl():
    def __init__(self,url,reason,title=""):
        self.url=url
        self.reason=reason
        self.urltitle=title
    def toStr(self):
        return "BadUrl<%s , %s , %s>" %(self.url,self.reason,self.urltitle)

    def __unicode__(self):
        return "BadUrl<%s , %s>" %(self,url,self.reason)

USER_STOPED=-1
UNDEFINDED=-2

class JobStrategy():
    def isJobSuilt(self,jobstr,keysDict):
        for k in keysDict:
            if jobstr.find(k.upper()) != -1:
                return True
        return False

class HtmlGetStrategy():
    mExtralInfo={'jobDescribe':'','companyDesc':''}
    lastDescConame=[]
    def load(self,url):
        r=HtmlReader(url,timeout=120)
        r.run()
        self.outdata=r.outdata
    def data(self):
        return self.outdata

    def getDescribeIntrestingUrl(self):
        return self.mExtralInfo['jobDetailPageUrl']

    def needScore(self):
        return False

    def needJobCompDesc(self):
        return True

    def isDescValid(self):
        return len(self.mExtralInfo['jobDescribe'])>5

    def needIgnoreCompany(self,coname):
        return False


class RenderHtmlGetStrategy(HtmlGetStrategy):
    def load(self,url):
        wr=WebkitRender(url,60,5)
        wr.load()
        self.date="%s" %wr.data()
    def data(self):
        return self.date

    def getDescribeIntrestingUrl(self):
        return self.mExtralInfo['companyUrl']
    def needScore(self):
        return True
    def needJobCompDesc(self):
        return False

    def isDescValid(self):
        return self.mExtralInfo['score']>=0

    def needIgnoreCompany(self,nowconame):
        if not nowconame in self.lastDescConame :
            self.lastDescConame.append(nowconame)
            print "Current Total companys : %d" %(len(self.lastDescConame))
            return False
        return True

class StrategyFactory():
    def __init__(self,factype):
        if factype==1:
            self.htmlGetor=RenderHtmlGetStrategy()
            self.jobOpr=JobCompScoreOpr()
            print "StrategyFactory[RenderHtmlGetStrategy,JobCompScoreOpr]"
        else:
            self.htmlGetor=HtmlGetStrategy()
            self.jobOpr=JobDbOpr()
            print "StrategyFactory[HtmlGetStrategy,JobDbOpr]"

class Job51Adder():
    unprocessedUrls=[]
    isRuning=False
    userStopped=False
    mJobStrategy=JobStrategy()
    def init(self):
        self.unprocessedUrls=[]
        self.userStopped=False
        self.mHtmlGetStrategy.lastDescConame=[]
    def setQuerryDict(self,querryDict):
        self.mQuerryDic=querryDict
        print "setQuerryDict querryDict=%s" %querryDict
        self.mFilterKeys=querryDict.get("filterkeys").split(",")
        print "self.mFilterKeys type=%s l=%s" %(type(self.mFilterKeys),self.mFilterKeys)
        strategyFactory=StrategyFactory(int(self.mQuerryDic['serverActionType']))
        self.mJobOprStrategy=strategyFactory.jobOpr
        self.mHtmlGetStrategy=strategyFactory.htmlGetor

    def addJob(self,keyword,jobarea,issuedate,startpage=1,endpage=50):
        keyword=urllib.quote(keyword.encode('utf-8'))
        self.init()

        loop=startpage
        isRuning=True
        self.mFinishReason="FINISH_OK"
        st=getCurTime() #from uty.py
        while(loop<=endpage or endpage==-1):
            jobs=UNDEFINDED
            try:
                jobs,url=self.addOnePageJob(keyword,jobarea,issuedate,loop)
            except Exception,ex:
                err= "Exception ex=%s in addOnePageJob ,saved data in Error.txt" %(ex)
                print err
                saveFile("%s\n" %(err),"Error.txt",'a')
               
            if jobs==0 :
                print "Exit,No job in page "+url
                self.mFinishReason="REACH_END"
                break;            
            elif jobs==USER_STOPED:
                print "user stopped,exit addJob"
                self.mFinishReason="STOP"
                break;
            loop+=1;
        print "====StartPage=%s===Loop=%s=EndPage=%s=================" %(startpage,loop,endpage)
        print "============%s===>%s=======================================" %(st,getCurTime())
        for bu in self.unprocessedUrls:
            print bu.toStr()
    def addOnePageJob(self,keyword,jobarea,issuedate,pageindex):
        jbo = self.mJobOprStrategy #JobCompScoreOpr() #JobDbOpr()
        pagesearchurl=("http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea="+jobarea+"&district=000000&funtype=0000&industrytype=00&issuedate="+issuedate+"&providesalary=99&keyword="+keyword+"&keywordtype="+self.mQuerryDic.get('keywordtype')+"&curr_page="+str(pageindex)+"&lang=c&stype=2&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=01&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14")
        reader=HtmlReader(pagesearchurl,retrycnt=5)
        reader.run()
        soup=BeautifulSoup(reader.outdata)
        print "process %s" %pagesearchurl
        #print soup.findAll("ul",{"class":"dict-basic-ul"})[0].li.strong.string 
        #find the table firest ,then find the job items
        #a itme looks like : checkbox jobname companyname locate udatedata
        #olTag=soup.findAll("table",{"class":"resultList resultListWide"})[0].findAll("tr",{"class":"tr0"})
        olTag=soup.findAll("div",{"class":"resultListDiv"})[0].findAll("tr",{"class":"tr0"})
        cnt=0
        for j in olTag :
            if self.userStopped :
                return USER_STOPED,pagesearchurl
            cols=j.findAll("td")
            jobDetailPageUrl=cols[1].findAll("a",{"class":"jobname"})[0].get('href')
            #needn't encode chinese to utf-8 with django db models
            jobname=cols[1].get_text() #.encode('utf-8') #remove tags
            company=cols[2].get_text() #.encode('utf-8')
            companyUrl=cols[2].findAll("a",{"class":"coname"})[0].get('href')
            local=cols[3].get_text() #.encode('utf-8')
            ud=cols[4].get_text()
            self.mHtmlGetStrategy.mExtralInfo['jobDetailPageUrl']=jobDetailPageUrl
            self.mHtmlGetStrategy.mExtralInfo['companyUrl']=companyUrl
            if self.mHtmlGetStrategy.needIgnoreCompany(company):
                print "Ignore company %s,the same as last one" %company
                continue
            self.getDescript(self.mHtmlGetStrategy.getDescribeIntrestingUrl())
            jd=self.mHtmlGetStrategy.mExtralInfo['jobDescribe']
            cd=self.mHtmlGetStrategy.mExtralInfo['companyDesc']
            jbo.mExtraInfoDict=self.mHtmlGetStrategy.mExtralInfo
            if not self.mHtmlGetStrategy.isDescValid():
                continue
            job=Job(job=jobname,jobu=jobDetailPageUrl,local=local,coname=company,courl=companyUrl,jd=jd,cd=cd,udate=ud)
            if self.mHtmlGetStrategy.needJobCompDesc():
                jobstring="%s%s" %(jobname,jd.decode("utf-8")) #TODO why type(jd)=str but type(jobname)=u?
                if not self.mJobStrategy.isJobSuilt(jobstring.upper(),self.mFilterKeys):
                    print "Ignore Job<%s,%s> NOT contain keyword %s" %(jobname,company,self.mFilterKeys)
                    continue
            if not jbo.isJobExist(job):
                jbo.add(job)
            elif jbo.isOutData(job) :
                jbo.update(job)
            else:
                print ("Exist %s, ignore" %(job))

            cnt+=1
        return cnt,pagesearchurl
        #jbo.showAll()

    def getDescript(self,joburl):
        self.mHtmlGetStrategy.load(joburl)
        outdata=self.mHtmlGetStrategy.data()
        #print outdata
        try:
            s=BeautifulSoup(outdata)
            if self.mHtmlGetStrategy.needJobCompDesc():
                jd=s.findAll("td",{"class":"txt_4 wordBreakNormal job_detail "})[0]
                sjd="%s" %jd
                sjd=self.rmHtmlTag(sjd)

                cd=s.findAll("table")[3].findAll("tr")[3]
                scd="%s" %cd
                scd=self.rmHtmlTag(scd)

                update=s.findAll("table")[6].findAll("tr")[0].findAll("td")[1]
                update="%s" %update
                update=self.rmHtmlTag(update)
                self.mHtmlGetStrategy.mExtralInfo['update']=update

                self.mHtmlGetStrategy.mExtralInfo['jobDescribe']=sjd
                self.mHtmlGetStrategy.mExtralInfo['companyDesc']=scd 
            if self.mHtmlGetStrategy.needScore(): 
                self.mHtmlGetStrategy.mExtralInfo['score']=-1
                score=s.findAll('a',{"id":"company_url"})[0].get_text().strip()[4:][:-1]
                self.mHtmlGetStrategy.mExtralInfo['score']=score
                print "%s , %s" %(score,joburl)
        except Exception,ex:
            #print "%s" %outdata
            err= "Exception ex=%s in getDescript(%s),saved data in Error.txt" %(ex,joburl)
            print err
            saveFile("%s\n" %(err),"Error.txt",'a')
            #saveFile("%s" %(outdata),"Error.txt",'a')
            #exit() 
            #print traceback.print_exc()
            jobstoped=s.findAll("div",{"class":"qxjyxszw"})
            sjd=""
            scd=""
            if len(jobstoped)>0:
                print jobstoped[0] #the job has expired
                self.unprocessedUrls.append(BadUrl(url=joburl,reason="Job expired"))
            elif joburl.find("search.51job.com")==-1:
                print ("Can't get job description from %s" %(joburl))
                self.unprocessedUrls.append(BadUrl(url=joburl,reason="invalid job url,Can't get job description"))
            elif s and s.title:
                self.unprocessedUrls.append(BadUrl(url=joburl,reason="Unknown reason",title=s.title))
            else:
                self.unprocessedUrls.append(BadUrl(url=joburl,reason="Unknown reason"))
    def getUpdate(self,jobDetailUrl):
        self.getDescript(jobDetailUrl)
        return self.mHtmlGetStrategy.mExtralInfo['update']

    def rmHtmlTag(self,html):
        html=html.replace("<br>","\n").replace("</br>","")
        html=html.replace("<div>","\n").replace("</div>","")
        html=html.replace("<p>","\n").replace("</p>","")
        html=re.sub(r'</?\w+[^>]*>','',html)
        return html

    def tst(self):
        print "hello"


        
if __name__=="__main__":
    jobadder=Job51Adder()
    qd={'filterkeys':'linux','keywordtype':'100','serverActionType':55}
    jobadder.setQuerryDict(qd)
    #jobadder.addJob("linux","020000",'3',1,-1)
    #jobadder.tst()
    jobadder.getDescript('http://search.51job.com/job/51281684,c.html') #job url
    #jobadder.getDescript('http://search.51job.com/list/co,c,2245593,000000,10,1.html') #company url
    #jobadder.getDescript('http://search.51job.com/list/co,c,3289243,000000,10,1.html') #company url
    #getDescript('http://ac.51job.com/phpAD/adtrace.php?ID=15736875&JobID=56483257')
