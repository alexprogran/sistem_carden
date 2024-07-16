from decimal import Decimal
from datetime import date
from django.db.models import Sum
from django.db import transaction
import datetime
from .models import  (
CategoriaProdutoModel,DebitoModel, DebitoModel, FuncionarioModel, HistoricoDebitoModel, EstoqueModel,
CadastrosVendaModel, ModelAluno, UnidModel
)
from django.urls import reverse        
from django.shortcuts import get_object_or_404, render, redirect
from .forms import (
AlunosForms, CadastroDebitoFormModel, CadastroVendaFormModel, CategoriaProdutoFormModel,
 CreateUnidModelForm,FuncionarioModelForm,EstoqueFomModel, UnidModelForm
)

from .funcs import Check

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.views.generic import View
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import DebitoModel  # Importe seu modelo aqui


    


def view_login(request):
    """
    A view checa e autentica o usuário para a utilização
    do Sistem Carden.
    
    """

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
            return redirect(reverse('cadastro:unidade'))  
    
    # Exiba o formulário para login.
    else:       
        form_login = AuthenticationForm()

    return render(request, 'login.html', {'form_login': form_login})


@login_required
def create_unid(request):
    """ 
    A view realiza o cadastro da unidade do usuario

    É necessário que o usuário esteja autenticado para acessar esta view.

    """
   
    # Indentificando o usuário.
    user = request.session['usuario_logado']
    
    # Formulário de cadatro.
    unid_form = CreateUnidModelForm(usuario=user)  
    contexto = {'unid_form':unid_form, 'usuario': user}

    if request.method == 'POST':
        
        unid_form = CreateUnidModelForm(request.POST, usuario=user)  
        if  unid_form.is_valid(): 
            unid = unid_form.cleaned_data['unidade']
            
            # refereciando o usuário a unidade criada 
            request.session['unidade'] = unid
            cadast_unidade = UnidModel(
                usuario = user,
                unidade = unid
            )   
            cadast_unidade.save()

            return redirect(reverse('cadastro:home-carden'))
                    
        # "Ativando a valdação.
        else:
            contexto = {'unid_form':unid_form}

    return render(request, 'create_unid.html', contexto)


@login_required
def view_unid(request):
    """ 
    A view define a unidade do usuário logado: 
        * exibe o fomulário para a indetificação da unidade,

        * implementando na sessão a unidade do usuário,

        * realiza uma chacagem de primeiro acesso 
        
        * e exibe informes para criação de unidade.
    
    É necessário que o usuário esteja autenticado para acessar esta view.

    """
    # Definindo o usuário
    user = request.session['usuario_logado']
   

    # Formulário de pesquisa.
    unid_form = UnidModelForm(request.POST or None, usuario=user)    
    contexto = {'unid_form': unid_form, 'usuario': user}

    # Caso não tenha unidade cadastrada.
    if UnidModel.objects.filter(usuario=user).count() <= 0:
        contexto['unidade_zerada'] = True 
    
    if unid_form.is_valid():
        unidade = unid_form.cleaned_data['unidade']
        request.session['unidade'] = unidade
        contexto['sucesso'] = True
        return redirect(reverse('cadastro:home-carden'))
    return render(request, 'unidade.html',contexto)

      
@login_required
def view_cadastro_estoque(request):

    """ 
    A view cadastra o produto no estoque: 
        * exibe o fomulário para cadastro dos dados

        * e salva o registro no banco de dados.
    
    É necessário que o usuário esteja autenticado para acessar esta view
     e informe uma unidade correlacionada.

    """

    # Resgate do usuário e  unidade
    user = request.session['usuario_logado']
    unid = request.session['unidade']

    # Formulário de cadastro do produto
    estoque_form = EstoqueFomModel(usuario=user, unidade=unid)
    contexto ={'estoque_form':estoque_form, 'usuario': user, 'unidade': unid}

    # Caso não tenha categoria cadastrada.
    if CategoriaProdutoModel.objects.filter(usuario=user, unidade=unid).count() <= 0:
        contexto['categoria_zerada'] = True
    
    
    if request.method == 'POST':
       
        estoque_form = EstoqueFomModel(request.POST, usuario=user, unidade=unid)      
    
        if estoque_form.is_valid():
           
             
            form_produto = estoque_form.cleaned_data['produto'] 
            db_estoque = EstoqueModel()   
            form_codigo = db_estoque.gerador_de_codigo()
            form_quantidade = estoque_form.cleaned_data['quantidade']
            form_preco_custo = estoque_form.cleaned_data['preco_custo'] 
            form_total_custo = form_quantidade * form_preco_custo
            form_preco_varejo = estoque_form.cleaned_data['preco_varejo'] 
            form_total_varejo = form_quantidade * form_preco_varejo 
            form_categoria = estoque_form.cleaned_data['categoria'] 
            
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
            
            )
            cadastro_estoque.save()
            contexto = {           
                'sucesso':True,
            
            }      
        
        else:
            contexto ={'estoque_form':estoque_form, 'usuario': user, 'unidade': unid}


    return render(request,'cadast_estoque.html',contexto)


@login_required
def view_cadastro_funcionario(request):
    """ 
        A view realiza o cadastro do funcionário: 
            * exibe o fomulário para cadastro dos dados

            * e salva o registro no banco de dados.
        
        É necessário que o usuário esteja autenticado para acessar esta view
        e informe uma unidade correlacionada.

    """

    # Resgate do usuário e  unidade
    user = request.session['usuario_logado']
    unid = request.session['unidade']

    # Fomulário para cadastro do funcionário.
    funcionario_form = FuncionarioModelForm(request.POST or None,
    usuario=user,unidade=unid)
    contexto = {'funcionario_form':funcionario_form,
    'usuario': user, 'unidade': unid}
    if funcionario_form.is_valid():
        telefone_form = funcionario_form.cleaned_data['telefone']
        funcionario_form = funcionario_form.cleaned_data['funcionario']        

        cadastrar = FuncionarioModel(
            usuario=user,
            unidade=unid,
            funcionario=funcionario_form,
            telefone=telefone_form,        
            )
        cadastrar.save()
        contexto['sucesso'] = True
    else:

        contexto = {
            'funcionario_form':funcionario_form,
            'usuario': user, 'unidade': unid,
            }


    return render(request,'cadast_funcionario.html',contexto) 


@login_required
def view_home_carden(request):
    """
    Esta view esta relacionada com
    a visualização das opções de navegações do Sistem Carden.

    É necessário que o usuário esteja autenticado para acessar esta view.

    """
    # Resgatando usuário e unidade.
    user = request.session['usuario_logado']
    unid = request.session['unidade']

    return render(request,'home_carden.html',{'usuario':user, 'unidade': unid})


@login_required                                             
def view_cadastro_aluno(request):
    """
    View para cadastrar um novo aluno.
    
    *É necessário que o usuário esteja autenticado para acessar esta view
     e informe uma unidade correlacionada.

    """

    # Identificando usuário e unidade
    user = request.session['usuario_logado']
    unid = request.session['unidade']

    if request.method == 'POST':
        aluno_form = AlunosForms(request.POST,usuario=user, unidade=unid)
        if aluno_form.is_valid():            
            # Se o formulário for válido, processar os dados
            nome_form = aluno_form.cleaned_data['nome']
            turma_form = aluno_form.cleaned_data['turma']
            responsavel_form = aluno_form.cleaned_data['responsavel']
            telefone_responsavel_form = aluno_form.cleaned_data['telefone_responsavel']
                         
            
            db_aluno = ModelAluno(
                usuario=user,
                unidade=unid,
                nome=nome_form,
                turma=turma_form,
                responsavel=responsavel_form,
                tel_responsavel=telefone_responsavel_form
            )
            db_aluno.save()
            contexto = {
                'sucesso': True,
                'aluno': nome_form,
            }
        # Ativando validações.    
        else:
            contexto = {'aluno_form': aluno_form, 'unidade': unid}

    else:
        # Formulário para cadastro.
        aluno_form = AlunosForms(usuario=user, unidade=unid)
        contexto = {'aluno_form': aluno_form, 'unidade': unid}

    return render(request, 'cadast_aluno.html', contexto)


@login_required  
def view_cadastro(request):
    """ 
        A view exibe a vizualização das opções de cadastros do 
        sistama.

        É necessário que o usuário esteja autenticado para acessar esta view
        e informe uma unidade correlacionada.

    """

    user = request.session['usuario_logado'] 
    unid = request.session['unidade']      
            
    return render(request,'cadastro.html',{'usuario':user, 'unidade': unid}) 



@login_required
def view_cadastro_debito(request):
    """ 
        A view realiza o cadastro de valores em aberto dos alunos: 
            * exibe o fomulário para cadastramento do débito 

            * e salva o registro na base de dados.
        
        É necessário que o usuário esteja autenticado para acessar esta view
        e informe uma unidade correlacionada.

    """

    # Resgatando o usuário e unidade.
    user = request.session['usuario_logado']
    unid = request.session['unidade']

    formulario_debito = CadastroDebitoFormModel(usuario=user, unidade=unid)
    contexto = {'formulario_debito':formulario_debito,'usuario': user,
    'unidade': unid}
        
        # Caso não tenha cadastro de alunos na base de dados.
    if ModelAluno.objects.filter(usuario=user, unidade=unid).count() <= 0:
        contexto['sem_cadastro'] = True

    # Caso não tenha cadastro de produtos na base de dados de estoque .
    elif EstoqueModel.objects.filter(usuario=user, unidade=unid).count() <= 0:
       contexto['produto_zerado'] =True

    # Caso não tenha registro de categoria na base de dados de categoria.   
    elif CategoriaProdutoModel.objects.filter(usuario=user, unidade=unid).count() <= 0:
        contexto['categoria_zerada'] = True

    elif request.method == 'POST':
        formulario_debito = CadastroDebitoFormModel(request.POST,usuario=user, unidade=unid)
        

        if formulario_debito.is_valid():
            # Entrandas:
            aluno_form =  formulario_debito.cleaned_data['aluno']
            produto_form = formulario_debito.cleaned_data['produto']
            quantidade_form = formulario_debito.cleaned_data['quantidade']        
            data_form = formulario_debito.cleaned_data['data']

            # Instância do produto no estoque.
            tabela_estoque = EstoqueModel.objects.get(
            unidade=unid,usuario=user,produto=produto_form)
            valor_unitario=tabela_estoque.preco_varejo,        
            
            tabela_debito = DebitoModel() 
            # Registrando os débitos no modelo DebitoModel.           
            protol_criate = tabela_debito.gerentec(unid, user, aluno_form, produto_form,
            quantidade_form, data_form, valor_unitario[0])
            soma_total = DebitoModel.objects.aggregate(soma=Sum('valor_total'))['soma']
            
            # Criando um histórico do registro.
            # historico_debito_model = HistoricoDebitoModel(
            #     usuario=user,
            #     unidade=unid,
            #     aluno=formulario_debito.cleaned_data['aluno'],
            #     produto=formulario_debito.cleaned_data['produto'], 
            #     valor=tabela_estoque.preco_varejo,            
            #     data=data_form         
            #    )         
            # historico_debito_model.save()
            contexto = {            
                'sucesso':True,
                'soma_total':soma_total
            }
        # Ativando validações.
        else:
              contexto = {'formulario_debito':formulario_debito,'usuario': user,
            'unidade': unid,} 
    return render(request,'cadast_debito.html',contexto)


@login_required
def view_cadastro_vendas(request):
    """ 
    A view realizar o cadastro da venda: 
        * exibe o fomulário para cadastro dos dados

        * e salva o registro no banco de dados.
    
    É necessário que o usuário esteja autenticado para acessar esta view
     e informe uma unidade correlacionada.

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

     # Caso não tenha produto cadastrado.
    if EstoqueModel.objects.filter(usuario=user).count() <= 0:
        contexto['produto_zerado'] = True
    
        
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

    """
    View realiza o cadastro de categoria para o produto.
    
    *É necessário que o usuário esteja autenticado para acessar esta view
     e informe uma unidade correlacionada.

    """

    # Resgatando usuário e unidade.
    user = request.session['usuario_logado']
    unid = request.session['unidade']

    # Fomulário para cadastro de produto.
    categoria_form = CategoriaProdutoFormModel(request.POST or None,
    usuario=user, unidade=unid)
    contexto = {'categoria_form':categoria_form, 'usuario': user,'unidade':unid}
    if categoria_form.is_valid():
        
        categore = categoria_form.cleaned_data['categoria']

        create_categoria = CategoriaProdutoModel(
            
            usuario=user,
            unidade=unid,
            categoria = categore

        )
        
        create_categoria.save()
        contexto = {
            # 'usuario': user,
            'sucesso':True,
        }   
  
    return render(request,'categoria_produto.html',contexto)




def view_cadastro_usuario(request):
    
    """ A view realizar o cadastro do usuário."""

    contexto = {'sucesso': False}
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # Campo oculto na templete('form_cadast_user') para indetificar o formulário
        if form_type == 'form_cadast_user': 
          
            form_cadast_user = UserCreationForm(request.POST)
            if form_cadast_user.is_valid():
                form_cadast_user.save()
                form_login = AuthenticationForm()  # Cria um novo formulário de login
                contexto = {'sucesso': True, 'formulario_login': form_login}
            else:
                contexto = {'form_cadast_user': form_cadast_user}
                
        # Campo oculto na templete("form_login") para indetificar o formulário
        elif form_type == "form_login":           
            
            form_login = AuthenticationForm(request, data=request.POST)
            if form_login.is_valid():
                username = form_login.cleaned_data['username']
                password = form_login.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    request.session['usuario_logado'] = user.username            
                    return redirect(reverse('cadastro:unidade'))
            else:
                 contexto = {'sucesso': True, 'formulario_login': form_login}
    
    
    else: # Fomulário de cadastro de usuário

        form_cadast_user = UserCreationForm(request.POST or None) 
        print('Rederizando o formulário de inscrição do usuário')       
        contexto = {'form_cadast_user': form_cadast_user}

    return render(request, 'cadast_user.html', contexto)


















