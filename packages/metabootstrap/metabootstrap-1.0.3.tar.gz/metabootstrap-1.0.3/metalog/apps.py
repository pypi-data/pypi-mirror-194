from django.apps import AppConfig


class MetalogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "metabootstrap.metalog"
    verbose_name = "Metalog"

    def ready(self):
        import metabootstrap.metalog.models
