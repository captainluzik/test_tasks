# Generated by Django 5.1.5 on 2025-01-15 11:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("user_updated", "User Updated"),
                            ("task_created", "Task Created"),
                            ("task_updated", "Task Updated"),
                            ("event_created", "Event Created"),
                            ("event_updated", "Event Updated"),
                        ],
                        max_length=50,
                    ),
                ),
                ("data", models.JSONField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="WebhookClient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("url", models.URLField()),
                ("secret_key", models.CharField(max_length=255)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="WebhookSubscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("user_updated", "User Updated"),
                            ("task_created", "Task Created"),
                            ("task_updated", "Task Updated"),
                            ("event_created", "Event Created"),
                            ("event_updated", "Event Updated"),
                        ],
                        max_length=50,
                    ),
                ),
                ("user_id", models.IntegerField(blank=True, null=True)),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subscriptions",
                        to="main.webhookclient",
                    ),
                ),
            ],
        ),
    ]
