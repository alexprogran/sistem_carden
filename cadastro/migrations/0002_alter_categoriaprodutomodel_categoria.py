# Generated by Django 4.2 on 2023-12-25 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="categoriaprodutomodel",
            name="categoria",
            field=models.CharField(
                blank=True, max_length=25, null=True, verbose_name="Categoria"
            ),
        ),
    ]