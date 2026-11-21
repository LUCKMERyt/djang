from django.db import migrations, models


class Migration(migrations.Migration):
    """Добавление slug для детальных страниц товаров (/products/<slug>/)."""

    dependencies = [
        ('hello', '0008_person_email_person_phone_person_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='slug',
            field=models.SlugField(blank=True, null=True, verbose_name='URL-пропуск', unique=True),
        ),
    ]
