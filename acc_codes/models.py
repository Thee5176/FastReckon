from django.conf import settings
from django.db import models
from django.urls import reverse

class AccountLevel1(models.Model):
    code = models.CharField(max_length=1, unique=True)
    name = models.CharField(max_length=50)
    guideline = models.TextField(null=True, blank=True)
    
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
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=50)
    guideline = models.TextField(null=True, blank=True)
    balance = models.IntegerField(choices=BALANCE_TYPE)
    level1 = models.ForeignKey(AccountLevel1, related_name="level2_accounts", on_delete=models.CASCADE)

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
    code = models.CharField(max_length=4, unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    guideline = models.TextField(null=True, blank=True)
    balance = models.IntegerField(choices=BALANCE_TYPE)
    level2 = models.ForeignKey(AccountLevel2 ,related_name="level3_accounts", on_delete=models.CASCADE)

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
    
    name = models.CharField(max_length=50)
    level3 = models.ForeignKey(AccountLevel3, related_name="accounts", on_delete=models.CASCADE)
    sub_account = models.CharField(max_length=2)
    detailed_account = models.CharField(max_length=2, null=True, blank=True)
    balance_adjustment = models.IntegerField(choices=BALANCE_TYPE, null=True, blank=True)
    guideline = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    @property
    def code(self):
        coa = f"{self.level3.code}{self.sub_account}"
        if self.detailed_account :
            coa += f"-{self.detailed_account}"
        return coa
    
    class Meta:
        ordering = ["level3","sub_account","detailed_account"]
        verbose_name = ("Account")
        verbose_name_plural = ("Accounts")

    def __str__(self):
        return f"{self.code} | {self.name}"
    
    def get_absolute_url(self):
        return reverse("account_detail", kwargs={"pk": self.pk})
    