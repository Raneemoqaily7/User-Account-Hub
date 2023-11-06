from django.contrib import admin

# Register your models here.
from UserAccountHub.models import Account,User

admin.site.register(Account)
admin.site.register (User)