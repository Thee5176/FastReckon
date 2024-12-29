from django.contrib.auth import get_user_model
from django.db import models

class CodeOfAccount(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=50)
    class Meta:
        ordering = ['code']

class MetaRecord(models.Model):
    recorder = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_date = models.DateField(auto_now=False, auto_now_add=True)
    last_updated = models.DateField(auto_now=True, auto_now_add=False)
    
    class Meta:
        abstract = True
    
class JournalRecord(MetaRecord, models.Model):
    JOURNAL_ENTRY_TYPES = [
        (1,'Debit'),
        (2,'Credit'),
    ]
    book_id = models.CharField(max_length=2)
    date = models.DateField(auto_now=False, auto_now_add=False)
    ref = models.IntegerField()
    description = models.CharField(max_length=255)
    # TODO: entry type https://www.geeksforgeeks.org/journal-entries/ , https://www.accountancyknowledge.com/books-of-accounts/    
    entry_type = models.IntegerField(choices=JOURNAL_ENTRY_TYPES)
    Dr_account = models.CharField(max_length=50)
    Dr_amount = models.DecimalField(max_digits=5, decimal_places=2)
    Cr_account = models.CharField(max_length=50)
    Cr_amount = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        ordering = ['book_id','date','ref']
        
    def __str__(self):
        return "{self.date}|{self.book_id}{self.ref}"
    
    def get_absolute_url(self):
        return reverse("journal_detail", kwargs={"pk": self.pk})
    