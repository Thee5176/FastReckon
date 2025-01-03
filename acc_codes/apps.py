from django.apps import AppConfig
from django.db.models.signals import post_migrate

class AccCodesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'acc_codes'

    def ready(self):
        from acc_codes import signals