# -*- coding:utf-8 -*-
#!/usr/bin/python
import sys
sys.path.append("/home/sin/wkspace/soft/python/pub/web/")
from getPage import HtmlReader

from bs4 import BeautifulSoup
from jobdb import ormsettingconfig

if __name__=='__main__':
    ormsettingconfig()

from jobdb import Job,JobDbOpr
import re


def addJob(keyword,jobarea,issuedate,startpage=1,endpage=50):
    loop=startpage
    while(loop<=endpage):
        jobs,url=addOnePageJob(keyword,jobarea,issuedate,loop)
        if jobs==0 :
            print "Exit,No job in page "+url
            break;            
        loop+=1;

def addOnePageJob(keyword,jobarea,issuedate,pageindex):
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
        cols=j.findAll("td")
        jobDetailPageUrl=cols[1].findAll("a",{"class":"jobname"})[0].get('href')
        #needn't encode chinese to utf-8 with django db models
        jobname=cols[1].get_text() #.encode('utf-8') #remove tags
        company=cols[2].get_text() #.encode('utf-8')
        companyUrl=cols[2].findAll("a",{"class":"coname"})[0].get('href')
        local=cols[3].get_text() #.encode('utf-8')
        ud=cols[4].get_text()
        jd,cd=getDescript(jobDetailPageUrl)
        if(len(jd)<5):
            continue
        job=Job(job=jobname,jobu=jobDetailPageUrl,local=local,coname=company,courl=companyUrl,jd=jd,cd=cd,udate=ud)
        jbo.add(job)
        cnt+=1
    return cnt,pagesearchurl
    #jbo.showAll()

def getDescript(joburl):
    r=HtmlReader(joburl)
    r.run()
    s=BeautifulSoup(r.outdata)
    try:
        jd=s.findAll("td",{"class":"txt_4 wordBreakNormal job_detail "})[0]
        sjd="%s" %jd
        sjd=rmHtmlTag(sjd)

        cd=s.findAll("table")[3].findAll("tr")[3]
        scd="%s" %cd
        scd=rmHtmlTag(scd)
    except Exception,ex:
        jobstoped=s.findAll("div",{"class":"qxjyxszw"})
        if len(jobstoped)>0:
            print jobstoped[0]
            return "",""
        print "Exception in getDescript(%s)" %joburl
        raise Exception(ex)

    return sjd, scd

def rmHtmlTag(html):
    html=html.replace("<br>","\n").replace("</br>","")
    html=re.sub(r'</?\w+[^>]*>','',html)
    return html


if __name__=="__main__":
    addJob("webkit","020000",'3',3,50)
    #getDescript('http://search.51job.com/job/56889371,c.html')
    #getDescript('http://ac.51job.com/phpAD/adtrace.php?ID=15736875&JobID=56483257')
