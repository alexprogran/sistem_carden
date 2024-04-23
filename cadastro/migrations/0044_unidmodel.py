# Generated by Django 4.2 on 2024-01-27 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0043_usuariosmodel"),
    ]

    operations = [
        migrations.CreateModel(
            name="UnidModel",
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
                ("usuario", models.CharField(max_length=25, verbose_name="Ususario")),
                ("unidade", models.CharField(max_length=25, verbose_name="Unidade")),
            ],
        ),
    ]