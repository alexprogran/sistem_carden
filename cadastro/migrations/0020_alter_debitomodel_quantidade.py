# Generated by Django 4.2 on 2023-12-27 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0019_alter_debitomodel_valor_unitario"),
    ]

    operations = [
        migrations.AlterField(
            model_name="debitomodel",
            name="quantidade",
            field=models.DecimalField(
                decimal_places=0, max_digits=5, null=True, verbose_name="Quantidade"
            ),
        ),
    ]
