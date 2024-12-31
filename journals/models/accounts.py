from django.db import models

class AccountLevel1(models.Model):
    CHART_OF_ACCOUNT = [
        ("1","Asset"),
        ("2","Liability"),
        ("3","Equity"),
        ("4","Revenue"),
        ("5","Expense"),
        ("6","Gain"),
        ("7","Loss"),
    ]

    code = models.CharField(max_length=1, choices=CHART_OF_ACCOUNT, unique=True)
    name = models.CharField(max_length=50)
    guideline = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = ("AccountLevel1")
        verbose_name_plural = ("AccountLevel1s")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("AccountLevel1_detail", kwargs={"pk": self.pk})

class AccountLevel2(models.Model):
    ACCOUNT_CATAGORIES = [
        ("11","Current Asset"),
        ("12","Fixed Asset"),
        ("21","Current Liability"),
        ("22","Long-term Liability"),
        ("31", "Common Stock"),
        ("32", "Preferred Stock"),
        ("33", "Retained Earning"),
        ("41","Personal Revenue"),
        ("42","Corporate Revenue"),
        ("51","Personal Expense"),
        ("52","Corporate Expense"),
    ]

    code = models.CharField(max_length=2, choices=ACCOUNT_CATAGORIES, unique=True)
    name = models.CharField(max_length=50)
    guideline = models.TextField(null=True, blank=True)
    level1 = models.ForeignKey(AccountLevel1, related_name="level2_account", on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("AccountLevel2")
        verbose_name_plural = ("AccountLevel2s")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("AccountLevel2_detail", kwargs={"pk": self.pk})

class AccountLevel3(models.Model):
    MAIN_ACCOUNT = [
        #Asset
        ("1100", "Cash"),
        ("1102", "Deposit"),
        ("1103", "E-wallet"),
        ("1104", "Debit Card"),
        ("1105", "Account Receivable"), #Should have already received
        ("1106", "Deferred Income"),    #Yet to get paid
        ("1201", "Inventory"),
        ("1202", "Equipment"),
        ("1203", "Vehicle"),
        ("1204", "Taxes Receivable"),
        #Liability
        ("2101", "Credit Card"),
        ("2102", "Account Payable"),    #Should have already paid
        ("2103", "Accured Expense"),   #Yet to pay
        ("2201","Loan"),
        ("2202","Taxes Payable"),
        #Equity
        ("3100", "Common Stock"),
        ("3200", "Preferred Stock"),
        ("3300", "Retained Eearning"),
        #Personal Income
        ("4101", "Salary Revenue"),
        ("4102", "Wage Revenue"),
        ("4103", "Licensing Revenue"),
        ("4104", "Interest Revenue"),
        ("4105", "Rent Revenue"),
        ("4106", "Business Revenue"),
        ("4107", "Scholarship Stipend"),
        ("4108", "Allowance"),
        ("4109", "Tuition Expenses"),
        #Business Revenue
        ("4211", "Goods"),
        ("4212", "Services"),
        ("4213", "Products"),   
        ("4214", "Subsciptions"),
        #Personal Expenses
        ("5101", "Food Expense"),
        ("5102", "Transportation Expense"),
        ("5103", "Accommodation Expense"),
        ("5104", "Utilities Bill"),
        ("5105", "Health Expense"),
        ("5106", "Education Expense"),
        ("5107", "Social & Recreation Expense"),
        ("5108", "Family Expense"),
        ("5109", "Miscellaneous Expense"),
        #Business Expense
        ("5201","Payroll"),
        ("5202","Rent"),
        ("5203","Travel Expense"),
        ("5204","Depreciation"),
        ("5205","Utilities Expense"),
        ("5206","Cost of Goods Sold"),
    ]

    code = models.CharField(max_length=4, choices=MAIN_ACCOUNT, unique=True)
    name = models.CharField(max_length=50)
    guideline = models.TextField(null=True, blank=True)
    level2 = models.ForeignKey(AccountLevel2 ,related_name="level3_account", on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("AccountLevel3")
        verbose_name_plural = ("AccountLevel3s")

    def __str__(self):
        return f"{self.code} | {self.name}"

    def get_absolute_url(self):
        return reverse("AccountLevel3_detail", kwargs={"pk": self.pk})
    
class Account(models.Model):
    super_account = models.ForeignKey(AccountLevel3, on_delete=models.CASCADE)
    sub_account = models.CharField(max_length=3)
    detailed_account = models.CharField(max_length=2)
    name = models.CharField(max_length=50)
    guideline = models.TextField(null=True, blank=True)
 
    @property
    def code(self):
        coa = f"{self.super_account}{self.subaccount}"
        if detailed_account :
            coa += f"-{self.detailed_account}"
        return coa

    def __str__(self):
        return self.code
    