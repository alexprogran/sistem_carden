# Generated by Django 4.2 on 2024-02-04 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0047_categoriaprodutomodel_unidade_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="alunomodel",
            name="unidade",
            field=models.CharField(
                blank=True, max_length=25, null=True, verbose_name="Unidade"
            ),
        ),
        migrations.AddField(
            model_name="alunomodel",
            name="usuario",
            field=models.CharField(
                blank=True, max_length=25, null=True, verbose_name="Usuáiro"
            ),
        ),
    ]
