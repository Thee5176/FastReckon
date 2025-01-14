from django.conf import settings
from django.db import models
from django.db.models import Max
from django.urls import reverse
from django.utils.text import slugify

from acc_books.models import Book
from acc_codes.models import Account, AccountLevel3

    
class Transaction(models.Model):
    SHOPNAME = {
        1:"まいばすけっと",
        2:"OK",
    }
    
    book = models.ForeignKey(
        Book,
        related_name ="transactions",
        on_delete=models.CASCADE
    )
    date = models.DateField()
    intra_month_ref = models.IntegerField(blank=True)
    description = models.TextField() #TODO : Auto Generate
    slug = models.SlugField(unique=True, max_length=9)
    has_receipt = models.BooleanField(default=False)
    shop = models.IntegerField(choices=SHOPNAME, null=True, blank=True)
    #Meta
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name=("transactions"), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = ("Transaction")
        verbose_name_plural = ("Transactions")
        ordering = ["date","intra_month_ref"]
        constraints = [
            models.UniqueConstraint(fields=['date','intra_month_ref'], name='unique_intra_month_ref')
        ]
    
    def auto_narration(self):
        pass
        # self.description = f"Being {dr_account} {action_kw} by {cr_account}."
        #dr/cr_account might be in list
        #action_kw is determine by combination of account
        
    def total_debits(self):
        entries = self.entries.all()
        return sum(entry.amount for entry in entries if entry.entry_type == 1)
    
    def total_credits(self):
        entries = self.entries.all()
        return sum(entry.amount for entry in entries if entry.entry_type == 2)

    def is_balance(self):
        """Check if all associated 'entries' are Dr/Cr balanced."""
        return self.total_debits() == self.total_credits()
        
    def total_amount(self):
        total = 0
        for entry in self.entries.all():          
            total += entry.amount
        return total/2
            
    def update_slug(self):
        """
        update slug by concatenate created(year/month) with intra_month_ref(integer)
        """    
        book = self.book.abbr
        formatted_date = self.date.strftime("%y%m")
        ref = self.intra_month_ref
        latest_slug = slugify(f"{book}{formatted_date}-{ref}")
        if self.slug != latest_slug :
            self.slug = latest_slug
            
    def new_month_ref(self):
        """
        Automatically add intra_month_ref and slug
        """
        if not self.intra_month_ref:
            # Filter ref for designated month
            this_month = self.date.strftime("%m")
            # Get latest transaction's ref for the same month
            latest_ref = Transaction.objects.filter(date__month=this_month).aggregate(max_ref=Max('intra_month_ref'))
            if latest_ref['max_ref']:
                self.intra_month_ref = latest_ref['max_ref'] + 1
            else:
                self.intra_month_ref = 1

    def save(self, *args, **kwargs):
        self.new_month_ref()
        self.update_slug()
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("transaction_detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return f"{self.book.abbr}|{self.description}"
    
    
class Entry(models.Model):
    ENTRY_TYPES = [
        (1, "Dr"),
        (2, "Cr"),
    ]
        
    transaction = models.ForeignKey(
        Transaction,
        related_name ="entries",
        on_delete=models.CASCADE
    )
    
    code = models.ForeignKey(
        Account,
        related_name ="entries",
        on_delete=models.CASCADE
    )
    entry_type = models.IntegerField(choices=ENTRY_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        verbose_name = ("Entry")
        verbose_name_plural = ("Entries")
        ordering = ["entry_type","code","amount"]
    
    def get_entry_balance(self):
        if self.entry_type == self.code.get_account_type():
            return self.amount 
        else:
            return self.amount * -1
    
    def __str__(self):
        return f"{self.transaction}-{self.entry_type}"