from django.contrib import admin

# Register your models here.

from jobfind.models import Job,JobL
admin.site.register(Job)
admin.site.register(JobL)
