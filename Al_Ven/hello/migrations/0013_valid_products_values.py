from django.core.validators import MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hello", "0012_update_person_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="sale",
            field=models.IntegerField(
                "Цена",
                validators=[MinValueValidator(0)],
            ),
        ),
        migrations.AlterField(
            model_name="products",
            name="conter",
            field=models.IntegerField(
                "Количество",
                validators=[MinValueValidator(0)],
            ),
        ),
    ]
