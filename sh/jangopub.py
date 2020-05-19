# -*- coding:utf-8 -*-
#!/usr/bin/python
import sys

from django.conf import settings
def ormsettingconfig():
    if settings.configured==True: #Lesson: django judge whether setting is configed
        print "ormsettingconfig configured already!"
        return
    settings.configure( DATABASES = { #Lession : use ORM seprately,must config before import model
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'job51db',
            'USER': 'root',
            'PASSWORD': 'r',
            'HOST': '',
            'CHARSET':'utf-8',
        }
    }
    )
    print "ormsettingconfig configured!"


if __name__=='__main__':
    print "config ormsettingconfig"
    ormsettingconfig()

