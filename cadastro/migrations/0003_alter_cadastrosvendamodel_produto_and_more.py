# Generated by Django 4.2 on 2023-12-25 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0002_alter_categoriaprodutomodel_categoria"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cadastrosvendamodel",
            name="produto",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="cadastro.estoquemodel",
                verbose_name="Produto",
            ),
        ),
        migrations.AlterField(
            model_name="categoriaprodutomodel",
            name="categoria",
            field=models.CharField(
                default="S/categoira", max_length=25, verbose_name="Categoria"
            ),
        ),
    ]