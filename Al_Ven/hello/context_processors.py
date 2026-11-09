from django.conf import settings


def site_contacts(request):
    # NOTE: Контакты задаются переменными окружения и доступны всем шаблонам.
    # TODO: Перед публикацией заменить демонстрационные контакты на реальные.
    return {'SITE_CONTACTS': {
        'email': settings.SITE_EMAIL, 'phone': settings.SITE_PHONE,
        'address': settings.SITE_ADDRESS, 'vk': settings.SITE_VK,
        'telegram': settings.SITE_TELEGRAM, 'youtube': settings.SITE_YOUTUBE,
    }}
