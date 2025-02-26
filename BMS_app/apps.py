from django.apps import AppConfig


class BmsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BMS_app'

    def ready(self):
        import BMS_app.signals
