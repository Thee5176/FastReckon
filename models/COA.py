from django.db import models 

class AccountGroup(models.Model):
    """1st one Digit - 1 Asset,2 Liability,3 Equity,4 Income,5 Expense"""
    ACCOUNT_GROUPS = (
        (1, 'Asset'),
        (2, 'Liability'),
        (3, 'Equity'),
        (4, 'Income'),
        (5, 'Expense'),
    )
    group_id = models.IntegerField(primary_key=True, max_length=1, choices=ACCOUNT_GROUPS)
    group_name = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = 'Group of Account'
        verbose_name_plural = 'Group of Accounts'
        abstract = True
    
class AccountType(AccountGroup):
    """following 2 digits - For example, 1-10 Current_Asset"""
    type_id = models.PositiveIntegerField(primary_key=True)
    type_name = models.CharField(max_length=50) 

    class Meta:
        verbose_name = 'Type of Account'
        verbose_name_plural = 'Type of Accounts'
        abstract = True
    
class Account(AccountType):
    """following 3 digits - For example, 110-001 Cash"""
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=50) 

    class Meta:
        abstract = True
        
class SubAccount(Account):
    """optional last 2 digits 
    - For example, 110404-01 Account Receivable from -FRIEND#1_
                 , 110404-02 Account Receivable from -FRIEND#2_
    """
    id = models.PositiveIntegerField(null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
        