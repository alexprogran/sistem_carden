from rest_framework import serializers
from cadastro.models import AlunoModel, CategoriaProdutoModel


class AlunoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlunoModel
        fields = ['nome','turma','responsavel','telefone_responsavel']


class CategoriaProdutoSerializer(serializers.Serializer):
    categoria = serializers.CharField()


class CategoriaProdutoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaProdutoModel
        fields = ['categoria']