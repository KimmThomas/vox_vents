from django.apps import AppConfig


class VoxappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voxapp'

    def ready(self):
        import voxapp.signals

