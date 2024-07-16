from django.shortcuts import redirect
from django.core.paginator import Paginator
import datetime
from decimal import Decimal
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse
from cadastro.forms import CadastroDebitoFormModel
from cadastro.models import AlunoModel, CadastrosVendaModel, DebitoModel, EstoqueModel, HistoricoDebitoModel, ModelAluno
from .forms import PesquisaAlunoForm, PesquisaDebitoAlunoForm, PesquisaVendaDataForm
from django.contrib.auth.decorators import login_required


@login_required
def view_lista_debito(request):
    """
    Esta view é responsável pela visualização da      
    listagem geral de débito dos aluno.

    É necessário que o usuário esteja autenticado para acessar esta view
    e informe uma unidade correlacionada.

    """

    # Indentificando usuário e unidade
    user = request.session['usuario_logado']
    unid = request.session['unidade']

    list_deb = DebitoModel.objects.filter(usuario=user,
    unidade=unid,status='pendente').order_by('aluno')
    total_debito = list_deb.aggregate(Sum('valor_total'))['valor_total__sum']    
    quant_debito =list_deb.count()    
    lista_debito = list_deb.order_by('aluno').values('aluno','produto','valor_unitario','quantidade','valor_total','data')
    
    paginator = Paginator(list_deb, 5 )
    num_pag = request.GET.get('page')
    if num_pag == None:
        num_pag = 1
    pag_obj = paginator.get_page(num_pag)    
    tol_pag = paginator.num_pages
 
    contexto = {
        'usuario':user,
        'unidade':unid,
        'total_debito':total_debito,
        'lista_debito':lista_debito,
        'quant_debito':quant_debito,
        'page_obj': pag_obj,
        'tol_pag': tol_pag,
        'num_pag': num_pag,
    }
   
    return render(request,'lista_debito.html',contexto)



@login_required
def view_pesquisa_debito_aluno(request):   
    """
    Esta view realiza a visualização do formulário para       
    de pesquisa de débito do aluno.

    É necessário que o usuário esteja autenticado para acesso da view
    e informe uma unidade correlacionada.
    """

    # Indentificando usuário e unidade
    user = request.session['usuario_logado']
    unid = request.session['unidade']

    # Formulário de pesquisa
    formulario =PesquisaDebitoAlunoForm(request.POST or None,
    usuario=user, unidade=unid)
    contexto = {'formulario':formulario,'usuario': user, 'unidade': unid}
    
    if formulario.is_valid():


        estudante = formulario.cleaned_data['nome']

        request.session['aluno'] = estudante

        url = reverse('cadastro:result-deb-aluno',kwargs={'estudante': estudante})
        return redirect(url)      
      
    return render(request,'pesquisa_debito_aluno.html',contexto)


@login_required
def result_deb_aluno(request,estudante):
    """
    Esta view realiza a listagem do(s) débito(s) em aberto(s) do aluno.

    É necessário que o usuário esteja autenticado para acesso da view
    e informe uma unidade correlacionada.
    """
      # Indentificando usuário e unidade
    user = request.session['usuario_logado']
    unid = request.session['unidade']
     
    
    list_deb = DebitoModel.objects.filter(usuario= user, unidade=unid,
    aluno=estudante, status='pendente').order_by('data').values(
    'aluno','produto','valor_unitario','quantidade','valor_total','data'
        )
    valor_total =list_deb.aggregate(Sum('valor_total'))['valor_total__sum']
    quant_debito = list_deb.count()

    
    paginator = Paginator(list_deb, 5)
    num_pag = request.GET.get('page')
    pag_obj = paginator.get_page(num_pag)        
    tol_pag = paginator.num_pages
    if num_pag == None:
        num_pag = 1  

    contexto = {
            'usuario': user,
            'unidade': unid,
            'aluno':estudante,
            "list_debito_aluno": True,
            'valor_total':valor_total,
            'quant_debito': quant_debito,
            'pag_obj': pag_obj,
            'num_pag': num_pag,
            'tol_pag': tol_pag,      
        }       
    
    return render(request, 'pesquisa_debito_aluno.html', contexto)

def view_pdf(request):
    user = request.session['usuario_logado']
    unid = request.session['unidade']
    aluno = request.session['aluno']

    pdf = DebitoModel().gera_pdf(user,unid,aluno)
    # url = reverse('cadastro:lista-debito')
    return pdf

@login_required
def view_pesquisa(request):
    """
    Esta view é responsável pela visulaização das opções de navegação
    de listagem do Sistem Carden.
    """

    user = request.session['usuario_logado']
    unid = request.session['unidade']

    return render(request,'pesquisa.html',{'usuario':user, 'unidade': unid})


@login_required
def view_pesquisa_venda_data(request):
    """ 
    A  view realizamos a filtragem das vendas em função da data.

    *É necessário que o usuário esteja autenticado para acessar esta view e 

    indique uma unidade correlacionada.
    """

    #  Resgatando usuário e unidade    
    user = request.session['usuario_logado']
    unid = request.session['unidade']
   
        
    # Formulário de perquisa
    pesquisa_form = PesquisaVendaDataForm(request.POST or None)  
   
    contexto = {'pesq':True,'pesquisa_form': pesquisa_form ,'usuario': user,
        'unidade': unid,}
    
    if pesquisa_form.is_valid():
        dat_pesq = pesquisa_form.cleaned_data['data']
        
        url = reverse('cadastro:result-venda-data',kwargs={'dat_pesq': dat_pesq}) 
    
        return redirect(url) 
    
    return render(request,'pesquisa_venda_data.html',contexto)


@login_required
def result_vendas(request, dat_pesq):
     
    """ 
    A view exibe a lista de vendas referente a data da pesquisa.

    *É necessário que o usuário esteja autenticado para acessar esta view e 

    indique uma unidade correlacionada.
    """
    
    #  Resgatando usuário e unidade
    user = request.session['usuario_logado']
    unid = request.session['unidade']   

    lista_vendas = CadastrosVendaModel.objects.filter(usuario=user,
    unidade=unid, data=dat_pesq).values('produto','quantidade','valor_unitario',
    'valor_total','data').order_by('produto')


    soma_totais = lista_vendas.aggregate(
        valor_total=Sum('valor_total'),
        quantidade_total=Sum('quantidade'),
        )
    # Caso não exista registro de venda.
    if soma_totais['valor_total'] == None and soma_totais['quantidade_total'] == None:
        soma_totais['valor_total'] = 0.00
        soma_totais['quantidade_total'] = 0.00


    paginator = Paginator(lista_vendas, 5)
    
    number_page = request.GET.get('page')
    if number_page == None:
        number_page = 1   

    page_obj = paginator.get_page(number_page)

    tol_pag = paginator.num_pages

    contexto = {
        'usuario': user,
        'unidade': unid,       
        'valor_total': soma_totais['valor_total'],
        'quantidade_total': soma_totais['quantidade_total'],
        'pesquisa': True,
        'pag_obj': page_obj,
        'tol_pag': tol_pag,
        'page': number_page,


    }
    return render(request,'lista_vendas.html',contexto)




@login_required
def view_pesquisa_venda_entre_data(request):
    """ 
    - A view retorna o filtro entre os intervalos de data
    informadas pelo usuário.

    """        

    pesquisa_form = PesquisaVendaDataForm(request.POST or None)
    contexto = {'pesquisa_form': pesquisa_form}
    data_final = datetime.now()
    
    if pesquisa_form.is_valid():
        data_inicio = pesquisa_form.cleaned_data['data']
        query, quant_total, valor_total = CadastrosVendaModel.inter_data(data_inicio)

        contexto = {
            'query': query,
            'quant_total': quant_total,
            'valor_total': Decimal(valor_total),
            'pesquisa': True,
            'data_inicio': data_inicio,
            'data_final': data_final,

        }
       
    return render(request,'pesquisa_venda_entre_data.html',contexto)

@login_required
def view_lista_vendas(request):
    
    """ 
    A view realiza a listagem de vendas.

    *É necessário que o usuário esteja autenticado para acessar esta view e 

    indique uma unidade correlacionada.
    """
    
    #  Resgatando usuário e unidade
    user = request.session['usuario_logado']
    unid = request.session['unidade']   

    # Definindo data
    today = datetime.date.today()

    lista_vendas = CadastrosVendaModel.objects.filter(usuario=user,
    unidade=unid, data=today).values('produto','quantidade','valor_unitario',
    'valor_total','data').order_by('produto')
    

    soma_totais = lista_vendas.aggregate(
        valor_total=Sum('valor_total'),
        quantidade_total=Sum('quantidade'),
        )
    # Caso não exista registro de venda.
    if soma_totais['valor_total'] == None and soma_totais['quantidade_total'] == None:
        soma_totais['valor_total'] = 0.00
        soma_totais['quantidade_total'] = 0.00


    paginator = Paginator(lista_vendas, 5)
    
    num_page = request.GET.get('page')
    if num_page == None:
        num_page = 1

    page_obj = paginator.get_page(num_page)

    tol_page = paginator.num_pages

    contexto = {
        'usuario': user,
        'unidade': unid,
        'list_venda':True,       
        'valor_total': soma_totais['valor_total'],
        'quantidade_total': soma_totais['quantidade_total'],
         'page_obj': page_obj,
         'tol_pag':tol_page,
         'num_page': num_page,

    }
    return render(request,'lista_vendas.html',contexto)



@login_required
def view_lista_aluno(request):
    """ 
    A view realiza a listagem de alunos.

    *É necessário que o usuário esteja autenticado para acessar esta view e 

    indique uma unidade correlacionada.
    """
    # Resgatando usuário e unidade
    user = request.session['usuario_logado']
    unid = request.session['unidade']      

    #listamos os alunos pertecentes a unidade do usuário
    list_aluno = ModelAluno.objects.filter(usuario=user,
    unidade=unid).order_by('nome').values('nome','turma','responsavel',
    'tel_responsavel')
    quat_alunos = list_aluno.count()
    
    
    # Objeto paginator.
    paginator = Paginator(list_aluno, 5)

    # número da página.
    num_page = request.GET.get('page')
    if num_page == None:
        num_page = 1
    # página atual.
    page_atual = paginator.get_page(num_page)

    tol_pag = paginator.num_pages



    contexto = {
        
        'lista_aluno':True,
        'usuario': user,
        'unidade':unid,
        'page_obj': page_atual,  
        'tol_pag': tol_pag,
        'num_pag': num_page,
        'quat_alunos':quat_alunos,
        }
    
    return render(request,'lista_aluno.html',contexto )


@login_required       
def view_pesquisa_aluno(request):


   
    """ 
    View para pesquisa e recuperação de dados do aluno.
    
        - Através do nome passado ao formulário o aluno 
        
        é indentificado e os dados do registro recuperados.

    *É necessário que o usuário esteja autenticado para acessar esta view
     e informe uma unidade correlacionada.
    """

    # Resgatando usuário e unidade
    user = request.session['usuario_logado']
    unid = request.session['unidade'] 

    
    # Formulário para pesquisa
    pesquisa_aluno_form = PesquisaAlunoForm(usuario=user, unidade=unid)
    
    contexto = {
        'formulario_pesquisa':True,
        'usuario': user, 'unidade': unid,                
        'pesquisa_aluno_form':  pesquisa_aluno_form
        }    

        
    if request.method == 'POST':
        
        pesquisa_aluno_form = PesquisaAlunoForm(request.POST, 
        usuario=user, unidade=unid)
        if pesquisa_aluno_form.is_valid():
            aluno_form = pesquisa_aluno_form.cleaned_data['nome_aluno']

            # Pesquisando do aluno    
            resultado_pesquisa = ModelAluno.objects.filter(
            nome=aluno_form, usuario=user,unidade=unid).values(
            'nome','turma','responsavel','tel_responsavel')

            contexto = {
                'usuario': user,
                'unidade': unid,
                'resultado_pesquisa':resultado_pesquisa,
                'resultado':True,
            }               
        
            # "Levantando execação"
        else:
            
            contexto = {
            'formulario_pesquisa':True,
            'usuario': user, 'unidade': unid,                
            'pesquisa_aluno_form':  pesquisa_aluno_form    
            } 

          
            
    return render(request,'pesquisa_alunos.html',contexto)


def view_listar_estoque(request):
    """ 
    A view esta relacionada com a visualização da listagem do estoque.

    *É necessário que o usuário esteja autenticado para acessar esta view e 

    indique uma unidade correlacionada.
    """
    user = request.session['usuario_logado']
    unid = request.session['unidade']
    contexto = {'sucesso':False}
    lista_estoque = EstoqueModel.objects.filter(usuario=user, unidade=unid).order_by('produto').values(
        'produto','codigo','quantidade','preco_custo','total_custo','preco_varejo',
        'total_varejo','categoria')  # lista de dicionário contendo os campos e seus valores

    paginator = Paginator(lista_estoque, 5)   
    num_page = request.GET.get('page')
    if num_page == None:
        num_page = 1    
    page_atual = paginator.get_page(num_page) 
    tol_pag = paginator.num_pages  

    # Queryset
    quant_produtos = EstoqueModel.objects.filter(usuario=user, unidade=unid).values('produto').count()  # Contamos a quantidade de produtos.
    
    # Contém as chaves que guardam os valores dos resultantes da agregação.
    totais = EstoqueModel().sum_col(user, unid)
   
    contexto = {
        'usuario': user,
        'unid': unid,
        'itens_total': totais['itens_totais'],
        'total_custo': totais['custos_totais'],
        'total_varejo': totais['varejo_total'],
        'quantidade_produto': quant_produtos,      
        'page_obj': page_atual,
        'num_page': num_page,
        'tol_pag': tol_pag 
    }
    # Adicionando as chaves somente se houver registro no estoque.
    if EstoqueModel.objects.filter(usuario=user, unidade=unid).count() > 0:
        percent_total, lucro_total = EstoqueModel().percent_lucro(user, unid)
       
        contexto['percentual_lucro_total'] = percent_total
        contexto['total_lucro_liquido'] = lucro_total
       

    
    return render(request, 'lista_estoque.html', contexto)
