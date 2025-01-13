from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .management.commands.populate_account import AccountPopulator

User = get_user_model()

@staticmethod
@receiver(post_save, sender=User)
def handle_post_migrate(sender, created, instance,**kwargs):
    if created:
        AccountPopulator.populate_Level1()
        print("Succesfully populated account level1")
        AccountPopulator.populate_Level2()
        print("Succesfully populated account level2")
        AccountPopulator.populate_Level3()
        print("Succesfully populated account level3")
        AccountPopulator.populate_base(user_instance=instance)
        print(f"populated initial account structure for new user:")