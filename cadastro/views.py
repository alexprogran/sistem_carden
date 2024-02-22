from decimal import Decimal
from datetime import date
from django.db.models import Sum
from django.db import transaction
import datetime
from cadastro.models import  (
AlunoModel, CategoriaProdutoModel,DebitoModel, DebitoModel, HistoricoDebitoModel, EstoqueModel,
CadastrosVendaModel, UnidModel
)
from django.urls import reverse        
from django.shortcuts import get_object_or_404, render, redirect
from cadastro.forms import (
AlunoForms, CadastroDebitoFormModel, CadastroVendaFormModel, CategoriaProdutoFormModel,
 CreateUnidModelForm,FormTesteEstoque,FuncionarioModelForm,EstoqueFomModel, UnidModelForm
)
from cadastro.models import TesteEstoqueModel
from .funcs import Check

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def view_login(request):
    if request.method == 'POST':
        form_login = AuthenticationForm(request, request.POST)
        if form_login.is_valid():
            # Autenticar o usuário
            username = form_login.cleaned_data['username']
            password = form_login.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Login bem-sucedido
                login(request, user)
                request.session['usuario_logado'] = user.username
                return redirect(reverse('cadastro:unidade'))  # Redirecione para a página desejada após o login
    else:
        form_login = AuthenticationForm()

    return render(request, 'login.html', {'form_login': form_login})


@login_required
def create_unid(request):
    """A view create_unid cria a(as) unidade(s) referentes à cada usuário"""
   
    # indentificando o usuário
    user = request.session['usuario_logado']

    unid_form = CreateUnidModelForm(usuario=user)  
    contexto = {'unid_form':unid_form}

    if request.method == 'POST':
        
        unid_form = CreateUnidModelForm(request.POST, usuario=user)  
        if  unid_form.is_valid(): 
            unid = unid_form.cleaned_data['unidade']
            request.session['unidade'] = unid
            cadast_unidade = UnidModel(
                usuario = user,
                unidade = unid
            )
            if UnidModel.objects.filter(usuario=user, unidade=unid).exists():
                contexto = {'unid_invalid': True,'unidade': unid}                

            else:
                cadast_unidade.save()
                contexto = {
                    
                    'sucesso': True,
                    
                    }         
    # else:   

    #     unid_form = CreateUnidModelForm()
    #     contexto = {
    #         'unid_form': unid_form,
    #         'usuario': request.session['usuario_logado'],

    #                 }

    return render(request, 'create_unid.html', contexto)


@login_required
def view_unid(request):
    user = request.session['usuario_logado']
    unid_form = UnidModelForm(request.POST or None)
    contexto = {'unid_form': unid_form, 'usuario': user}
    if unid_form.is_valid():
        unidade = unid_form.cleaned_data['unidade']
        request.session['unidade'] = unidade
        contexto['sucesso'] = True
        return redirect(reverse('cadastro:home-carden'))
    return render(request, 'unidade.html',contexto)

      
@login_required
def view_cadastro_estoque(request):

    """ A view_cadastro_estoque é responsável por cadastrar 
    o produto no estoque em função do usuário e unidade.  """

    # Rescate do usuário e  unidade
    user = request.session['usuario_logado']
    unid = request.session['unidade']

    # Formulário de cadastro do produto
    estoque_form = EstoqueFomModel(usuario=user, unidade=unid)
    contexto ={'estoque_form':estoque_form, 'usuario': user, 'unidade': unid}
    
    db_estoque = EstoqueModel()
    if request.method == 'POST':
       
        estoque_form = EstoqueFomModel(request.POST, usuario=user, unidade=unid)      
    
        if estoque_form.is_valid():
            # Campos formulario
            # user = request.session['usuario_logado']
            # unid = request.session['unidade']
            form_produto = estoque_form.cleaned_data['produto']    
            form_codigo = db_estoque.gerador_de_codigo()
            form_quantidade = estoque_form.cleaned_data['quantidade']
            form_preco_custo = estoque_form.cleaned_data['preco_custo'] 
            form_total_custo = form_quantidade * form_preco_custo
            form_preco_varejo = estoque_form.cleaned_data['preco_varejo'] 
            form_total_varejo = form_quantidade * form_preco_varejo 
            form_categoria = estoque_form.cleaned_data['categoria'] 
            print('Saida do formulário:',form_categoria)
            cadastro_estoque = EstoqueModel(
                usuario = user,
                unidade = unid,
                produto=form_produto,
                codigo=form_codigo,
                quantidade=form_quantidade,
                preco_custo=form_preco_custo,
                total_custo=form_total_custo,
                preco_varejo=form_preco_varejo,
                total_varejo=form_total_varejo,
                categoria= form_categoria
            #     CategoriaProdutoModel.objects.filter(
            #     id=form_categoria, usuario=user, unidade=unid).values_list('categoria',flat=True)
            )
            cadastro_estoque.save()
            contexto ={           
                'sucesso':True,
            
            }      
        
    return render(request,'cadast_estoque.html',contexto)



def view_cadastro_funcionario(request):
    funcionario_form = FuncionarioModelForm(request.POST or None)
    contexto = {'funcionario_form':funcionario_form}
    if funcionario_form.is_valid():
        funcionario_form.save()
        contexto['sucesso'] = True 
    return render(request,'cadast_funcionario.html',contexto) 


@login_required
def view_home_carden(request):
    user = request.session['usuario_logado']
    unid = request.session['unidade']
    return render(request,'home_carden.html',{'usuario':user, 'unidade': unid})


@login_required                                             
def view_cadastro_aluno(request):
    # Indentificando usuáiro e unidade
    user = request.session['usuario_logado']
    unid = request.session['unidade']

    # passando para o formulário  o usuário e  a unidade
    aluno_form = AlunoForms(usuario=user, unidade=unid)
    contexto = {'aluno_form':aluno_form,'unidade': unid,}    
     
    if request.method == 'POST':
        aluno_form = AlunoForms(request.POST, usuario=user, unidade=unid)
        if aluno_form.is_valid():            
                      
            nome_form = aluno_form.cleaned_data['nome']
            turma_form = aluno_form.cleaned_data['turma']
            responsavel_form = aluno_form.cleaned_data['responsavel']
            telefone_responsavel_form = aluno_form.cleaned_data['telefone_responsavel']
                         
            # Checando a existência do registro no banco de dados
            exist_aluno = AlunoModel().exist_aluno(user, unid, nome_form) 
            if not exist_aluno:
                contexto = {'not_exist': True, 'nome_form': nome_form}

            else:
            
                db_aluno = AlunoModel(
                    usuario=user,
                    unidade=unid,
                    nome=nome_form,
                    turma=turma_form,
                    responsavel=responsavel_form,
                    telefone_responsavel=telefone_responsavel_form
                )
                db_aluno.save()
                contexto = {
                    
                    
                    'sucesso': True,
                    'aluno': nome_form,
                }
       
    return render(request, 'cadast_aluno.html', contexto)


@login_required  
def view_cadastro(request):
    user = request.session['usuario_logado'] 
    unid = request.session['unidade']      
            
    return render(request,'cadastro.html',{'usuario':user, 'unidade': unid}) 



@login_required
def view_cadastro_debito(request):

    user = request.session['usuario_logado']
    unid = request.session['unidade']

    formulario_debito = CadastroDebitoFormModel(usuario=user, unidade=unid)
    contexto = {'formulario_debito':formulario_debito,'usuario': user,
            'unidade': unid,}
    
    if request.method == 'POST':
        formulario_debito = CadastroDebitoFormModel(request.POST,usuario=user, unidade=unid)
        

        if formulario_debito.is_valid():
            
            # Entrandas:
            aluno_form =  formulario_debito.cleaned_data['aluno']
            produto_form = formulario_debito.cleaned_data['produto']
            quantidade_form = formulario_debito.cleaned_data['quantidade']        
            data_form = formulario_debito.cleaned_data['data']
            tabela_estoque = EstoqueModel.objects.get(
            unidade=unid,usuario=user,produto=produto_form)
            valor_unitario=tabela_estoque.preco_varejo,        
            tabela_debito = DebitoModel()
            gerenciador = tabela_debito.gerentec(unid, user, aluno_form, produto_form,
            quantidade_form, data_form, valor_unitario[0])
            soma_total = DebitoModel.objects.aggregate(soma=Sum('valor_total'))['soma']
            # historico_debito_model = HistoricoDebitoModel(
            #     aluno=formulario_debito.cleaned_data['aluno'],
            #     produto=formulario_debito.cleaned_data['produto'],  
            #     valor=tabela_estoque.preco_varejo,            
            #     data=date.today()          
            #    )         
            # historico_debito_model.save()
            contexto = {            
                'sucesso':True,
                'soma_total':soma_total
            }
           
    return render(request,'cadast_debito.html',contexto)


@login_required
def view_cadastro_vendas(request):
    """ A view_cadastro_vendas esta relacionada com a visualização do formulario 
    de cadastro de vendas e contém a lógica para salvar os dados no modelo 
    Cadastro_venda_Model.
    """
    # Resgatando o usuário e a unidade
    user = request.session['usuario_logado']
    unid = request.session['unidade']

   # Definido a data
    today = datetime.date.today()
    
    # formulário de cadastro de vendas
    vendas_form = CadastroVendaFormModel(request.POST or None,
    usuario=user, unidade=unid)
    contexto = {'vendas_form':vendas_form, 'usuario': user, 'unidade':unid}
    
        
    if vendas_form.is_valid():    
    
        produto_form = vendas_form.cleaned_data['produto']
        quantidade = vendas_form.cleaned_data['quantidade']
             

        # resgatando o valor unitário  do produto.          
        produto_estoque = EstoqueModel.objects.get(usuario=user,
        unidade=unid, produto=produto_form)
        valor_unidade = produto_estoque.preco_varejo 
        
        # Ou o registro ou atualizamos da quantidade e do valor total, ao criterio do "gerentec". 
        cadastro_vendas = CadastrosVendaModel()            
        cadastro = cadastro_vendas.gerentec(user, unid,produto_form,quantidade,today,valor_unidade) 
        contexto = cadastro
    
    
       
    return render(request,'cadastro_vendas.html',contexto)



@login_required
def view_categoria_produto(request):
    user = request.session['usuario_logado']
    unidade = request.session['unidade']
    categoria_form = CategoriaProdutoFormModel(request.POST or None)
    contexto = {'categoria_form':categoria_form, 'usuario': user,}

    if categoria_form.is_valid():
        
        categore = categoria_form.cleaned_data['categoria']

        create_categoria = CategoriaProdutoModel(
            
            usuario=user,
            unidade=unidade,
            categoria = categore

        )
        
        create_categoria.save()
        contexto = {
            # 'usuario': user,
            'sucesso':True,
        }
  
    return render(request,'categoria_produto.html',contexto)



def view_cadastro_usuario(request):
    form_cadast_user = UserCreationForm(request.POST or None)
    contexto = {'form_login': form_cadast_user}
    if form_cadast_user.is_valid():
        form_cadast_user.save()
        contexto['sucesso'] = True
    
    return render(request,'cadast_user.html',contexto)


@login_required
def view_cadastro_teste_produto(request):

    
    formulario =FormTesteEstoque(request.POST or None)
    contexto = {'formulario': formulario}
    nome_user = request.session['usuario_logado']
    unid = request.session['unidade']
    if formulario.is_valid():
        produto = formulario.cleaned_data['produto']
        quantidade = formulario.cleaned_data['quantidade']
        valor = formulario.cleaned_data['valor']
        
        # Criando a ação para o usuário logado
        db_teste_estoque_model = TesteEstoqueModel(
            usuario = nome_user, unidade=unid, produto=produto,quantidade=quantidade,valor=valor
        )

        db_teste_estoque_model.save()

        contexto['sucesso'] = True 
    
    return render(request,'testando_produto.html',contexto)
    

@login_required
def lista_teste_produto(request):
    usuario = request.session['usuario_logado']
    unid = request.session['unidade']
    lista = TesteEstoqueModel.objects.filter(usuario=usuario,unidade=unid).values()
    print(lista)
    contexto = {
        'unid': unid,
        'usuario': usuario,
        'listagem': True,
        'lista':lista,

    }
    return render(request, 'testando_produto.html',contexto)
















