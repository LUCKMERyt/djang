import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('hello', '0009_products_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductInquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Ваше имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('message', models.TextField(max_length=2000, verbose_name='Сообщение (что и в какой цене нужно?)')),
                ('status', models.CharField(choices=[('new', 'Новая'), ('handled', 'Обработана')], default='new', max_length=10, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inquiries', to='hello.products', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Заявка на товар',
                'verbose_name_plural': 'Заявки на товар',
                'ordering': ['-created_at'],
            },
        ),
    ]
