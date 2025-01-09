from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account, AccountLevel1, AccountLevel2, AccountLevel3

User = get_user_model()

class AccountPopulator:
    @staticmethod
    @receiver(post_save, sender=User)
    def handle_post_migrate(sender, created, instance,**kwargs):
        if created:
            AccountPopulator.populate_AccountLevel1()
            AccountPopulator.populate_AccountLevel2()
            AccountPopulator.populate_AccountLevel3()
            AccountPopulator.populate_EquityAccount(instance)

    @staticmethod
    def populate_AccountLevel1():
        CHART_OF_ACCOUNT = [
            ("1","Asset",""),
            ("2","Liability",""),
            ("3","Equity",""),
            ("4","Revenue",""),
            ("5","Expense",""),
            ("6","Gain",""),
            ("7","Loss",""),
        ]
        for (c,n,g) in CHART_OF_ACCOUNT:
            AccountLevel1.objects.get_or_create(code=c,name=n,guideline=g)

    @staticmethod
    def populate_AccountLevel2():
        ACCOUNT_TYPE = [
            ("11","Current Asset", 1,""),
            ("12","Fixed Asset", 1,""),
            ("21","Current Liability", 2,""),
            ("22","Long-term Liability", 2,""),
            ("30","Equity", 2,""),
            ("41","Personal Revenue", 2,""),
            ("42","Corporate Revenue", 2,""),
            ("51","Personal Expense", 1,""),
            ("52","Corporate Expense", 1,""),
        ]
        for (c,n,b,g) in ACCOUNT_TYPE:
            level1_code = c[0]
            try:
                level1_instance = AccountLevel1.objects.get(code=level1_code)
                
                AccountLevel2.objects.get_or_create(
                    code=c,
                    name=n,
                    balance=b,
                    guideline=g,
                    level1=level1_instance
                )
            except AccountLevel1.DoesNotExist:
                print(f"AccountLevel1 with code '{level1_code}' does not exist.")

    @staticmethod
    def populate_AccountLevel3():
        ACCOUNT_GROUP = [
            #Fixed Asset 11
            ("1101", "Cash", 1,""),
            ("1102", "Deposit", 1,""),
            ("1103", "E-wallet", 1,""),
            ("1104", "Debit Card", 1,""),
            ("1105", "Account Receivable", 1,""),
            #Asset 12
            ("1201", "Inventory", 1,""),
            ("1202", "Equipment", 1,""),
            ("1203", "Vehicle", 1,""),
            ("1204", "Taxes Receivable", 1,""),
            ("1205", "Accured Wage", 1,""),
            #Liability 21
            ("2101", "Credit Card", 2,""),
            ("2102", "Account Payable", 2,""),
            ("2103", "Accured Expense", 2,""),
            ("2104","Taxes Payable", 2,""),
            #Liability 22
            ("2201","Long-term Debt", 2,""),
            #Equity 30
            ("3001","Stock", 2,""),
            ("3002","Capital", 2,""),
            ("3003","Partnership Equity", 2,""),
            ("3004","Other Equity", 2,""),
            ("3005","Dividend", 2,""),
            #Personal Revenue 41
            ("4101", "Salary Revenue", 2,""),
            ("4102", "Wage Revenue", 2,""),
            ("4103", "Licensing Revenue", 2,""),
            ("4104", "Interest Revenue", 2,""),
            ("4105", "Rent Revenue", 2,""),
            ("4106", "Business Revenue", 2,""),
            ("4107", "Scholarship Stipend", 2,""),
            ("4108", "Allowance", 2,""),
            #Business Revenue 42
            ("4211", "Goods", 2,""),
            ("4212", "Services", 2,""),
            ("4213", "Products", 2,""),   
            ("4214", "Subsciptions", 2,""),
            #Personal Expenses 51
            ("5101", "Food Expense", 1,""),
            ("5102", "Transportation Expense", 1,""),
            ("5103", "Shopping Expense", 1,""),
            ("5104", "Utilities Bill", 1,""),
            ("5105", "Health Expense", 1,""),
            ("5106", "Education Expense", 1,""),
            ("5107", "Social & Recreation Expense", 1,""),
            ("5108", "Family Expense", 1,""),
            ("5109", "Miscellaneous Expense", 1,""),
            ("5110", "Accommodation Expense", 1,""),
            #Business Expense 52
            ("5201","Payroll", 1,""),
            ("5202","Rent", 1,""),
            ("5203","Repair and Maintenance", 1,""),
            ("5204","Depreciation", 1,""),
            ("5205","Utilities Expense", 1,""),
            ("5206","Cost of Sales", 1,""),
        ]
        for (c,n,b,g) in ACCOUNT_GROUP:
            level2_code = c[:2]
            try:
                level2_instance = AccountLevel2.objects.get(code=level2_code)
                
                AccountLevel3.objects.get_or_create(
                    code=c,
                    name=n,
                    balance=b,
                    guideline=g,
                    level2=level2_instance,
                )
            except AccountLevel2.DoesNotExist:
                print(f"AccountLevel2 with code '{level2_code}' does not exist.")

    @staticmethod
    def populate_EquityAccount(user_instance):
        EquityAccount = [
            ("300101", "Common Stock", None,""),
            ("300102", "Preferred Stock", None,""),
            ("300103", "Additional Paid-in Capital", None,""),
            ("300104", "Retained Earning", None,""),
            ("300105", "Other Comprehensive Income", None,""),
            ("300106", "Treasury Stock", None,""),
            ("300201", "Capital Contribution", None,""),
            ("300202", "Capital Withdrawal", None,""),
        ]
        for (c,n,b,g) in EquityAccount:
            level3_code = c[:4]
            try:
                level3_instance = AccountLevel3.objects.get(code=level3_code)

                Account.objects.get_or_create(
                    name=n,
                    level3=level3_instance,
                    sub_account=c[-2:],
                    balance=b,
                    guideline=g,
                    created_by=user_instance
                )
            except AccountLevel3.DoesNotExist:
                print(f"AccountLevel3 with code '{level3_code}' does not exist.")