
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

# from Delete.forms import DeleteProdutoEstoque, PesquisaEstoqueFormDelete
from cadastro.models import EstoqueModel
from deleta.forms import DeleteProdutoEstoque, PesquisaEstoqueFormDelete


@login_required
def view_delete_produto(request): 
    user = request.session['usuario_logado']
    unid = request.session['unidade']
   
    # Fomulário de pesquisa do produto a ser deletado.    
    pesquisa_form =PesquisaEstoqueFormDelete(request.POST or None)
    contexto = {
    'pesquisa_form': pesquisa_form, 'pesquisa_produto': True,'usuario':user,
    'unidade': unid}
   
    if pesquisa_form.is_valid():
        
        entrada_form = pesquisa_form.cleaned_data['produto']
        db_estoque = EstoqueModel()

        #Checando a entrada do formulario
        not_exist = db_estoque.chec_produt(user, unid, entrada_form)
       
        if not_exist:               
            contexto = not_exist
        else:

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

    return render(request, 'delete_produto.html', contexto)


