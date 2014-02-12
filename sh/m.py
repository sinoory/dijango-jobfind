# -*- coding:utf-8 -*-
#!/usr/bin/python
import sys
sys.path.append("/home/sin/wkspace/soft/python/pub/web/")
from getPage import HtmlReader

from bs4 import BeautifulSoup
from jobdb import ormsettingconfig

if __name__=='__main__':
    print "config ormsettingconfig"
    ormsettingconfig()

from jobdb import Job,JobDbOpr
import re

class BadUrl():
    url=""
    reason=""


USER_STOPED=-1

class Job51Adder():
    unprocessedUrls=[]
    isRuning=False
    userStopped=False
    def addJob(self,keyword,jobarea,issuedate,startpage=1,endpage=50):
        loop=startpage
        isRuning=True
        while(loop<=endpage):
            jobs,url=self.addOnePageJob(keyword,jobarea,issuedate,loop)
            if jobs==0 :
                print "Exit,No job in page "+url
                break;            
            elif jobs==USER_STOPED:
                print "user stopped,exit addJob"
                break;
            loop+=1;

    def addOnePageJob(self,keyword,jobarea,issuedate,pageindex):
        jbo = JobDbOpr()
        pagesearchurl=("http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea="+jobarea+"&district=000000&funtype=0000&industrytype=00&issuedate="+issuedate+"&providesalary=99&keyword="+keyword+"&keywordtype=2&curr_page="+str(pageindex)+"&lang=c&stype=2&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=01&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14")
        reader=HtmlReader(pagesearchurl)
        reader.run()
        soup=BeautifulSoup(reader.outdata)
        #print soup.findAll("ul",{"class":"dict-basic-ul"})[0].li.strong.string 
        #find the table firest ,then find the job items
        #a itme looks like : checkbox jobname companyname locate udatedata
        olTag=soup.findAll("table",{"class":"resultList resultListWide"})[0].findAll("tr",{"class":"tr0"})
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
            jd,cd=self.getDescript(jobDetailPageUrl)
            if(len(jd)<5):
                continue
            job=Job(job=jobname,jobu=jobDetailPageUrl,local=local,coname=company,courl=companyUrl,jd=jd,cd=cd,udate=ud)
            jobstring="%s%s" %(jobname,jd.decode("utf-8")) #TODO why type(jd)=str but type(jobname)=u?
            if jobstring.upper().find(keyword.upper()) == -1:
                print "Ignore Job<%s,%s> not contain keyword %s" %(jobname,company,keyword)
                continue

            jbo.add(job)
            cnt+=1
        return cnt,pagesearchurl
        #jbo.showAll()

    def getDescript(self,joburl):
        r=HtmlReader(joburl)
        r.run()
        s=BeautifulSoup(r.outdata)
        try:
            jd=s.findAll("td",{"class":"txt_4 wordBreakNormal job_detail "})[0]
            sjd="%s" %jd
            sjd=self.rmHtmlTag(sjd)

            cd=s.findAll("table")[3].findAll("tr")[3]
            scd="%s" %cd
            scd=self.rmHtmlTag(scd)
        except Exception,ex:
            jobstoped=s.findAll("div",{"class":"qxjyxszw"})
            if len(jobstoped)>0:
                print jobstoped[0] #the job has expired
                self.unprocessedUrls.append(BadUrl(url=joburl,reason="Job expired"))
                return "",""
            if joburl.find("search.51job.com")==-1:
                print ("Can't get job description from %s" %(joburl))
                self.unprocessedUrls.append(BadUrl(url=joburl,reason="Can't get job description"))
                return "",""
            print "Exception in getDescript(%s)" %joburl
            raise Exception(ex)

        return sjd, scd

    def rmHtmlTag(self,html):
        html=html.replace("<br>","\n").replace("</br>","")
        html=html.replace("<div>","\n").replace("</div>","")
        html=html.replace("<p>","\n").replace("</p>","")
        html=re.sub(r'</?\w+[^>]*>','',html)
        return html


if __name__=="__main__":
    jobadder=Job51Adder()
    jobadder.addJob("webkit","020000",'3',1,2)
    #getDescript('http://search.51job.com/job/56889371,c.html')
    #getDescript('http://ac.51job.com/phpAD/adtrace.php?ID=15736875&JobID=56483257')
