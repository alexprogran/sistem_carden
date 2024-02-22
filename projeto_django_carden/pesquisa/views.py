import datetime
from decimal import Decimal
from django.db.models import Sum
from django.shortcuts import render
from cadastro.forms import CadastroDebitoFormModel
from cadastro.models import AlunoModel, CadastrosVendaModel, DebitoModel, EstoqueModel, HistoricoDebitoModel
from pesquisa.forms import AlunoFormModl, EstoqueModelForm, PesquisaDebitoAlunoForm, PesquisaVendaDataForm
from django.contrib.auth.decorators import login_required


@login_required
def view_lista_debito(request):
    """
    Esta view é responsável pela visualização da      
    listagem geral de débito dos aluno, referentes
    ao usuário e unidade.
    """

    # Indentificando usuário e unidade
    user = request.session['usuario_logado']
    unid = request.session['unidade']

    total_debito =DebitoModel.objects.filter(usuario=user,
    unidade=unid).aggregate(Sum('valor_total'))['valor_total__sum']    
    quant_debito = DebitoModel.objects.filter(usuario=user,
    unidade=unid).count()    
    lista_debito = DebitoModel.objects.filter(usuario=user,
    unidade=unid).values('aluno','produto','valor_unitario','quantidade','valor_total','data')
   
    contexto = {
        'usuario':user,
        'unidade':unid,
        'total_debito':total_debito,
        'lista_debito':lista_debito,
        'quant_debito':quant_debito,
    }
   
    return render(request,'lista_debito.html',contexto)

@login_required
def view_pesquisa_debito_aluno(request):

    # Indentificando usuário e unidade
    """
    Esta view é responsável pela visualização da      
    listagem de débito do aluno.
    """
    
    user = request.session['usuario_logado']
    unid = request.session['unidade']

    # Formulário de pesquisa
    formulario =PesquisaDebitoAlunoForm(request.POST or None)
    contexto = {'formulario':formulario,'usuario': user, 'unidade': unid}
    
    if formulario.is_valid():
        aluno_form = formulario.cleaned_data['nome']
       
        valor_total = DebitoModel.objects.filter(usuario= user, unidade=unid,
        aluno=aluno_form).aggregate(Sum('valor_total'))['valor_total__sum']
        quant_debito = DebitoModel.objects.filter(usuario=user, unidade=unid,
        aluno=aluno_form).count()

        lista_debito = DebitoModel.objects.filter(usuario=user, unidade=unid,
        aluno=aluno_form).values(
            'aluno','produto','valor_unitario','quantidade','valor_total','data'
            )
        contexto = {
            'usuario': user,
            'unidade': unid,
            'aluno':aluno_form,
            "list_debito_aluno": True,
            'valor_total':valor_total,
            'quant_debito':quant_debito,
            'lista_debito':lista_debito, 
            # 'produto':lista_debito[0]['produto'],
            # 'valor':lista_debito[0]['valor_total']

        }
      
    return render(request,'pesquisa_debito_aluno.html',contexto)

def delete_lista_debito(request):
    nome_aluno = request.GET.get('nome')   
    lista_debito = request.GET.get('lista_debito')
  
   
    infor_debito =  DebitoModel.objects.filter(aluno=nome_aluno).values(
        'aluno','produto','data','quantidade','valor_unitario','valor_total'
        )
      
    contexto = {
        'sucesso':True,
        'aluno':nome_aluno,
        'infor_debito':infor_debito       
    }
    
    if infor_debito:
        infor_debito =  DebitoModel.objects.filter(aluno=nome_aluno)
        infor_debito.delete()
   
    return render(request,'delete_list.html',contexto)

@login_required
def view_pesquisa(request):

    user = request.session['usuario_logado']
    unid = request.session['unidade']

    return render(request,'pesquisa.html',{'usuario':user, 'unidade': unid})

@login_required
def view_pesquisa_venda_data(request):
    """ A vew_pesquisa_venda_data retorna um registro de venda da unidade 
    do usuário em função da data.
        """

    #  Resgatando usuário e unidade    
    user = request.session['usuario_logado']
    unid = request.session['unidade']   

    # Formulário de perquisa
    pesquisa_form = PesquisaVendaDataForm(request.POST or None)
    contexto = {'pesquisa_form': pesquisa_form ,'usuario': user,
            'unidade': unid,}
 
    if pesquisa_form.is_valid():
        data_pesquisa = pesquisa_form.cleaned_data['data']
     
        query_pesquisa, quantidade_total, valor_total  = CadastrosVendaModel.pesquisa_data(user, unid, data_pesquisa)       
           
        contexto = {
            'usuario': user,
            'unidade': unid,
            'query_pesquisa': query_pesquisa,
            'quantidade_total':quantidade_total,
            'valor_total': Decimal(valor_total),
            'pesquisa': True,

        }        

    return render(request,'pesquisa_venda_data.html',contexto)

def view_pesquisa_venda_entre_data(request):
    pesquisa_form = PesquisaVendaDataForm(request.POST or None)
    contexto = {'pesquisa_form': pesquisa_form}
    data_final = datetime.now()
    
    if pesquisa_form.is_valid():
        data_inicio = pesquisa_form.cleaned_data['data']
        query, quant_total, valor_total = CadastrosVendaModel.pesq_venda_inter_data(data_inicio)

        contexto = {
            'query': query,
            'quant_total': quant_total,
            'valor_total': Decimal(valor_total),
            'pesquisa': True,
            'data_inicio': data_inicio,
            'data_final': data_final,

        }
        print('quantidade total:',contexto['quant_total'])
    return render(request,'pesquisa_venda_entre_data.html',contexto)

@login_required
def view_lista_vendas(request):
    
    """ A "view_lista_vendas" trata da visualização da listagem das vendas
      referentes a unidade do usuário.
     """
    
    #  Resgatando usuário e unidade
    user = request.session['usuario_logado']
    unid = request.session['unidade']   

    # Definindo data
    today = datetime.date.today()

    lista_vendas = CadastrosVendaModel.objects.filter(usuario=user,
    unidade=unid, data=today).values('produto','quantidade','valor_unitario',
    'valor_total','data').order_by('data')
    soma_totais = CadastrosVendaModel.objects.aggregate(
        valor_total=Sum('valor_total'),
        quantidade_total=Sum('quantidade'),
        )
   
    contexto = {
        'usuario': user,
        'unidade': unid,
        'lista_vendas':lista_vendas,
        'valor_total': soma_totais['valor_total'],
        'quantidade_total': soma_totais['quantidade_total']

    }
    return render(request,'lista_vendas.html',contexto)

def view_listar_estoque(request):
    user = request.session['usuario_logado']
    unid = request.session['unidade']
    lista_estoque = EstoqueModel.objects.filter(usuario=user,unidade=unid).values(
    'produto','codigo','quantidade','preco_custo','total_custo','preco_varejo',
    'total_varejo','categoria')#lista de dicionário cotendo os campos e seus valores
    quant_produtos = EstoqueModel.objects.filter(usuario=user, unidade=unid).values('produto').count() #contamos a quantidade de produtos.
    totais = EstoqueModel().sum_col(user, unid)#contém as chaves que guadam os valores dos somatórios agregados das colunas.
    contexto = {
        'usuario': user,
        'unid': unid,
        'itens_total':totais['itens_totais'],
        'total_custo':totais['custos_totais'],
        'total_varejo':totais['varejo_total'],
        'quantidade_produto':quant_produtos,      
        'lista_estoque':lista_estoque,
    }
    
    return render(request,'lista.estoque.html',contexto)


@login_required       
def view_pesquisa_aluno(request):

    user = request.session['usuario_logado']
    unid = request.session['unidade']      

    #listamos os alunos pertecentes a unidade do usuário
    listagem_alunos = AlunoModel.objects.filter(usuario=user,unidade=unid).values(
        'nome','turma','responsavel','telefone_responsavel')   
    contexto = {'listagem_alunos':listagem_alunos, 'lista_aluno':True,
    'usuario': user, 'unidade':unid}
    
    # action gurada a ação pretendida(pesquisa)
    action = request.GET.get('action')
    #Se na template(pesquisa_aluno.html) for selecionado o butão "pesquisa por nome"
    if action == 'pesquisa':  
        
        if request.method =='POST':          
            pesquisa_aluno_form = AlunoFormModl(request.POST)
            if pesquisa_aluno_form.is_valid():
                aluno_form = pesquisa_aluno_form.cleaned_data['nome_aluno']
                # Checamos a não existência do registro do aluno
                not_exists = AlunoModel().exist_aluno(user,unid,aluno_form)
                if not_exists:
                    contexto = not_exists
                
                else: # existindo o registro seguimos com a pesquisa.
                    resultado_pesquisa = AlunoModel.objects.filter(
                    nome=aluno_form, usuario=user,unidade=unid).values(
                    'nome','turma','responsavel','telefone_responsavel')
                    contexto = {
                        'usuario': user,
                        'unidade': unid,
                        'resultado_pesquisa':resultado_pesquisa,
                        'resultado':True,
                    }               
        else:
            pesquisa_aluno_form = AlunoFormModl(usuario=user, unidade=unid)
            contexto = {
                    'usuario': user,
                    'unidade': unid,
                    'pesqu_aluno_form': pesquisa_aluno_form,
                    'formulario_pesquisa':True,            
                    }           
           
    return render(request,'pesquisa_aluno.html',contexto)