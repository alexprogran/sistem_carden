from datetime import datetime

from django.shortcuts import get_object_or_404, render
from cadastro.forms import AlunoForms, EstoqueFomModel
from cadastro.models import AlunoModel, CadastrosVendaModel, DebitoModel, EstoqueModel

from pesquisa.forms import AlunoFormModl

from upadate.forms import (FormUpadateDebitoModelProduto, FormUpdateDebitoModelAluno, 
FormUpdateEstoque, FormUpdateEstoquePorProduto, UpdateAlunoFormPesquisa,
UpdateAlunoForms, UpdateVendasForm, UpdateVendasForm, UpdateVendasformPesquisa)
from django.contrib.auth.decorators import login_required

def update(request):
    return render(request,'update.html')

def update_debito_model_aluno(request):
    update_aluno_form = FormUpdateDebitoModelAluno(request.POST or None)
    contexto = {'update_aluno_form':update_aluno_form}
    if update_aluno_form.is_valid():
        nome_a_tualizar = update_aluno_form.cleaned_data['nome_atual']
        codigo = update_aluno_form.cleaned_data['codigo']        
        nome_atualizado = update_aluno_form.cleaned_data['update_novo_nome']       
        novo_aluno = AlunoModel.objects.get(nome=nome_atualizado)
        update_aluno = DebitoModel.objects.filter(codigo=codigo).update(aluno=novo_aluno.id)
        contexto = {
            'sucesso': True,
            'form':update_aluno_form,
            'aluno':True,           
            'codigo': codigo,
            'nome_a_aturalizar':nome_a_tualizar,
            'nome_atualizado': nome_atualizado,
        }
    return render(request,'update_debito_model_aluno.html',contexto)


def update_debito_model_produto(request):
    update_produto_form = FormUpadateDebitoModelProduto(request.POST or None)
    contexto = {'update_produto_form':update_produto_form}
    if update_produto_form.is_valid():
        nome_produto = update_produto_form.cleaned_data['produto_exitente']
        update_produto = update_produto_form.cleaned_data['update_nome_produto']
        contexto = {
            'sucesso': True,
            'form':update_produto_form,
            'produto_atualizado':True,
            'nome_produto': nome_produto,
            'novo_produto':update_produto
        }
    return render(request,'update_debito_model_produto.html',contexto)


@login_required
def view_update_estoque(request):
    # Resgatando usuário e unidade 
    user = request.session['usuario_logado']
    unid = request.session['unidade']
   
    # Fomulário de pesquisa do produto.    
    pesquisa_form = FormUpdateEstoquePorProduto(usuario=user, unidade=unid)
    contexto = {
    'pesquisa_form': pesquisa_form, 'pesquisa_produto': True,'usuario':user,
    'unidade': unid}
    if request.method == 'POST':
        pesquisa_form = FormUpdateEstoquePorProduto(request.POST,usuario=user, unidade=unid)

        if pesquisa_form.is_valid():
            # Indicamos a instância a ser editada
            entrada_form = pesquisa_form.cleaned_data['produto']
            db_estoque = EstoqueModel()
            product_invalid = db_estoque.chec_produt(user, unid, entrada_form)
            # Checando a entrada do formulario
            if product_invalid:
                contexto = product_invalid
            else:
                
                # Defindo o objeto a ser editado  print(f'{entrada_form} não existe em nosso registros.')
                instance_estoque = EstoqueModel.objects.get(
                unidade=unid, usuario=user,produto=entrada_form)                                     
            
                # formulário populado com os dados da instância à serem editados.         
                estoque_form = FormUpdateEstoque(instance=instance_estoque,usuario=user, unidade=unid) 
                contexto = {'estoque_form': estoque_form, 'usuario': user}

                # formulário com os dados já editados.
                if request.method == 'POST':

                    print('Entrou no post') 
                    estoque_form = FormUpdateEstoque(request.POST,instance=instance_estoque,usuario=user, unidade=unid)  
                    
                    if  estoque_form.is_valid():
                        print('Entrou nos dados limpos')
                        
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

                     
                   



    return render(request, 'update_estoque.html', contexto)

@login_required
def view_update_vendas_(request):

    """ A view_update_vendas realiza atualizações nos registros de vendas
   que ocorrem em paralelo com os registros do estoque.
    """
    # Resgatando usuário e unidade 
    user = request.session['usuario_logado']
    unid = request.session['unidade']   
    
    # Fomulário de pesquisa.
    pesquisa_form = UpdateVendasformPesquisa(request.POST or None)
    contexto = {'pesquisa_form': pesquisa_form, 'pesquisa_venda': True}
   
    if pesquisa_form.is_valid():

        # Indicamos a instância a ser editada
        pesquisa_data = pesquisa_form.cleaned_data['data']
        pesquisa_produto = pesquisa_form.cleaned_data['produto']      
        
        # Condicionando a busca, a exitência do registro do produto na data vendido.  
        if  CadastrosVendaModel.objects.filter(produto=pesquisa_produto, data=pesquisa_data).exists():
            instance_vendas = CadastrosVendaModel.objects.get(produto=pesquisa_produto,data=pesquisa_data)
        
            # formulário populado com os dados da instância à serem editados.         
            vendas_form = UpdateVendasForm(instance=instance_vendas)
            contexto = {"vendas_form": vendas_form}

            # formulário com os dados já editados.
            if request.method == 'POST':
                vendas_form = UpdateVendasForm(request.POST,instance=instance_vendas) 
                        
                if  vendas_form.is_valid(): 
                    
                    
                    # Os dados limpos a serem atualizados
                    quant_inicial = vendas_form.cleaned_data['quantidade_inicial']
                    campo_oculto_produto = str(vendas_form.cleaned_data['recebe_produto'])
                    form_produto = vendas_form.cleaned_data['produto']                    
                    form_quantidade = vendas_form.cleaned_data['quantidade']                
                    form_valor_unitario = vendas_form.cleaned_data['valor_unitario']                
                    form_data = vendas_form.cleaned_data['data']
                    
                    # Atualização dos campos pretendidos.
                    db_cadastro_vendas = CadastrosVendaModel()
                    atualizar = db_cadastro_vendas.gerentec_update(
                    form_produto,campo_oculto_produto,form_quantidade,quant_inicial,form_data,form_valor_unitario
                    )                    

                    contexto = {
                        'sucesso': True,
                    }            
        else:
            contexto['registro_inexistente'] = 'registro inexistente'

    return render(request, 'update_vendas.html', contexto)

@login_required
def view_update_vendas(request):

    """ A view_update_vendas realiza atualizações nos registros de vendas
   que ocorrem em paralelo com os registros do estoque.
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
            instance_vendas = CadastrosVendaModel.objects.get(usuario=user,unidade=unid,
            produto=pesquisa_produto,data=pesquisa_data)
        
            # formulário populado com os dados da instância à serem editados.         
            vendas_form = UpdateVendasForm(instance=instance_vendas, usuario=user, unidade=unid)
            contexto = {
                "vendas_form": vendas_form,
                "usuario":user, "unidade":unid
            }
            if request.method == 'POST':
                vendas_form = UpdateVendasForm(request.POST, instance=instance_vendas,usuario=user, unidade=unid)
                if  vendas_form.is_valid(): 
                    
                    
                    # Os dados limpos a serem atualizados
                    quant_inicial = vendas_form.cleaned_data['quantidade_inicial']
                    field_clone = str(vendas_form.cleaned_data['field_clone'])
                    form_produto = vendas_form.cleaned_data['produto']                    
                    form_quantidade = vendas_form.cleaned_data['quantidade']                
                    form_valor_unitario = vendas_form.cleaned_data['valor_unitario']                
                    form_data = vendas_form.cleaned_data['data']
                    
                    # Restrigimos a quantidade de correção à do registro
                    print('form_quantidade: ',form_quantidade ,'quant_inicial', quant_inicial  )

                
                    if form_quantidade <= quant_inicial:    
                        # Atualização dos campos pretendidos.
                        db_cadastro_vendas = CadastrosVendaModel()
                        atualizar = db_cadastro_vendas.gerentec_update(user, unid,
                        form_produto,field_clone, form_quantidade,quant_inicial,form_data
                        )   

                        contexto = {
                            'sucesso': True,
                        }
                    # Se a quantidade correção superar à quantidade do registro.   
                    else:  

                        contexto['quant_superior'] = True
 

        else:
            contexto['registro_inexistente'] = 'registro inexistente'

    return render(request, 'update_vendas.html', contexto)





@login_required
def view_update_aluno(request):
    user = request.session['usuario_logado']
    unid = request.session['unidade']   
    
    # Fomulário de pesquisa.
    pesquisa_form =  UpdateAlunoFormPesquisa(request.POST or None)
    contexto = {'pesquisa_form': pesquisa_form, 'pesquisa_aluno': True, 'usuario': user}
    
    if pesquisa_form.is_valid():
        entrada_form = pesquisa_form.cleaned_data['nome_aluno']
        print('usuario:',user, 'unidade:',unid, 'entrada_form:', entrada_form)
        
        # Declarando a instância a ser editada
        instance_aluno = AlunoModel.objects.get(
        nome=entrada_form, usuario=user, unidade=unid) 
        print('instance:',instance_aluno)
        # Formulário preechido com os dados da intância
        form_preenchido =  UpdateAlunoForms(instance=instance_aluno) 
        contexto = {'form_preenchido': form_preenchido,'form_dados': True, 'usuario': user}
        
        
        if request.method == 'POST':
                    
            form_preenchido = UpdateAlunoForms(request.POST, instance=instance_aluno)
        
            if form_preenchido.is_valid():
                print('Você consiguiu validadar os dados')
                
                print('Formulário submetido e validado')  
                # Os dados limpos a serem atualizados
                clone_fild_name = form_preenchido.cleaned_data['clone_fild_name']
                form_turma = form_preenchido.cleaned_data['turma']
                form_responsavel = form_preenchido.cleaned_data['responsavel']  
                form_telefone_responsavel = form_preenchido.cleaned_data['telefone_responsavel']  

                # Realizando a atualização.
                atualizando_aluno = AlunoModel.objects.filter(usuario=user, unidade=unid,nome=entrada_form).update(
                nome=clone_fild_name, turma=form_turma, responsavel=form_responsavel,
                telefone_reponsavel=form_telefone_responsavel)    

                contexto = {
                            'sucesso': True,        
                            } 
            else: 

                form_preenchido = UpdateAlunoForms(request.POST, instance=instance_aluno)
                contexto = {'form_preenchido': form_preenchido,'preenchido_form.errors ': True}    
                
    return render(request, 'update_aluno.html', contexto)
