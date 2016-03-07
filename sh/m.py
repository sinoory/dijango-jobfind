# -*- coding:utf-8 -*-
#!/usr/bin/python
import sys,os,traceback
sys.path.append(os.path.join(os.path.dirname(__file__),"../pypub/utility"))
sys.path.append(os.path.join(os.path.dirname(__file__),"../pypub/web"))
from webLogin import LoginBroser
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
                print traceback.print_exc()
               
            if jobs==0 :
                print "Exit,No job in page "+url
                self.mFinishReason="REACH_END"
                break;            
            elif jobs==USER_STOPED or self.userStopped:
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
        pagesearchurl="http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea="+jobarea+"&district=000000&funtype=0000&industrytype=00&issuedate="+issuedate+"&providesalary=99&keyword="+keyword+"&keywordtype="+self.mQuerryDic.get('keywordtype')+"&curr_page="+str(pageindex)+"&lang=c&stype=2&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=01&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=0&confirmdate=9"
        #pagesearchurl="http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=020000%2C00&district=000000&funtype=0000&industrytype=00&issuedate=3&providesalary=99&keyword="+keyword+"&keywordtype="+self.mQuerryDic.get('keywordtype')+"&curr_page="+str(pageindex)+"&lang=c&stype=2&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=01&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=0&confirmdate=9"
        ck="guid=14559615973991260064; ps=us%3DATgGbFAwBS1SNQ5mAHtSZ1FiUX5VYVIzBjBWeFphUWUMMVc5A2gBMVc3WzEAZFdnU2hQYlFgV35QGlBxCHQOSAFT%26%7C%26nv_3%3D; adv=adsnew%3D0%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttp%253A%252F%252Fbzclk.baidu.com%252Fadrc.php%253Ft%253D0fKL00c00f7A79n0jn-w00uiAsjtPT9y00000r6zeHY00000TD0ttK.THYdnyGEm6K85yF9pywd0Znqmvn3uWFhrHcsnj04nyRkP0Kd5HNKwHbknH0srRPafb7Krjw7P1TYwHDLrjN7rRcYPHwD0ADqI1YhUyPGujYzPH6zrjfYPHc1FMKzUvwGujYkPBuEThbqniu1IyFEThbqFMKzpHYz0ARqpZwYTjCEQLwzmyP-QWRkphqBQhPEUiqYTh7Wui4spZ0Omyw1UMNV5HT3rHc1nzu9pM0qmR9inAPDULunnvf1uZbYnRdgTZuupHNJmWcsI-0zyM-BnW04yydAT7GcNMI-u1YqFh_qnARkPHcYPjFbrAFWrHRsuHR4PhFWPjmkryPhrHKhuhc0mLFW5HD1PHfz%2526tpl%253Dtpl_10085_12986_1%2526l%253D1038955240%2526ie%253DUTF-8%2526f%253D8%2526tn%253Dbaidu%2526wd%253D51job%26%7C%26adsnum%3D789233; guide=1; nolife=fromdomain%3D; search=jobarea%7E%60020000%7C%21ord_field%7E%600%7C%21list_type%7E%600%7C%21recentSearch0%7E%602%A1%FB%A1%FA020000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA3%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA01%A1%FB%A1%FA99%A1%FB%A1%FAlinux%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1456818574%A1%FB%A1%FA0%A1%FB%A1%FA%7C%21"

        lb=LoginBroser()
        #lb.nomalOpen("http://www.51job.com/");
        reader=HtmlReader(pagesearchurl,cookie=ck,retrycnt=5)
        #reader=HtmlReader(pagesearchurl,retrycnt=5,jsondata={})#use jsondata for post request
        reader.run()
        #BeautifulSoup will try to get encode from page  <meta  content="text/html; charset=gb2312">
        #here the data from HtmlReader is already utf8,not meta gb2312,so pass utf-8 to its construct to force encoding,
        #otherwise the BeautifulSoup can't work
        soup=BeautifulSoup(reader.outdata,fromEncoding="utf-8")
        print "process %s" %pagesearchurl
        #print soup.findAll("ul",{"class":"dict-basic-ul"})[0].li.strong.string 
        #find the table firest ,then find the job items
        #a itme looks like : checkbox jobname companyname locate udatedata
        #olTag=soup.findAll("table",{"class":"resultList resultListWide"})[0].findAll("tr",{"class":"tr0"})
        #olTag=soup.findAll("div",{"class":"resultListDiv"})[0].findAll("tr",{"class":"tr0"})
        olTag=soup.findAll("div",{"id":"resultList"})[0].findAll("div",{"class":"el"})
        cnt,jloop=0,1
        while jloop<len(olTag) :
            if self.userStopped :
                return USER_STOPED,pagesearchurl
            j=olTag[jloop]
            jloop+=1
            jobDetailPageUrl=j.findAll("p",{"class":"t1"})[0].findAll("a")[0].get("href")
            #needn't encode chinese to utf-8 with django db models
            jobname=j.findAll("p",{"class":"t1"})[0].findAll("a")[0].get("title") 
            #cols[1].get_text() #.encode('utf-8') #remove tags
            company=j.findAll("span",{"class":"t2"})[0].findAll("a")[0].get("title")
            companyUrl=j.findAll("span",{"class":"t2"})[0].findAll("a")[0].get("href")
            local=j.findAll("span",{"class":"t3"})[0].get_text() #.encode('utf-8')
            ud=j.findAll("span",{"class":"t5"})[0].get_text()
            self.mHtmlGetStrategy.mExtralInfo['jobDetailPageUrl']=jobDetailPageUrl
            self.mHtmlGetStrategy.mExtralInfo['companyUrl']=companyUrl
            if self.mHtmlGetStrategy.needIgnoreCompany(company):
                print "Ignore company %s,the same as last one" %company
                continue
            self.getDescript(self.mHtmlGetStrategy.getDescribeIntrestingUrl())
            jd=self.mHtmlGetStrategy.mExtralInfo['jobDescribe']
            cd=self.mHtmlGetStrategy.mExtralInfo['companyDesc']
            jbo.mExtraInfoDict=self.mHtmlGetStrategy.mExtralInfo
            #print "%s  %s\n %s \n %s " %(jobname,company,jd,cd)
            if not self.mHtmlGetStrategy.isDescValid():
                print "xxxxinvalid job descxxxxxx"
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

            cnt=cnt+1
        return cnt,pagesearchurl
        #jbo.showAll()

    def getDescript(self,joburl):
        self.mHtmlGetStrategy.load(joburl)
        outdata=self.mHtmlGetStrategy.data()
        #print outdata
        try:
            s=BeautifulSoup(outdata,fromEncoding='utf-8')
            if self.mHtmlGetStrategy.needJobCompDesc():
                jd=s.findAll("div",{"class":"bmsg job_msg inbox"})[0]
                sjd="%s" %jd
                sjd=sjd.replace("<br/>","\n")
                sjd=self.rmHtmlTag(sjd)

                cd=s.findAll("div",{"class":"tmsg inbox"})[0]
                scd="%s" %cd
                scd=self.rmHtmlTag(scd)


                #update=s.findAll("table")[6].findAll("tr")[0].findAll("td")[1]
                #update="%s" %update
                #update=self.rmHtmlTag(update)
                #self.mHtmlGetStrategy.mExtralInfo['update']=update

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
    qd={'filterkeys':'android','keywordtype':'100','serverActionType':55}
    jobadder.setQuerryDict(qd)
    jobadder.addJob("android","020000",'1',3,3)
    #jobadder.tst()
    #jobadder.getDescript('http://jobs.51job.com/shanghai-pdxq/72070349.html?s=0') #job url
    #jobadder.getDescript('http://search.51job.com/list/co,c,2245593,000000,10,1.html') #company url
    #jobadder.getDescript('http://search.51job.com/list/co,c,3289243,000000,10,1.html') #company url
    #getDescript('http://ac.51job.com/phpAD/adtrace.php?ID=15736875&JobID=56483257')
