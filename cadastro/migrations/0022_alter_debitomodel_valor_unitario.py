# Generated by Django 4.2 on 2023-12-27 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0021_alter_debitomodel_quantidade_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="debitomodel",
            name="valor_unitario",
            field=models.FloatField(default=1.0, verbose_name="Valor"),
        ),
    ]
