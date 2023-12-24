from django.apps import AppConfig

#  the apps.py file is typically used to configure the behavior of a Django app and to provide an application-specific configuration
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'  # Set the name of the application to 'accounts'

    def ready(self):
        import accounts.signals
