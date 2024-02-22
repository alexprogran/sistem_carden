# Generated by Django 4.2 on 2023-12-27 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0023_alter_debitomodel_quantidade_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="debitomodel",
            name="quantidade",
            field=models.DecimalField(
                decimal_places=0, default=1.0, max_digits=10, verbose_name="Quantidade"
            ),
        ),
    ]
