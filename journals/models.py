from django.db import models
from django.conf import settings
from acc_codes.models import Account, AccountLevel3
from acc_books.models import Book
    
class Transaction(models.Model):
    book = models.ForeignKey(
        Book,
        related_name ="transaction",
        on_delete=models.CASCADE
    )
    description = models.TextField()
    date = models.DateField()
    intra_date_ref = models.CharField(max_length=3, null=True, blank=True)
    #Meta
    recorder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def total_debits(self):
        return sum(entry.amount for entry in self.entries.filter(entry_type=1))
    
    def total_credits(self):
        return sum(entry.amount for entry in self.entries.filter(entry_type=2))
    
    def is_balanced(self):
        return self.total_debits == self.total_credits

    def ask_for_ref(self):
        return self.book_set.get_latest_ref
    
    def auto_ref(self):
        self.ref = self.ask_for_ref
    
    def get_absolute_url(self):
        return reverse("transaction_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f"{self.book_id}{self.id}"
    
    
class Entry(models.Model):
    ENTRY_TYPES = [
        (1, "Debit"),
        (2, "Credit"),
    ]
        
    transaction = models.ForeignKey(
        Transaction,
        related_name ="entries",
        on_delete=models.CASCADE
    )
    
    account = models.ForeignKey(
        Account,
        related_name ="entries",
        on_delete=models.CASCADE
    )
    entry_type = models.IntegerField(choices=ENTRY_TYPES)
    amount = models.DecimalField(max_digits=5, decimal_places=2)