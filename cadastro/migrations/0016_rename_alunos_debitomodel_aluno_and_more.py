# Generated by Django 4.2 on 2023-12-26 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cadastro", "0015_rename_aluno_debitomodel_alunos_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="debitomodel",
            old_name="alunos",
            new_name="aluno",
        ),
        migrations.RenameField(
            model_name="debitomodel",
            old_name="produtos",
            new_name="produto",
        ),
    ]
