from django.contrib import admin

from .models import AccountLevel1, AccountLevel2, AccountLevel3, Account

    
admin.site.register(AccountLevel1)
admin.site.register(AccountLevel2)
admin.site.register(AccountLevel3)
admin.site.register(Account)