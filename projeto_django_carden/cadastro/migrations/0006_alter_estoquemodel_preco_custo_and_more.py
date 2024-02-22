# Generated by Django 4.2 on 2023-12-25 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0005_alter_estoquemodel_quantidade"),
    ]

    operations = [
        migrations.AlterField(
            model_name="estoquemodel",
            name="preco_custo",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=5, verbose_name="Preço custo"
            ),
        ),
        migrations.AlterField(
            model_name="estoquemodel",
            name="preco_varejo",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=5, verbose_name="Preço varejo"
            ),
        ),
        migrations.AlterField(
            model_name="estoquemodel",
            name="quantidade",
            field=models.DecimalField(
                decimal_places=0, default=0, max_digits=5, verbose_name="Quantidade"
            ),
        ),
        migrations.AlterField(
            model_name="estoquemodel",
            name="total_custo",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=5, verbose_name="Total custo"
            ),
        ),
        migrations.AlterField(
            model_name="estoquemodel",
            name="total_varejo",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=5, verbose_name="Total varejo"
            ),
        ),
    ]
