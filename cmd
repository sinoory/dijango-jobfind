python manage.py runserver
python manage.py syncdb

#can use ip to access webserver
python manage.py runserver 0.0.0.0:8085


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
sudo apt-get install python-mysqldb
sudo apt-get install python-qt4
