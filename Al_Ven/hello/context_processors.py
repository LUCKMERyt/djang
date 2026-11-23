from django.conf import settings as _settings
from django.core.exceptions import ImproperlyConfigured


def _readable_address(value):
    # Repair the observed Windows-1251 decoding of a UTF-8 SITE_ADDRESS value.
    if not any(marker in value for marker in ("Рђ", "СЂ", "Сѓ")):
        return value
    try:
        return value.encode("cp1251").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError) as error:
        raise ImproperlyConfigured(
            "SITE_ADDRESS contains text with an invalid Windows-1251/UTF-8 encoding."
        ) from error


def settings(request):
    # NOTE: В шаблоны передаются только ID счётчиков аналитики, а не все настройки Django:
    # иначе любой шаблон мог бы прочитать SECRET_KEY и пароли.
    return {'settings': {
        'YMETRICA_ID': _settings.YMETRICA_ID,
        'GA_MEASUREMENT_ID': _settings.GA_MEASUREMENT_ID,
    }}


def site_contacts(request):
    # NOTE: Контакты задаются переменными окружения и доступны всем шаблонам.
    # TODO: Перед публикацией заменить демонстрационные контакты на реальные.
    return {'SITE_CONTACTS': {
        'email': _settings.SITE_EMAIL, 'phone': _settings.SITE_PHONE,
        'address': _readable_address(_settings.SITE_ADDRESS), 'vk': _settings.SITE_VK,
        'telegram': _settings.SITE_TELEGRAM, 'youtube': _settings.SITE_YOUTUBE,
    }}
