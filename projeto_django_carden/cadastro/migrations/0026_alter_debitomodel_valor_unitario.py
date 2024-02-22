# Generated by Django 4.2 on 2023-12-27 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0025_alter_debitomodel_quantidade"),
    ]

    operations = [
        migrations.AlterField(
            model_name="debitomodel",
            name="valor_unitario",
            field=models.DecimalField(
                decimal_places=2, max_digits=10, verbose_name="Valor unitário"
            ),
        ),
    ]
