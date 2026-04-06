from django.apps import AppConfig
from django.core.management import call_command


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    def ready(self):
        try:
            call_command('loaddata', 'data.json')
        except Exception:
            # Handle cases where migrations haven't run or file is missing
            pass
