from django.contrib import admin
from .models import Transaction, Entry

class EntryInline(admin.StackedInline):
    model = Entry
    extra = 2

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["intra_month_ref", "slug"]
    fieldsets = (
        (None, {
            "fields": (
                ["book","date","intra_month_ref","description","shop","slug","created_by"]
            ),
        }),
    )
    
    inlines=[EntryInline]
