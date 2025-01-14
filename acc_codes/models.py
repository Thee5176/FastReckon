from django.conf import settings
from django.db import models
from django.urls import reverse

class AccountLevel1(models.Model):
    BALANCE_TYPE = [
        (1, "Dr"),
        (2, "Cr"),
    ]
    code = models.CharField(max_length=1, unique=True)
    name = models.CharField(max_length=50)
    guideline = models.TextField(null=True, blank=True)
    balance = models.IntegerField(choices=BALANCE_TYPE)

    
    class Meta:
        ordering = ["code"]
        verbose_name = ("AccountLevel1")
        verbose_name_plural = ("AccountLevel1s")

    def __str__(self):
        return f"{self.code} | {self.name}"

class AccountLevel2(models.Model):
    BALANCE_TYPE = [
        (1, "Dr"),
        (2, "Cr"),
    ]
    level1 = models.ForeignKey(AccountLevel1, related_name="level2", on_delete=models.CASCADE)
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=50)
    guideline = models.TextField(null=True, blank=True)
    balance = models.IntegerField(choices=BALANCE_TYPE)

    class Meta:
        ordering = ["code"]
        verbose_name = ("AccountLevel2")
        verbose_name_plural = ("AccountLevel2s")

    def __str__(self):
        return f"{self.code} | {self.name}"

class AccountLevel3(models.Model):
    BALANCE_TYPE = [
        (1, "Dr"),
        (2, "Cr"),
    ]
    level2 = models.ForeignKey(AccountLevel2 ,related_name="level3", on_delete=models.CASCADE)
    code = models.CharField(max_length=4, unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    guideline = models.TextField(null=True, blank=True)
    balance = models.IntegerField(choices=BALANCE_TYPE)

    class Meta:
        ordering = ["code"]
        verbose_name = ("AccountLevel3")
        verbose_name_plural = ("AccountLevel3s")

    def __str__(self):
        return f"{self.code} | {self.name}"
    
class Account(models.Model):
    
    BALANCE_TYPE = [
        (1, "Dr"),
        (2, "Cr"),
    ]
    
    level3 = models.ForeignKey(AccountLevel3, related_name="accounts", on_delete=models.CASCADE)
    sub_account = models.CharField(max_length=2)
    detailed_account = models.CharField(max_length=2, null=True, blank=True)
    code = models.CharField(max_length=9, blank=True)
    name = models.CharField(max_length=50)
    balance = models.IntegerField(choices=BALANCE_TYPE, null=True, blank=True)
    guideline = models.TextField(null=True, blank=True)
    #Meta
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name=("accounts"), on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["level3","sub_account","detailed_account"]
        verbose_name = ("Account")
        verbose_name_plural = ("Accounts")
    
    def update_code(self):
        self.code = f"{self.level3.code}{self.sub_account}"
        if self.detailed_account :
            self.code += f"-{self.detailed_account}"
            
    def save(self,*args, **kwargs):
        self.update_code()
        super(Account, self).save(*args, **kwargs)
    
    @property
    def record_count(self):
        return self.entries.all().count

    def get_account_type(self):
        return self.balance if self.balance else self.level3.balance
    
    def get_account_balance(self):
        balance = 0
        for entry in self.entries.all():
            if entry.entry_type == self.get_account_type():
                balance += entry.amount
            else:
                balance -= entry.amount
        return balance
    
    def __str__(self):
        return f"{self.code} | {self.name}"
    
    def get_absolute_url(self):
        return reverse("account_detail", kwargs={"pk": self.pk})
    