from django.apps import AppConfig


class CartrigeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cartrige'

    def ready(self):
        import cartrige.signals
