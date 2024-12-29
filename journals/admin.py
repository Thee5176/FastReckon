from django.contrib import admin
from .models import JournalRecord

class JournalRecordAdmin(admin.ModelAdmin):    
    # Add search fields if needed
    search_fields = ['description', 'book_id', 'ref']

    # Specify the fields to be shown in the form
    fieldsets = (
        (None, {
            'fields': ('date', 'book_id', 'ref', 'description')
        }),
    )
    

admin.site.register(JournalRecord, JournalRecordAdmin)