# Generated by Django 4.2 on 2023-12-26 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0013_alter_debitomodel_produto"),
    ]

    operations = [
        migrations.AlterField(
            model_name="debitomodel",
            name="aluno",
            field=models.CharField(
                blank=True, max_length=25, null=True, verbose_name="Aluno"
            ),
        ),
        migrations.AlterField(
            model_name="debitomodel",
            name="produto",
            field=models.CharField(
                blank=True, max_length=25, null=True, verbose_name="produto"
            ),
        ),
    ]
