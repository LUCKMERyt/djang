from django.conf import settings as _settings


def settings(request):
    # NOTE: Собственный context_processor, который пробрасывает все
    # настройки Django в шаблоны (название `settings`, как в ожиданиях).
    return {'settings': _settings}


def site_contacts(request):
    # NOTE: Контакты задаются переменными окружения и доступны всем шаблонам.
    # TODO: Перед публикацией заменить демонстрационные контакты на реальные.
    return {'SITE_CONTACTS': {
        'email': _settings.SITE_EMAIL, 'phone': _settings.SITE_PHONE,
        'address': _settings.SITE_ADDRESS, 'vk': _settings.SITE_VK,
        'telegram': _settings.SITE_TELEGRAM, 'youtube': _settings.SITE_YOUTUBE,
    }}
