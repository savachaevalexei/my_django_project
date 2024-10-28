from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    verbose_name = "Мой сайт"
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articles'
