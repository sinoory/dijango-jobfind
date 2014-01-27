# -*- coding:utf-8 -*-
#!/usr/bin/python
import sys
sys.path.append("/home/sin/wkspace/soft/python/pub/web/")
from getPage import HtmlReader
from bs4 import BeautifulSoup
from jobdb import Job,JobDbOpr




def test():
    jbo = JobDbOpr()
    reader=HtmlReader("http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=000000%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&keyword=android&keywordtype=2&curr_page=2&lang=c&stype=2&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=01&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14")
    reader.run()
    soup=BeautifulSoup(reader.outdata)
    #print soup.findAll("ul",{"class":"dict-basic-ul"})[0].li.strong.string 
    #find the table firest ,then find the job items
    #a itme looks like : checkbox jobname companyname locate updatedata
    olTag=soup.findAll("table",{"class":"resultList resultListWide"})[0].findAll("tr",{"class":"tr0"})
    for j in olTag :
        cols=j.findAll("td")
        jobDetailPageUrl=cols[1].findAll("a",{"class":"jobname"})[0].get('href')
        #needn't encode chinese to utf-8 with django db models
        jobname=cols[1].get_text() #.encode('utf-8') #remove tags
        company=cols[2].get_text() #.encode('utf-8')
        companyUrl=cols[2].findAll("a",{"class":"coname"})[0].get('href')
        local=cols[3].get_text() #.encode('utf-8')
        job=Job(job=jobname,jobu=jobDetailPageUrl,local=local,coname=company,courl=companyUrl,jd='jd',update='data')
        #job=Job(jobname,jobDetailPageUrl,local,company,companyUrl,'jd','data')
        jbo.add(job)

    jbo.showAll()

test()
