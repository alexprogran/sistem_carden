import json
from django.http import HttpResponse
from django.shortcuts import render
from cadastro.models import AlunoModel, CategoriaProdutoModel
from rest_framework.decorators import api_view,action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import viewsets
from api.serializer import AlunoModelSerializer, CategoriaProdutoSerializer, CategoriaProdutoModelSerializer

# sem utilizar o rest-framework
def view_api_testes_(request):

    instence_estoque = CategoriaProdutoModel.objects.all()
    dados = []
    for categoria in instence_estoque:
        dado = {'categoria':categoria.categoria}
        dados.append(dado)
    print(dados)   
    return HttpResponse(json.dumps(dados))



# com a utilização da rest-framework
@api_view()
def lita_categoria_(request):

    instence_estoque = CategoriaProdutoModel.objects.all()
    dados = []
    for categoria in instence_estoque:
        dado = {'categoria':categoria.categoria}
        dados.append(dado)
    
    return Response(dados)


# com a utilização da rest-framework
@api_view(http_method_names= ['POST'])
def criar_categoria_(request):
    categoria  = request.data['categoria']
    create = CategoriaProdutoModel.objects.create(categoria=categoria)        
    dados = []
    dado = {'categoria':create.categoria}
    dados.append(dado)
    
    return Response(dados)


# com a utilização da rest-framework com o "serializer.Serializer"
@api_view(http_method_names= ['POST'])
def criar_categoria(request):
    serializer = CategoriaProdutoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    categoria = serializer.validated_data['categoria']
    create = CategoriaProdutoModel.objects.create(categoria=categoria)        
    dados = []
    dado = {'categoria':create.categoria}
    dados.append(dado)
    
    return Response(dados)

# usando o "serializer.ModelSerializer"
@api_view()
def lita_categoria(request):

    db_categoria = CategoriaProdutoModel.objects.all()
    serializer = CategoriaProdutoModelSerializer(instance=db_categoria, many=True)
    
    return Response(serializer.data)


class AlunoViewSet(ViewSet):
    serializer_class = AlunoModelSerializer
    
    def create(self, request):
        db_aluno = AlunoModel.objects.all()
        serializer = AlunoModelSerializer(instance=db_aluno,data=request.data)
        serializer.is_valid(raise_exception=True)
        nome = serializer.validated_data['nome']
        turma = serializer.validated_data['turma']
        responsavel = serializer.validated_data['responsavel']
        telefone_responsavel =serializer.validated_data['telefone_responsavel']
        create = AlunoModel.objects.create(nome=nome, turma=turma, responsavel=responsavel,telefone_responsavel=telefone_responsavel)
        dado = {
            'nome': create.nome,
            'turma': create.turma,
            'responsavel': create.responsavel,
            'telefone_responsavel': create.telefone_responsavel
        }
        
        return Response(dado)


    def list(self, request):
        db_aluno = AlunoModel.objects.all()
        serializer = AlunoModelSerializer(instance=db_aluno, many=True)
        return Response(serializer.data)

    def retrieve( self, request, pk=None):
        try:
            db_aluno = AlunoModel.objects.get(id=pk)
        except AlunoModel.DoesNotExist:
            return Response({'error':'Aluno não encontrado'})
        serializer = AlunoModelSerializer(instance=db_aluno)
       
        return Response(serializer.data)
        

    def update(self, request, pk=None):
        # Obtenha o objeto existente pelo ID (pk)
        try:
            aluno = AlunoModel.objects.get(pk=pk)
        except AlunoModel.DoesNotExist:
            return Response({'error': 'Aluno não encontrada'})

        # Serialize os dados da solicitação para atualização
        serializer = AlunoModelSerializer(aluno, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Responda com os dados atualizados
        return Response(serializer.data)
    
    
    def partial_update(self,request, pk=None):
      
        try:
            db_aluno = AlunoModel.objects.get(pk=pk)
           
        except AlunoModel.DoesNotExist:
            return Response({'erro': 'Aluno não existe'})
        serializer = AlunoModelSerializer(db_aluno, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk=None):
        try:
            db_aluno = AlunoModel.objects.get(pk=pk) 

        except AlunoModel.DoesNotExist:
            return Response({'erro': 'Aluno não existe'})
        serializer = AlunoModelSerializer(instance=db_aluno, data={}, partial=True)
        serializer.is_valid(raise_exception=True)
        db_aluno.delete()
        return Response({'sucesso':'O registro foi deletado com sucesso'})
       
class AlunoModelViewSet(viewsets.ModelViewSet):
    serializer_class = AlunoModelSerializer
    queryset = AlunoModel.objects.all()
    

    

class CategoriaProdutoViewSet(ViewSet):

    serializer_class = CategoriaProdutoSerializer

    def list(self,request):
        db_categoria = CategoriaProdutoModel.objects.all()
        serializer = CategoriaProdutoSerializer(instance=db_categoria, many=True)
        return Response(serializer.data)
    

    def create(self, request):
        db_categoria = CategoriaProdutoModel.objects.all()
        serializer = CategoriaProdutoSerializer(instance=db_categoria, many=True)
        serializer.is_valid(raise_exception=True)
        categoria = serializer.validated_data['categoria']
        create = CategoriaProdutoModel.objects.create(categoria=categoria)
        dado = {'categoria': create.categoria}
        return Response(dado)

    
    def update(self, request, pk=None):

        # Obtenha o objeto existente pelo ID (pk)        
        try:
            categoria = CategoriaProdutoModel.objects.get(pk=pk)
        except CategoriaProdutoModel.DoesNotExist:
            return Response({'error': 'Categoria não encontrada'})

        # Serialize os dados da solicitação para atualização
        serializer = CategoriaProdutoSerializer(categoria, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Responda com os dados atualizados
        return Response(serializer.data)

    # def update(self, request, *args, **kwargs):
    #     # Recupere a instância do objeto existente pelo ID (pk)
    #     instance = self.get_object()

    #     # Serialize os dados da solicitação para atualização
    #     serializer = self.get_serializer(instance, data=request.data,)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    
    