# Generated by Django 4.2 on 2023-12-28 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0026_alter_debitomodel_valor_unitario"),
    ]

    operations = [
        migrations.AlterField(
            model_name="estoquemodel",
            name="categoria",
            field=models.CharField(max_length=25, null=True, verbose_name="Categoria"),
        ),
    ]
