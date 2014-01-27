#!/usr/bin/python  
#-*- coding: utf-8 -*-  
  
from django.conf import settings  
settings.configure(  
    DATABASES = {  
        'default': {  
            'ENGINE': 'django.db.backends.sqlite3',  
            'NAME': '/tmp/mydb.db3',  
            'USER': '',  
            'PASSWORD': '',  
            'HOST': '',  
            'PORT': '',  
        }  
    }  
)  
  
from django.db import models  
class MyModel(models.Model):  
    name = models.CharField(max_length = 50)  
    gender = models.BooleanField(default = False)  
    age = models.IntegerField(default = 0)  
      
    def __unicode__(self):  
        return self.name  
  
myModel = MyModel()  
myModel.name = 'Jim Green'  
myModel.gender = True  
myModel.age = 18  
myModel.save();  
