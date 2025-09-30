from django.apps import AppConfig

class CloudCustomizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cloud_customization'

    def ready(self) -> None:
        from horilla.urls import include, path, urlpatterns
        import cloud_customization.signals
        from django.contrib.auth.models import User

        from .models import CustomUserManager
        urlpatterns.append(
            path("", include("cloud_customization.urls")),
        )
        User.add_to_class('objects', CustomUserManager())
        return super().ready()