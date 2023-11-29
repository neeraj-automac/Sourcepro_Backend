from django.apps import AppConfig


class SourceproConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sourcepro'

    def ready(self):
        pass
        # from . import signals