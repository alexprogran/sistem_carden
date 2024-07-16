import json
from django.http import HttpResponse,HttpRequest
from rest_framework.request import Request

from rest_framework.viewsets import ViewSet, ModelViewSet

from django.shortcuts import render
from cadastro.models import AlunoModel, CategoriaProdutoModel, DebitoModel, FuncionarioModel
from rest_framework.decorators import api_view,action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from api.serializer import (AlunoModelSerializer, CategoriaProdutoSerializer,
 CategoriaProdutoModelSerializer, DebAlunoModelSerializer, DebitoSerializer,
FuniconarioModelSeiralzer)


from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

@api_view(http_method_names=['GET', 'POST'])
def sum_deb(request):
    # Inicializando variáveis
    dados = []
    data = []
   
    # Obtendo todos os débitos e agrupando por data
    debitos = DebitoModel.objects.all()
    current_date = None
    valor_total = 0

    for deb in debitos:  

        if len(dados)> 0:
            if deb.data in data:
                    dat = deb.data.strftime("%d/%m/%Y")
                    print('Chave:',dados[dat])

        # 
           
            # list_data = [list(data.values())[0] for data in dados]
            # list_data = [data for data in dados]
            # print('list_date:',list_data)           
            # for dat in dados:
            #     data_lista = dict(dat)
            #     print('Data do banco de dados',deb.data)
            #     print('Data da lista cosntruida:', list(data_lista.keys()))           
                
            #     if str(deb.data) == str(list(dat.keys())[0]):
            #         print('Igual')
                
       

        if deb.data != current_date:

            if current_date is not None:
                # Adiciona o total da data anterior à lista de dados
                dados.append({'data': current_date, 'valor_total': valor_total})
                data.append(deb.data) #--> compondo a lista de datas               
                
            # Atualiza a data atual e reinicializa o valor total
            current_date = deb.data
            valor_total = deb.valor_total # --> atualização do valor_total
        else:
            # Soma o valor ao total acumulado para a data atual
            valor_total += deb.valor_total

    # Adiciona o último total acumulado à lista de dados
    if current_date is not None:
        dados.append({'data': current_date, 'valor_total': valor_total})  
    print(len(dados))
    
    # Retornando os dados acumulados por data em uma resposta JSON
    return Response(dados)

            
# sem utilizar o rest-framework
# def view_api_testes_(request):
def lista_categoria_(request):
    instence_estoque = CategoriaProdutoModel.objects.all()
    dados = []
    for categoria in instence_estoque:
        dado = {'categoria':categoria.categoria}
        dados.append(dado)
    print(dados)   
    return HttpResponse(json.dumps(dados))



# com a utilização da rest-framework
@api_view()
def lista_categoria_(request):

    instence_estoque = CategoriaProdutoModel.objects.all()
    dados = []
    for categoria in instence_estoque:
        dado = {'categoria':categoria.categoria,
                'unidade': categoria.unidade,
                'usuario': categoria.usuario,
                }
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
    # serializer = CategoriaProdutoSerializer(data=request.data)
    serializer = CategoriaProdutoModelSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):

        categoria = serializer.validated_data['categoria']
        user = serializer.validated_data['usuario']
        unid = serializer.validated_data['unidade']
        create = CategoriaProdutoModel.objects.create(categoria=categoria,usuario=user,unidade=unid)        
        dados = []
        dado = {'categoria':create.categoria,'unidade': create.unidade, 'usuario': create.usuario}
        dados.append(dado)
        
        return Response(dados)
    

# usando o "serializer.ModelSerializer"
@api_view(http_method_names=['GET','POST'])
def lista_categoria(request):

    db_categoria = CategoriaProdutoModel.objects.all()
    serializer = CategoriaProdutoModelSerializer(instance=db_categoria, many=True)
    
    return Response(serializer.data)

@api_view()
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
    


    
       
class AlunoModelViewSet(ModelViewSet):
    serializer_class = AlunoModelSerializer
    queryset = AlunoModel.objects.all()
    

    

# class CategoriaProdutoViewSet(ViewSet):

#     serializer_class = CategoriaProdutoSerializer

#     def list(self,request):
#         db_categoria = CategoriaProdutoModel.objects.all()
#         serializer = CategoriaProdutoSerializer(instance=db_categoria, many=True)
#         return Response(serializer.data)
    

#     def create(self, request):
       
#         serializer = CategoriaProdutoSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         categoria = serializer.validated_data['categoria']
#         user = serializer.validated_data['usuario']
#         unid = serializer.validated_data['unidade']
#         create = CategoriaProdutoModel.objects.create(categoria=categoria, unidade=unid, usuario=user)
       
#         return Response(serializer.data)

class CategoriaProdutoModelViewSet(ModelViewSet):
    serializer_class = CategoriaProdutoModelSerializer
    # queryset = CategoriaProdutoModel.objects.all()

    def get_queryset(self):
        return super().get_queryset()

    # def get_queryset(self):
    #     return CategoriaProdutoModel.objects.all()
    
    def perform_create(self, serializer):
        # Se o usuário estiver autenticado o objeto criado terá uma referência ao usário que o cirou.
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.seva()


# class CategoriaProdutoViewSet(ViewSet):  
     
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
    
    

class DebitoVeiwSet(ViewSet):
        
        
        def list(self, request):

            dados = []
            # Obtendo todos os débitos e agrupando por data
            debitos = DebitoModel.objects.all()
            current_date = None
            valor_total = 0

            for deb in debitos:
                if deb.data != current_date:
                    if current_date is not None:
                        # Adiciona o total da data anterior à lista de dados
                        dados.append({'data': current_date, 'valor_total': valor_total})
                    
                    # Atualiza a data atual e reinicializa o valor total
                    current_date = deb.data
                    valor_total = deb.valor_total
                else:
                    # Soma o valor ao total acumulado para a data atual
                    valor_total += deb.valor_total

            # Adiciona o último total acumulado à lista de dados
            if current_date is not None:
                dados.append({'data': current_date, 'valor_total': valor_total})

            serializer = DebitoSerializer(dados, many=True)
            return Response(serializer.data)



class DebAlunoModoViewSet(ModelViewSet):
    serializer_class = DebAlunoModelSerializer
    queryset = DebitoModel.objects.all()


class FuncionarioModelVeiwSet(ModelViewSet):
    # personalizar url--> path("api-uath/",include('rest_framework.urls'))
        # importar a classe IsAuthenticated
        # implementar a classe na view
    permission_classes = [IsAuthenticated]

    serializer_class = FuniconarioModelSeiralzer
    # queryset = FuncionarioModel.objects.all()

    def get_queryset(self):
        return FuncionarioModel.objects.all()
    
    def perform_create(self, serializer):

        if self.request.user.is_authenticated:
            serializer.save(criado_por=self.request.user) #--> usuário logado.
        else:
            serializer.save()