from django.contrib import admin
from .models import Transaction, Entry

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
