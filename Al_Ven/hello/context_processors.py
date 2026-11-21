from django.conf import settings as _settings


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
        'address': _settings.SITE_ADDRESS, 'vk': _settings.SITE_VK,
        'telegram': _settings.SITE_TELEGRAM, 'youtube': _settings.SITE_YOUTUBE,
    }}
