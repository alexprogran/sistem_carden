# Generated by Django 4.2 on 2024-01-23 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0040_alter_cadastrosvendamodel_quantidade_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="TesteEstoque",
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
                ("usuario", models.CharField(max_length=25, verbose_name="Usuário")),
                ("produto", models.CharField(max_length=25, verbose_name="Produto")),
                (
                    "quantidade",
                    models.CharField(max_length=25, verbose_name="Quantidade"),
                ),
                ("valor", models.IntegerField(verbose_name="Valor")),
            ],
        ),
    ]