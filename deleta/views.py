
from django.http import FileResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cadastro.models import  DebitoModel, EstoqueModel, ModelAluno
from .forms import DeleteAlunoModelForm, DeleteProdutoEstoque, PesquisaAlunoFormDelete, PesquisaEstoqueFormDelete
from django.db.models import Min, Max
from pesquisa.views import view_pdf

@login_required
def view_delete_produto(request): 
    """ 
        A view deleta o registro do produto na base de dados:

            * exibe o formulário de pesquisa do produto a ser excluido,

            * retorna o formulário populado com os dados do produto
            para confirmar à exclusão

            * e deleta o registro especificado.

        É necessário que o usuário esteja autenticado para acessar esta view
        e indique uma unidade correlacionada.    
    """
    # Resgatando usuário e unidade.
    user = request.session['usuario_logado']
    unid = request.session['unidade']
   
    # Fomulário de pesquisa do produto a ser deletado.    
    pesquisa_form =PesquisaEstoqueFormDelete(request.POST or None, usuario=user, unidade=unid)
    contexto = {
    'pesquisa_form': pesquisa_form, 'pesquisa_produto': True,'usuario':user,
    'unidade': unid}
    
    if pesquisa_form.is_valid():
       
        entrada_form = pesquisa_form.cleaned_data['produto']

        # Instância a ser deletada
        instance_produt = EstoqueModel.objects.get(usuario=user,
        unidade= unid,produto=entrada_form)
        # Formulári com os dados da intância à ser deletada.
        form_produt = DeleteProdutoEstoque(instance=instance_produt)     
        contexto = {'form_produt':form_produt, 'usuario': user, 'unidade': unid }
        
        if request.method == 'POST':
            form_produt = DeleteProdutoEstoque(request.POST, instance=instance_produt) 
            if form_produt.is_valid(): 
                # Delete da instância
                produto_excluido = EstoqueModel.objects.filter(usuario=user,
            unidade= unid,produto=entrada_form).delete()
                contexto = {'sucesso': True}

    # Situação para validações
    else:
        contexto = {
        'pesquisa_form': pesquisa_form, 
        'pesquisa_produto': True,'usuario':user,
        'unidade': unid
    }
                

    return render(request, 'delete_produto.html', contexto)


@login_required
def view_delete_aluno(request):
    """ 
        A view deleta o registro do aluno no banco de dados:

            * exibe o formulário para pesquisa do aluno a ser excluido,

            * retorna o formulário populado com os dados do aluno
            para confimação da exclusão

            * e deleta o registro especificado.

        É necessário que o usuário esteja autenticado para acessar esta view
        e indique uma unidade correlacionada.    

    """

    # Resgatando usuário e unidade.
    user = request.session['usuario_logado']
    unid = request.session['unidade']
   
    # Fomulário para pesquisa do aluno.    
    pesquisa_form = PesquisaAlunoFormDelete(request.POST or None, usuario=user, unidade=unid)
    contexto = {
    'pesquisa_form': pesquisa_form, 'pesquisa_aluno': True,'usuario':user,
    'unidade': unid}
    
    if pesquisa_form.is_valid():
       
        entrada_form = pesquisa_form.cleaned_data['nome']

        # Instância a ser deletada
        instance_aluno = ModelAluno.objects.get(usuario=user,
        unidade= unid,nome=entrada_form)
        
        # Formulári com os dados da intância à ser deletada.
        form_aluno =  DeleteAlunoModelForm(instance=instance_aluno)     
        contexto = {'form_aluno':form_aluno, 'usuario': user, 'unidade': unid }
        
        if request.method == 'POST':
            form_aluno = DeleteAlunoModelForm(request.POST, instance=instance_aluno) 
            if form_aluno.is_valid(): 
                # Delete da instância
                aluno_excluido = ModelAluno.objects.filter(usuario=user,
            unidade= unid,nome=entrada_form).delete()
                contexto = {'sucesso': True}

    # Situação para validações
    else:
        contexto = {
        'pesquisa_form': pesquisa_form, 
        'pesquisa_aluno': True,'usuario':user,
        'unidade': unid
    }
                

    return render(request, 'delete_aluno.html', contexto)



def g_pdf(user,unid,estudante):
    pdf = DebitoModel().gera_pdf(user,unid,estudante)
    pdf_file = open(pdf, 'rb')
    return FileResponse(pdf_file, as_attachment=True, filename='lanches.pdf')


def delete_lista_debito(request):
    """
    Esta view muda o status de débito "pendente" em "pago" e retorna a lista 
    com o novo status.
    """

    user = request.session['usuario_logado']
    unid = request.session['unidade']
    session_aluno = request.session['aluno'] 


    infor =  DebitoModel.objects.filter(
        usuario=user,
        unidade=unid, 
        aluno=session_aluno, 
        status='pendente'
        )  
    
    infor_debito =  infor.values('aluno','produto',
    'data','quantidade','valor_unitario','valor_total')

    # cópia de segurança
    # pdf = view_pdf(request) 
    pdf = DebitoModel().gera_pdf(user,unid,session_aluno)
    # pdf = g_pdf(user, unid, session_aluno)
    
    if infor:
        lista_delit = infor
           
   
    data_updata = infor_debito.update(status='pago')        
    
    contexto = {
        'sucesso':True,
        'aluno':session_aluno,
        'infor': lista_delit,
     }
   
   
    # return render(request,'delete_list.html',contexto)
    return pdf
    





def delete_lista_debito_(request):
    """
    Esta view muda o status de débito "pendente" para "pago" e retorna a lista 
    com o novo status.
    """
    try:
        user = request.session['usuario_logado']
        unid = request.session['unidade']
        session_aluno = request.session['aluno']
    except KeyError:
        # Redireciona ou trata o caso onde a sessão não contém os dados esperados
        return render(request, 'error.html', {'message': 'Sessão inválida. Por favor, faça login novamente.'})

    infor = DebitoModel.objects.filter(
        usuario=user,
        unidade=unid, 
        aluno=session_aluno, 
        status='pendente'
    )

    # Atualiza o status para "pago"
    infor.update(status='pago')

    # Gera PDF
    pdf_path = DebitoModel().gera_pdf(user, unid, session_aluno)

    # Obtem os dados atualizados
    infor_debito = infor.values('aluno', 'produto', 'data', 'quantidade', 'valor_unitario', 'valor_total')

    contexto = {
        'sucesso': True,
        'aluno': session_aluno,
        'infor': infor_debito,
    }

    # Renderiza a página HTML com os dados atualizados
    response = render(request, 'delete_list.html', contexto)

    # Adiciona o PDF ao response
    pdf_file = open(pdf_path, 'rb')
    response.content = pdf_file.read()
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = 'attachment; filename="debito.pdf"'

    return response
