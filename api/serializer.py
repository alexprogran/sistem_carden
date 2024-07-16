from rest_framework import serializers
from cadastro.models import AlunoModel, CategoriaProdutoModel, DebitoModel, FuncionarioModel


class AlunoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlunoModel
        fields = ['nome','turma','responsavel','telefone_responsavel']


class CategoriaProdutoSerializer(serializers.Serializer):
    categoria = serializers.CharField()
    usuario = serializers.CharField()
    unidade = serializers.DateField()


    def validate(self, attrs):

        valid = super().validate(attrs)

        categ = attrs['categoria']
        unid = attrs['unidade']
        user = attrs['usuario']

        # Checando se já existe uma categoria com os mesmos valores de unidade e usuário.
        if CategoriaProdutoModel.objects.filter(categoria=categ, unidade=unid, usuario=user).exists():
            raise serializers.ValidationError('Categoria inválida, já existe em nosso cadastro.')
        
        return attrs



class CategoriaProdutoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaProdutoModel
        fields = ['id','categoria','usuario','unidade']

  


class DebitoSerializer(serializers.Serializer):
    data = serializers.DateField()
    valor_total = serializers.FloatField()


class DebAlunoModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = DebitoModel
        fields = ['usuario', 
                  'unidade', 
                  'aluno', 
                  'produto',
                  'valor_unitario',
                  'quantidade',
                  'valor_total',
                  'data',
                  'criado_em']


class FuniconarioModelSeiralzer(serializers.ModelSerializer):
    class Meta:
        model = FuncionarioModel
        fields = ['usuario','unidade','funcionario','telefone']





