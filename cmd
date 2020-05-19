
#for first run to creat db
python manage.py syncdb

#main
python manage.py runserver

#can use ip to access webserver
python manage.py runserver 0.0.0.0:8085

view :
http://0.0.0.0:8085/jobfind/index

Using the URLconf defined in mysite.urls, Django tried these URL patterns, in this order:
^admin/
^jobfind/ ^index$ [name='index']
^jobfind/ ^querry$ [name='querry']
^jobfind/ ^(?P<poll_id>\d+)/$ [name='detail']
^jobfind/ ^modify/(?P<rcdid>\d+)/$
^jobfind/ ^submitstatus$
^jobfind/ ^viewljobs$
^jobfind/ ^accounts/login/$
^jobfind/ ^accounts/logout/$
^polls/
^shoplist/
^admin/



clear db:
see mysite/mysite/settings.py for mysql config

setup: django require version 1.6
sudo pip install django==1.6
sudo pip install south
pip install mechanize
sudo apt-get install python-mysqldb
sudo apt-get install python-qt4
sudo apt-get install mysql-server

fill sql root password in mysite/settings.py

QA:
当遇到数据库写入错误时：
perationalError: (1366, "Incorrect string value: '\\xC2\\xA0\\xC2\\xA0|\\xC2...' for column 'jd' at row 1")
1. sh/m.py  BeautifulSoup 的fromEncoding要正确，使m.py正常打印出中文)
2. 数据库使用utf8创建：
2.1: drop database
2.2: CREATE DATABASE datablasename DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
2.3 : python manage.py syncdb
