
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cadastro.models import  DebitoModel, EstoqueModel, ModelAluno
from .forms import DeleteAlunoModelForm, DeleteProdutoEstoque, PesquisaAlunoFormDelete, PesquisaEstoqueFormDelete



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





def delete_lista_debito(request):
    """
    A view esta relacionada com a visualização da lista de débito
    excluida do aluno.

    """

    user = request.session['usuario_logado']
    unid = request.session['unidade']

    nome_aluno = request.GET.get('nome')   
    lista_debito = request.GET.get('lista_debito')
  
   
    infor_debito =  DebitoModel.objects.filter(usuario=user,
    unidade=unid,aluno=nome_aluno).values('aluno','produto',
    'data','quantidade','valor_unitario','valor_total')
      
    contexto = {
        'sucesso':True,
        'aluno':nome_aluno,
        'infor_debito':infor_debito       
    }
    
    if infor_debito:
        infor_debito =  DebitoModel.objects.filter(aluno=nome_aluno)
        infor_debito.delete()
   
    return render(request,'delete_list.html',contexto)