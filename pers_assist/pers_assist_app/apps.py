from django.apps import AppConfig


class PersAssistAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pers_assist_app'


class AssistAppConfig(AppConfig):
    name = 'pers_assist_app'

    def ready(self):
        import pers_assist_app.signals