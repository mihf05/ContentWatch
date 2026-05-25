from django.apps import AppConfig


class CollaborationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collaboration'
    verbose_name = 'Real-time Collaboration'

    def ready(self):
        import collaboration.signals  # noqa: F401
