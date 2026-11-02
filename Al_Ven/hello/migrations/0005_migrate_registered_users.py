from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations
import hashlib
import unicodedata


def migrate_registered_users(apps, schema_editor):
    RegisteredUser = apps.get_model("hello", "RegisteredUser")
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    database = schema_editor.connection.alias

    for old_user in RegisteredUser.objects.using(database).all().iterator():
        email = old_user.email.strip().lower()
        if (not email or User.objects.using(database).filter(email__iexact=email).exists()):
            continue
        suffix = hashlib.sha256(unicodedata.normalize("NFKC", email).encode("utf-8")).hexdigest()[:20]
        username = f"{email[:120]}-{suffix}"
        if User.objects.using(database).filter(username=username).exists():
            continue
        user = User(
            username=username,
            email=email,
            first_name=old_user.name[:150],
            is_active=True,
        )
        user.password = make_password(old_user.password)
        user.save(using=database)


class Migration(migrations.Migration):
    dependencies = [
        ("hello", "0004_review_alter_category_options_alter_person_options_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(migrate_registered_users, migrations.RunPython.noop),
        migrations.DeleteModel(name="RegisteredUser"),
    ]
