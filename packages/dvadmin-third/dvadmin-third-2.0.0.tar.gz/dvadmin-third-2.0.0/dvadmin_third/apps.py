from django.apps import AppConfig


class DvadminCeleryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dvadmin_third'
    url_prefix = "dvadmin_third"
