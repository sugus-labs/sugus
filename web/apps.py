from django.apps import AppConfig
from web.science import generate_model

class WebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web'
    def ready(self):
        generate_model()