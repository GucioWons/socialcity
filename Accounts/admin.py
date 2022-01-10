from django.contrib import admin

# Register your models here.
from Accounts.models import Account, Notification, Request, Action

admin.site.register(Account)
admin.site.register(Notification)
admin.site.register(Request)
admin.site.register(Action)

