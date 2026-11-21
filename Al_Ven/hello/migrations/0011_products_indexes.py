from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('hello', '0010_productinquiry'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='products',
            index=models.Index(fields=['sale'], name='products_sale_idx'),
        ),
        migrations.AddIndex(
            model_name='products',
            index=models.Index(fields=['conter'], name='products_conter_idx'),
        ),
        migrations.AddIndex(
            model_name='products',
            index=models.Index(fields=['date_prod'], name='products_date_prod_idx'),
        ),
    ]
