from django.contrib import admin

# Register your models here.

from SmartInvestApp.models import *

# Register your models here.

admin.site.register(Transaction)
admin.site.register(Message)
admin.site.register(Contrat)
admin.site.register(Notification)

admin.site.register(Information)


