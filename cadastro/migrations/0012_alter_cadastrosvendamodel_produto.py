# Generated by Django 4.2 on 2023-12-26 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0011_alter_cadastrosvendamodel_produto"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cadastrosvendamodel",
            name="produto",
            field=models.CharField(
                blank=True, max_length=25, null=True, verbose_name="Produto"
            ),
        ),
    ]
