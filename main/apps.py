from django.apps import AppConfig
from time import sleep


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from execute import update
        sleep(2)
        update.start()
