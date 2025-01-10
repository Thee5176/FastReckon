from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
import os, sys
import pandas as pd

from acc_codes.models import AccountLevel1, AccountLevel2, AccountLevel3, Account

class AccountPopulator:
    # Prepare file path
    level1_path = os.path.join(settings.BASE_DIR, "static/csv/level1.csv")
    level2_path = os.path.join(settings.BASE_DIR, "static/csv/level2.csv")
    level3_path = os.path.join(settings.BASE_DIR, "static/csv/level3.csv")
    base_path   = os.path.join(settings.BASE_DIR, "static/csv/base.csv")
    
    # Read CSV file into DataFrame
    df_1    = pd.read_csv(level1_path, delimiter=";", quotechar='"')
    df_2    = pd.read_csv(level2_path, delimiter=";", quotechar='"')
    df_3    = pd.read_csv(level3_path, delimiter=";", quotechar='"')
    df_base = pd.read_csv(base_path, delimiter=";", quotechar='"')

    # Adjust nan value to None
    df_base['balance'] = df_base['balance'].replace({pd.NA:None})
    
    def csv_to_variable(df):
        """_summary_

        Args:
            df (File handler): dataframe handler
        """
        def decorator(func):
            def wrapper_func(*args, **kwargs):       
                for _, row in df.iterrows():
                    c=str(row['code'])
                    n=row['name']
                    b=row['balance']
                    g=row['guideline']
                    func(c,n,b,g, *args, **kwargs)
            return wrapper_func
        return decorator
    
    @csv_to_variable(df_1)   
    def populate_Level1(c,n,b,g):            
        try:
            AccountLevel1.objects.get_or_create(
                code=c,
                name=n,
                balance=b,
                guideline=g
            )
        except:
            print(f"Encounter error when creating account: {c}")
            sys.exit(1)

    @csv_to_variable(df_2)
    def populate_Level2(c,n,b,g):
        level1_code = c[0]        
        level1_instance = AccountLevel1.objects.get(code=level1_code)
        try:
            AccountLevel2.objects.get_or_create(
                code=c,
                name=n,
                balance=b,
                guideline=g,
                level1=level1_instance
            )
        except:
            print(f"Encounter error when creating account: {c}")
            sys.exit(1)

    @csv_to_variable(df_3)      
    def populate_Level3(c,n,b,g):
        level2_code = c[:2]        
        level2_instance = AccountLevel2.objects.get(code=level2_code)
        try:
            AccountLevel3.objects.get_or_create(
                code=c,
                name=n,
                balance=b,
                guideline=g,
                level2=level2_instance
            )
        except:
            print(f"Encounter error when creating account: {c}")
            sys.exit(1)

    @csv_to_variable(df_base)
    def populate_base(c,n,b,g,user_instance=None):
        if not user_instance == None:
            level3_code = c[:4]        
            level3_instance = AccountLevel3.objects.get(code=level3_code)
            
            try:
                if b is not None:
                    Account.objects.get_or_create(
                        level3=level3_instance,     #code 1/2
                        sub_account=c[-2:],         #code 2/2
                        name=n,
                        guideline=g,
                        balance=b,
                        created_by=user_instance
                    )
                else:
                    Account.objects.get_or_create(
                        level3=level3_instance,     #code 1/2
                        sub_account=c[-2:],         #code 2/2
                        name=n,
                        guideline=g,
                        created_by=user_instance
                    )
            except Exception as e:
                print(f"Encounter error creating account: {c} with error {e}")
                sys.exit(1)
                
        else:
            print(f"Base Account isn't created: no user_instance is parsed.")
            sys.exit(1)

class Command(BaseCommand):
    help = "This command populate account level 1-3 and assign basic account to new user"
    
    def handle(self, *args, **kwargs):
        print("Running script populate_account...")
        AccountPopulator.populate_Level1()
        print("Succesfully populated account level1")
        AccountPopulator.populate_Level2()
        print("Succesfully populated account level2")
        AccountPopulator.populate_Level3()
        print("Succesfully populated account level3")
    