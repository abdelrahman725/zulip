# Generated by Django 5.0.7 on 2024-08-03 06:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("zerver", "0616_userprofile_can_change_user_emails"),
    ]

    operations = [
        migrations.CreateModel(
            name="RealmSession",
            fields=[
                (
                    "session_key",
                    models.CharField(
                        max_length=40, primary_key=True, serialize=False, verbose_name="session key"
                    ),
                ),
                ("session_data", models.TextField(verbose_name="session data")),
                ("expire_date", models.DateTimeField(db_index=True, verbose_name="expire date")),
                ("ip_address", models.GenericIPAddressField(db_index=True, null=True)),
                (
                    "realm",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.CASCADE, to="zerver.realm"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["realm", "user"], name="zerver_realmsession_realm_user_idx"
                    )
                ],
            },
        ),
    ]
