from django.apps import AppConfig

class TodolistapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todolistAPI'


    def ready(self):
        import todolistAPI.signals
