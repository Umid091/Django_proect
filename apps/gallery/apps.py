from django.apps import AppConfig

class GalleryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.gallery'

    def ready(self):
        print("--- GalleryConfig ready() ishladi ---")
        import apps.gallery.signals