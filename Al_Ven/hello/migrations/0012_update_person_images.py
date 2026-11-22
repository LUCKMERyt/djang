from django.db import migrations


IMAGE_PATHS = {
    "people/1-portrait.jpg": "people/1-sulki.jpg",
    "people/2-portrait.jpg": "people/2-sulki.jpg",
    "people/3-portrait.jpg": "people/3-sulki.jpg",
    "people/4-portrait.jpg": "people/4-sulki.jpg",
    "people/6-portrait.jpg": "people/6-sulki.jpg",
}


def update_person_image_paths(apps, schema_editor):
    person_model = apps.get_model("hello", "Person")
    database = schema_editor.connection.alias
    for old_path, new_path in IMAGE_PATHS.items():
        person_model.objects.using(database).filter(image=old_path).update(image=new_path)


def restore_person_image_paths(apps, schema_editor):
    person_model = apps.get_model("hello", "Person")
    database = schema_editor.connection.alias
    for old_path, new_path in IMAGE_PATHS.items():
        person_model.objects.using(database).filter(image=new_path).update(image=old_path)


class Migration(migrations.Migration):
    dependencies = [
        ("hello", "0011_products_indexes"),
    ]

    operations = [
        migrations.RunPython(update_person_image_paths, restore_person_image_paths),
    ]
