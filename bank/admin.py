from django.contrib import admin
from .models import account,history,vrf,email_token

# Register your models here.
@admin.register(account)
class show(admin.ModelAdmin):
    list_display = ['id','user','phone','addres','city','state','acn','amount','date_time']



@admin.register(history)
class histry(admin.ModelAdmin):
    list_display = ['id','user','acn','crid','dev','action','date_time']

@admin.register(vrf)
class vrif(admin.ModelAdmin):
    list_display = ['id','user','name','vf']


@admin.register(email_token)
class email_tokn(admin.ModelAdmin):
    list_display = ['id','user','name','forget_token','created_at']