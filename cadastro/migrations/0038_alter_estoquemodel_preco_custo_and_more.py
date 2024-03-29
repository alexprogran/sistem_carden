# Generated by Django 4.2 on 2023-12-31 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0037_alter_estoquemodel_preco_custo_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="estoquemodel",
            name="preco_custo",
            field=models.DecimalField(
                decimal_places=2, max_digits=20, verbose_name="Preço custo"
            ),
        ),
        migrations.AlterField(
            model_name="estoquemodel",
            name="preco_varejo",
            field=models.DecimalField(
                decimal_places=2, max_digits=20, verbose_name="Preço varejo"
            ),
        ),
        migrations.AlterField(
            model_name="estoquemodel",
            name="total_custo",
            field=models.DecimalField(
                decimal_places=2, max_digits=20, verbose_name="Total custo"
            ),
        ),
        migrations.AlterField(
            model_name="estoquemodel",
            name="total_varejo",
            field=models.DecimalField(
                decimal_places=2, max_digits=20, verbose_name="Total varejo"
            ),
        ),
    ]
