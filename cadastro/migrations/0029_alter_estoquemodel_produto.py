# Generated by Django 4.2 on 2023-12-30 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0028_alter_estoquemodel_produto"),
    ]

    operations = [
        migrations.AlterField(
            model_name="estoquemodel",
            name="produto",
            field=models.CharField(max_length=25, null=True, verbose_name="Produto"),
        ),
    ]
