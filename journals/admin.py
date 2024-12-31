from django.contrib import admin
from journals.models.main import Transaction, Entry
from journals.models.accounts import AccountLevel1, AccountLevel2, AccountLevel3, Account

class EntryInline(admin.StackedInline):
    model = Entry
    extra = 2

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                ['description','date']
            ),
        }),
    )
    
    inlines=[EntryInline]
    
admin.site.register(Account)
admin.site.register(AccountLevel1)
admin.site.register(AccountLevel2)
admin.site.register(AccountLevel3)