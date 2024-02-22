# Generated by Django 4.2 on 2023-12-31 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0029_alter_estoquemodel_produto"),
    ]

    operations = [
        migrations.AlterField(
            model_name="estoquemodel",
            name="quantidade",
            field=models.DecimalField(
                decimal_places=0, max_digits=5, verbose_name="Quantidade"
            ),
        ),
    ]
