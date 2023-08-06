from django.apps import AppConfig


class OntoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'onto'

    def ready(self) -> None:
        from . import signals
        return super().ready()