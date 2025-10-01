from django.apps import AppConfig
from threading import Thread


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from .rabbitmq import start_consumer

        # Lancer le consumer dans un thread séparé
        Thread(target=start_consumer, daemon=True).start()
