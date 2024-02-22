# Generated by Django 4.2 on 2023-12-26 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0008_alter_alunomodel_telefone_responsavel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cadastrosvendamodel",
            name="produto",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="cadastro.estoquemodel",
                verbose_name="Produto",
            ),
        ),
    ]