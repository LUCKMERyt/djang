from django.apps import AppConfig


class HelloConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hello'

    def ready(self):
        # NOTE: Регистрируем сигналы (инвалидация кэша каталога при сохранении/удалении товаров).
        from . import signals  # noqa: F401,E402
