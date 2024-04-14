from datetime import datetime
from django.core.cache import cache
from django.shortcuts import get_object_or_404, render, redirect
from cadastro.forms import EstoqueFomModel
from cadastro.models import (AlunoModel, CadastrosVendaModel,
 DebitoModel, EstoqueModel, ModelAluno)
from pesquisa.forms import PesquisaAlunoForm
from .forms import (FormUpadateDebitoModelProduto, FormUpdateDebitoModelAluno, 
FormUpdateEstoque, FormUpdateEstoquePorProduto, UpadatePesquisaRegistroAluno, UpdateAlunoFormPesquisa,
UpdateAlunoForms, UpdateCadastroAluno, UpdateVendasForm, UpdateVendasForm, UpdateVendasformPesquisa)
from django.contrib.auth.decorators import login_required

def update(request):
    return render(request,'update.html')







@login_required
def view_update_estoque(request):
    
    """
    A view realizar alterações nos dados do produto no  
    estoque:
        * exibe o formulário para pequisa do produto a ser atualizado,

        * retorna o formulário populado com os dados do produto  
        
        * e salva as alterações feitas no banco de dados.
    
    *É necessário que o usuário esteja autenticado para acessar esta view
    e indique uma unidade correlacionada.
    
    """

    # Resgatando usuário e unidade 
    user = request.session['usuario_logado']
    unid = request.session['unidade']
   
    # Fomulário de pesquisa do produto.    
    pesquisa_form = FormUpdateEstoquePorProduto(usuario=user, unidade=unid)
    contexto = {
    'pesquisa_form': pesquisa_form, 'pesquisa_produto': True,'usuario':user,
    'unidade': unid
    }
    if request.method == 'POST':
        pesquisa_form = FormUpdateEstoquePorProduto(request.POST,usuario=user,
         unidade=unid)

        if pesquisa_form.is_valid():
            
            # Indicamos a instância a ser editada
            entrada_form = pesquisa_form.cleaned_data['produto']
           
            
            # Defindo o objeto a ser editado.
            instance_estoque = EstoqueModel.objects.get(
            unidade=unid, usuario=user,produto=entrada_form)                                     
        
            # formulário populado com os dados da instância à serem editados.         
            estoque_form = FormUpdateEstoque(instance=instance_estoque,usuario=user, unidade=unid) 
            contexto = {'estoque_form': estoque_form, 'usuario': user}

            # formulário com os dados já editados.
            if request.method == 'POST':

                estoque_form = FormUpdateEstoque(request.POST,
                instance=instance_estoque, usuario=user, unidade=unid)  
                
                if  estoque_form.is_valid():                      
                    
                    # Os dados limpos a serem atualizados 
                    campo_oculto = estoque_form.cleaned_data['campo_oculto']                 
                    form_quantidade = estoque_form.cleaned_data['quantidade']
                    form_preco_custo = estoque_form.cleaned_data['preco_custo']
                    form_total_custo = form_quantidade * form_preco_custo
                    form_preco_varejo = estoque_form.cleaned_data['preco_varejo']
                    form_total_varejo = form_quantidade * form_preco_varejo
                    form_categoria = estoque_form.cleaned_data['categoria']               

                    # Atualização dos campos pretendidos.
                    atualizando_estoque = EstoqueModel.objects.filter(
                        usuario = user, unidade = unid, 
                        produto=entrada_form).update(produto=campo_oculto,
                        quantidade=form_quantidade, preco_custo=form_preco_custo,
                        total_custo=form_total_custo,preco_varejo=form_preco_varejo,
                        total_varejo=form_total_varejo, categoria=str(form_categoria)
                    )

                    contexto = {
                            'sucesso': True,        
                       } 
        
        # Codição para valiação
        else: 
            contexto = {
                'pesquisa_form': pesquisa_form,
                'pesquisa_produto': True,'usuario':user,
                'unidade': unid
                }                            

    return render(request, 'update_estoque.html', contexto)


@login_required
def view_update_vendas(request):
    """
    A view corrige os registros de vendas que foram acometidas
    por um erro e em paralelo atualiza o estoque:

        * exibe o formulário para indentificação da venda à corrigir,

        * retorna os dados para atualização  
        
        * e salva as correções feitas no banco de dados.
    
    *É necessário que o usuário esteja autenticado para acessar esta view
    e indique uma unidade correlacionada.
    
    """
    # Resgatando usuário e unidade 
    user = request.session['usuario_logado']
    unid = request.session['unidade']   
    
    # Fomulário de pesquisa.
    pesquisa_form = UpdateVendasformPesquisa(request.POST or None,usuario=user, unidade=unid)
    contexto = {'pesquisa_form': pesquisa_form,
    'usuario': user, 'unidade':unid, 'pesquisa_venda': True}
   
    if pesquisa_form.is_valid():

        # Indicamos a instância a ser editada
        pesquisa_data = pesquisa_form.cleaned_data['data']
        pesquisa_produto = pesquisa_form.cleaned_data['produto']      
        
        # Checando a existência do registro no banco de dados.  
        if  CadastrosVendaModel.objects.filter(usuario=user,unidade=unid,
            produto=pesquisa_produto, data=pesquisa_data).exists():
            
            # Registro de venda para correção.
            instance_vendas = CadastrosVendaModel.objects.get(usuario=user,unidade=unid,
            produto=pesquisa_produto,data=pesquisa_data)
        
            # formulário populado com os dados da instância à serem editados.         
            vendas_form = UpdateVendasForm(instance=instance_vendas, usuario=user,
            unidade=unid)
            contexto = {
                "vendas_form": vendas_form,
                "usuario":user, "unidade":unid
            }
        if request.method == 'POST':
            vendas_form = UpdateVendasForm(request.POST, instance=instance_vendas,usuario=user, unidade=unid)
            if  vendas_form.is_valid(): 
                
                
                # Os dados limpos a serem atualizados
                quant_inicial = vendas_form.cleaned_data['quantidade_inicial']
                field_clone = str(vendas_form.cleaned_data['field_clone'])#inicializado com o valor do produto
                form_produto = vendas_form.cleaned_data['produto']                    
                form_quantidade = vendas_form.cleaned_data['quantidade']                
                form_valor_unitario = vendas_form.cleaned_data['valor_unitario']                
                form_data = vendas_form.cleaned_data['data']            

                #Atualização dos campos pretendidos.
                db_cadastro_vendas = CadastrosVendaModel()
                atualizar = db_cadastro_vendas.gerentec_update(user, unid,
                form_produto,field_clone, form_quantidade,quant_inicial,form_data,
                )   
                # Se o gerentec_update perceber "quantidade incial inferior a final".
                if atualizar == 'quant_superior':
                                         
                    contexto['quant_superior'] = True
                
                # O gerentec_update precessor tudo corretamente.
                else:
                    contexto['sucesso'] = True


                
        else:
            contexto['registro_inexistente'] = 'registro inexistente'

    return render(request, 'update_vendas.html', contexto)


@login_required
def view_update_aluno(request):

    """
    A view realizar alterações nos dados de cadastro   
    do aluno:

        * exibe o formulário para pequisa do aluno à ser atualizado,

        * retorna o formulário populado com os dados do aluno  
        
        * e salva as alterações feitas no banco de dados.

    *É necessário que o usuário esteja autenticado para acessar esta view
    e indique uma unidade correlacionada.
    
    """
    # Resgatando usuário e unidade 
    user = request.session['usuario_logado']
    unid = request.session['unidade']   
     
     # Formulário de pesquisa
    form_pesquisa = UpadatePesquisaRegistroAluno(request.POST or None,
    usuario=user, unidade=unid)
    contexto = {'usuario': user,'unidade': unid ,
        'form_pesquisa':form_pesquisa ,'pesquisa': True}


    if request.method == 'POST':

        if form_pesquisa.is_valid():
            open_aluno = form_pesquisa.cleaned_data['nome']            
            
            # Instanciando aluno.
            instance_aluno = ModelAluno.objects.get(nome=open_aluno )

            
            form_preenchido = UpdateCadastroAluno(instance=instance_aluno)              
            contexto = {'usuario': user, 'unidade': unid,
            'form_preenchido': form_preenchido ,'instanciado': True}     
                      
            type_form = request.POST.get('type_form')
           
            # Se o form_preenchido for subemetido
            if request.POST.get('type_form') == 'form_preenchido':                
                    
                    form_preechido = UpdateCadastroAluno(request.POST,
                    instance=instance_aluno)
                
                    if form_preechido.is_valid():

                        clone_fild_name = form_preechido.cleaned_data['clone_fild_name']
                        form_turma = form_preechido.cleaned_data['turma']
                        form_responsavel = form_preechido.cleaned_data['responsavel']  
                        form_telefone_responsavel = form_preechido.cleaned_data['tel_responsavel']  

                        # Realizando a atualização.
                        atualizando_aluno = ModelAluno.objects.filter(usuario=user, unidade=unid,nome=open_aluno).update(
                        nome=clone_fild_name, turma=form_turma, responsavel=form_responsavel,
                        tel_responsavel=form_telefone_responsavel)    

                    contexto = {
                                'sucesso': True,            
                                }                         
        else:
            contexto = {'usuario': user,'unidade': unid ,
            'form_pesquisa':form_pesquisa ,'pesquisa': True}   
        
    return render(request,'update_aluno.html', contexto)




