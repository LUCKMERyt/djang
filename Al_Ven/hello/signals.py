from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Products


@receiver(post_save, sender=Products)
@receiver(post_delete, sender=Products)
def clear_products_cache(sender, **kwargs):
    """При изменении/удалении товаров кэшированная страница каталога сбрасывается."""
    cache.clear()
