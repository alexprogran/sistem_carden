# Generated by Django 4.2 on 2023-12-30 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0027_alter_estoquemodel_categoria"),
    ]

    operations = [
        migrations.AlterField(
            model_name="estoquemodel",
            name="produto",
            field=models.CharField(
                blank=True, max_length=25, null=True, verbose_name="Produto"
            ),
        ),
    ]