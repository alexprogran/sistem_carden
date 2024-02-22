import random
from django import forms
from django.db import models
from django.core.validators import RegexValidator
from django.db.models import Max
from decimal import Decimal
from django.db.models import Sum
import datetime

class AlunoModel(models.Model):
  
    usuario = models.CharField(verbose_name='Usuáiro',max_length=25,null=True, blank=True)
    unidade = models.CharField(verbose_name='Unidade',max_length=25, null=True, blank=True) 
    nome = models.CharField(verbose_name='Nome',max_length=25)
    turma = models.CharField(verbose_name='Turma',max_length=20,)
    responsavel = models.CharField( verbose_name='Responsavel',max_length=25)
    telefone_responsavel = models.CharField(verbose_name='Contato do responsável',max_length=25)   
    
    def exist_aluno(self, usuario, unidade, name_aluno):
        """O método " exist_aluno" checa a não existência do registro"""
        if not AlunoModel.objects.filter(
                nome=name_aluno, usuario=usuario,unidade=unidade).exists():
                   
                    return {'not_valid': True, 'input_form': name_aluno}
       
    def __str__(self):
        return self.nome



class CategoriaProdutoModel(models.Model):
    usuario = models.CharField(verbose_name ='Usuário', max_length=25, null=True,blank=True)
    unidade = models.CharField(verbose_name='Unidade', max_length=25, null=True,blank=True)
    categoria = models.CharField(
    verbose_name='Categoria', max_length=25
    )

    def __str__(self):
        return self.categoria



class EstoqueModel(models.Model):
    usuario = models.CharField(verbose_name ='Usuário', max_length=25, null=True,blank=True)
    unidade = models.CharField(verbose_name='Unidade', max_length=25, null=True,blank=True)
    produto = models.CharField(verbose_name='Produto', max_length=25, null=True,blank=True)
    codigo = models.CharField(verbose_name='Código', max_length=25)    
    quantidade = models.IntegerField(verbose_name='Quantidade')
    preco_custo = models.DecimalField(verbose_name='Preço custo',max_digits=20,decimal_places=2)
    total_custo = models.DecimalField(verbose_name='Total custo',max_digits=20,decimal_places=2)
    preco_varejo = models.DecimalField(verbose_name='Preço varejo',max_digits=20,decimal_places=2)
    total_varejo = models.DecimalField(verbose_name='Total varejo',max_digits=20,decimal_places=2)   
    categoria =  models.CharField(verbose_name='Categoria', max_length=25, null=True)

    def chec_produt(self, user, unid, product):
        """
            O método "chec_produto" realiza a checagem da existência do produto no estoque.

         """
        if not EstoqueModel.objects.filter(usuario=user, unidade=unid, produto=product).exists():
            invalid = {'produto_invalido':True}
            return invalid


    def sum_col(self,user,unid):
        '''
        O método "sum_col " realiza a soma das colunas especificadas e retorna um dicionário
        contendo um conjunto de chaves que tem como valores a soma agregada das colunas.
        '''
        # Obitendo o dicionário cujo os valores das chaves é o soma agregada das colunas.
        total = EstoqueModel.objects.filter(usuario=user,unidade=unid).aggregate(
            itens_totais=Sum('quantidade'),
            custos_totais=Sum('total_custo'),
            varejo_total=Sum('total_varejo'),
        )
        return total

    def gerador_de_codigo(self):
        """ 
        O método gera numerais  que  são resultados do resgate do ultimo id do modelo
        EstoqueModel e a soma por mais um. Uma das utilizações para estes númerais é 
        sevirem como valores para códigos na tabela.

        """
        registro_estoque = EstoqueModel.objects.count()#buscando registros 
        if registro_estoque > 0:
            id_code = EstoqueModel.objects.aggregate(Max('id'))['id__max']
            codigo = id_code + 1
        else: # caso a tabela esta vazia, sem registros.
            codigo = 1
        return codigo
    
    def atualize_db_estoque(self, user , unid,produt_form,quant_form):       
        
        '''  
        O método atualize_db_estoque atualiza a quantidade de produto no 
        estoque em função da venda ,subtraindo, do estoque, as mesmas 
        quantidades do produto na venda.     

        '''           
        
        instance = EstoqueModel.objects.get(usuario=user,
        unidade=unid, produto=produt_form)#instância a ser atualizada

        # os novos valores dos campos a serem atualizados
        nova_quantidade = instance.quantidade - int( quant_form )
        novo_total_custo = nova_quantidade * instance.preco_custo
        novo_total_varejo = nova_quantidade * instance.preco_varejo
        
        # Realizando a atualização com os novos valores.
        atualizando_estoque = EstoqueModel.objects.filter(usuario=user,unidade=unid,
        produto=produt_form).update(quantidade=nova_quantidade,
        total_varejo=novo_total_varejo , total_custo=novo_total_custo)



    def corrige_db_estoque  (self, user , unid,produt_corrig ,produt_edit,quant_form):
        '''  
        O método corrige_db_estoque corrige a quantidade dos produtos envolvidos 
        na autualização, devolvendo a quantidade, registrada(eroneamente),  de saida do produto
        ao estoque e subtrai da quantidade do produto  de correção para os ajustes no estoque.
        
        --> Parâmetros passados: user(usuário), unid(unidade), 
        produt_corrig(produto indicado par troca),
        produt_edit(produto indicado para a correção) 
        quant_form(quantidade do produto para a correção)<--

        '''     
        # lista de campos que irá definir a instâcia à atualização.
        lista_produto = [produt_edit, produt_corrig]  


        for produt in lista_produto:

            # Indentificando a instância a ser atualizada.
            instance = EstoqueModel.objects.get(usuario=user,
            unidade=unid, produto=produt )
            
            # Subtraindo a quantidade do produto  de correção no estoque
            if produt == produt_edit:
                
                # os novos valores dos campos a serem atualizados
                nova_quantidade = instance.quantidade - int( quant_form )
                novo_total_custo = nova_quantidade * instance.preco_custo
                novo_total_varejo = nova_quantidade * instance.preco_varejo
                
            # # Devolvendo a quantidade  registrada(errada) de saida do produto
            else:
                                                       
                # os novos valores dos campos a serem atualizados
                nova_quantidade = instance.quantidade + int( quant_form )        
                novo_total_custo = nova_quantidade * instance.preco_custo
                novo_total_varejo = nova_quantidade * instance.preco_varejo
                
                print('instance.quantidade:',instance.quantidade,'quant_form:',int( quant_form ),"nova_quantidade:",nova_quantidade  )
                    
            # Realizando a atualização com os novos valores.
            atualizando_estoque = EstoqueModel.objects.filter(usuario=user,unidade=unid,
            produto=produt).update(quantidade=nova_quantidade,
            total_varejo=novo_total_varejo , total_custo=novo_total_custo)

         

    def  subtrai_db_estoque(self, user, unid, produto_form,diferenca):       
        # user = usuario, unidade = unid
        '''  
        O método subtrai_db_estoque atualiza a quantidade de produto no estoque em função da venda,
        subtraindo do estoque a diferença indacada na atualização.
        '''           
                
        instance = EstoqueModel.objects.get(usuario=user, unidade=unid,produto=produto_form)#instância a ser atualizada

        # os novos valores dos campos a serem atualizados
        nova_quantidade = instance.quantidade + int(diferenca)# o sinal "+" - diferença sempre negativa
        novo_total_custo = nova_quantidade * instance.preco_custo
        novo_total_varejo = nova_quantidade * instance.preco_varejo
        
        # Realizando a atualização com os novos valores.
        atualizando_estoque = EstoqueModel.objects.filter(usuario=user, unidade=unid,
        produto=produto_form).update(quantidade=nova_quantidade,
        total_varejo=novo_total_varejo , total_custo=novo_total_custo)


    
    def acresce_db_estoque(self,user, unid, produto_form, form_quantidade):
       #user = usuario , unid = unidade
       
        ''' O método "acresce_db_estoque" realiza a atualização no estoque acrescentando-lhe a quantidade
        que lhe foi subtraido na venda. A idéia é corrigir a quantidade do produto que foi retirado do estoque
        erroneamente.
        '''       
       
        #instância a ser atualizada    
        instance = EstoqueModel.objects.get(usuario=user,
        unidade=unid,produto=produto_form)

        # os novos valores dos campos a serem atualizados
        nova_quantidade = int(instance.quantidade) + int(form_quantidade)
        novo_total_custo = nova_quantidade * instance.preco_custo
        novo_total_varejo = nova_quantidade * instance.preco_varejo
        
        # Realizando a atualização com os novos valores.
        atualizando_estoque = EstoqueModel.objects.filter(usuario=user
        ,unidade=unid, produto=produto_form).update(quantidade=nova_quantidade,
        total_varejo=novo_total_varejo , total_custo=novo_total_custo)
       

    def __str__(self):
        return self.produto



class DebitoModel(models.Model):
    usuario =  models.CharField(verbose_name='Usuário', max_length=25,blank=True,null=True)
    unidade =  models.CharField(verbose_name='Unidade', max_length=25,blank=True,null=True)
    aluno =  models.CharField(verbose_name='Aluno', max_length=25,blank=True,null=True)
    produto =  models.CharField(verbose_name='produto', max_length=25, blank=True,null=True)      
    valor_unitario = models.DecimalField(verbose_name='Valor unitário',max_digits=10,decimal_places=2)
    quantidade =  models.DecimalField(verbose_name='Quantidade',max_digits=10,decimal_places=0)
    valor_total =  models.DecimalField(verbose_name='Total',max_digits=10,decimal_places=2,null=True,blank=True)    
    data = models.DateField(verbose_name='Data')
    criado_em = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    
    
    def atualiza_db_debito(self,unid,user,produto_form,data_form,quantidade_form,aluno_form):
       
        '''
        O método "atualiza" realizar as atualizações 
        nos campo "quantidade" e "valor_total" do modelo.
        '''
        
        existe_registro = DebitoModel.objects.filter(usuario=user,unidade=unid,aluno=aluno_form,
        produto=produto_form, data=data_form).exists()
        
        if existe_registro:
            registro_debito = DebitoModel.objects.get(usuario=user, unidade=unid, 
            aluno=aluno_form, data=data_form, produto=produto_form)
            nova_quantidade = registro_debito.quantidade + quantidade_form 
            novo_valor_total = registro_debito.valor_total + (quantidade_form*registro_debito.valor_unitario)
            atualizar = DebitoModel.objects.filter(usuario=user, unidade=unid,
            aluno=aluno_form, produto=produto_form, data=data_form).update(
            quantidade=nova_quantidade,valor_total=novo_valor_total)  

    def gerador_de_codigo(self):
        '''Esta método utiliza o utimo id gerado no próprio modelo, DebitoModel, com 
         um dos elementos para construir números sequências.
            
        '''
        id_code = DebitoModel.objects.aggregate(Max('id'))['id__max']
        if id_code == None:
            codigo = 1 # Se a tebela não possuir registros
            return codigo
        codigo = id_code + 1 #--> valor para o campo código

        return codigo
          
    # def save(self, *args, **kwargs):       
        
    #     if not self.codigo:
    #         self.codigo = self.gerador_de_codigo() # salvando altomáticamente o código na tabela DebitoModel. 
    #     super().save(*args, **kwargs)

    def gerentec(self,unid,user,aluno_form,
        produto_form, quantidade_form, data_form, valor_unitario_form):

        """O método gerentec estabelece o critério de que ,para a criação de registro no modelo 
        não deverá existir registro do produto na data especificada, sendo realizado
        somente a atualização dos campos "quantidade" e "valor_total". O método retorna um dicionário cuja 
        a chave "sucesso" possui  boleano True.
         """
        
        cadastro_venda = DebitoModel(
            usuario=user,
            unidade=unid,       
            aluno=aluno_form,
            produto=produto_form,
            quantidade=quantidade_form,          
            data=data_form,
            valor_unitario = valor_unitario_form,
            valor_total=valor_unitario_form * quantidade_form,
         

        )
        # Condição para somente alterar a quantidade e o valor total
        if DebitoModel.objects.filter(unidade=unid,usuario=user, aluno=aluno_form,
            produto=produto_form, data=data_form).exists():  
            quary_set = DebitoModel()
            atualiza = quary_set.atualiza_db_debito(unid, user, produto_form,data_form,quantidade_form,aluno_form) # Atualizando(quantidade e valor total)
        else: # Realizando um  registro completo do produto na tabela.
            cadastro_venda.save()
        quary_set = DebitoModel()
        contexto = {
            'sucesso':True,
        }  
        return contexto
    
    def __str__(self):
        return self.aluno



class HistoricoDebitoModel(models.Model):
    aluno =  models.CharField(verbose_name='aluno',max_length=25)
    produto =  models.CharField(verbose_name='produto', max_length=25)
    valor = models.DecimalField(verbose_name='Valor',max_digits=5,decimal_places=3)
    data = models.DateField(verbose_name='Data')
    criado_em = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)    
    
    def __str__(self):
        return self.aluno



class FuncionarioModel(models.Model):
    funcionario = models.CharField(verbose_name='Funcionário',max_length=25)
    telefone = models.CharField(verbose_name='Telefone', max_length=25)

    def __str__(self):
        return self.funcionario



class CadastrosVendaModel(models.Model):
    usuario = models.CharField(verbose_name='Usuário', blank=True,null=True, max_length=25)
    unidade = models.CharField(verbose_name='Unidade', blank=True,null=True, max_length=25)
    produto = models.CharField(verbose_name='Produto', blank=True,null=True, max_length=25)
    quantidade = models.DecimalField(verbose_name='Quantidade',max_digits=20,decimal_places=0)
    valor_unitario =models.DecimalField(verbose_name='Valor_unitário',max_digits=20,decimal_places=2) 
    valor_total = models.DecimalField(verbose_name='Valor',max_digits=20, decimal_places=2) 
    data = models.DateField(verbose_name='Data')

        
    def acres(self, *args, **kwargs ):
        
        """
        O método "acres" é  usuado nas atualizações dos registros de vendas.
        O método exclui o registro da venda(que esta sendo corrigido) 
        e em paralelo acrescenta a mesma quantidade do registro deletado
        a quandidade do produto apontando para a correção.  
          
       --> Parâmetros para o método acres:
        usuario=user, unidade=unid, pro_corrig=produt_corrigir,
        pro_edit=produt_edit, qut_form=quantidade_form, 
        qut_inicil=quantidade_inicial, date=data_form, delete=True <--

        """  

        user = kwargs.get('usuario')
        unid = kwargs.get('unidade')
        pro_corrig = kwargs.get('pro_corrig')
        pro_edit = kwargs.get('pro_edit')
        date = kwargs.get('date')
        quant_form = kwargs.get('qut_form')

        # "Deletetando o registro zerado  na quantidade"
        if kwargs.get('delete'):

            # encontrando a instância a ser deletada.
            delete_instance = CadastrosVendaModel.objects.get(
            usuario=user, unidade=unid, produto=pro_corrig, data=date).delete()
       
            # Edite a nova quantidade para o produto corrigido:
            
                # encontrando a instância a editar
            produto_edit = CadastrosVendaModel.objects.get(usuario= user, unidade=unid ,
            produto=pro_edit ,data=date )
                # alterar a quantidade
            quant_edit = produto_edit.quantidade + int(quant_form)
            total_valor = quant_edit * produto_edit.valor_unitario
                # atualizando                    
            atualizar = CadastrosVendaModel.objects.filter(usuario=user,
            unidade=unid, data=date, produto=produto_edit).update(quantidade=quant_edit,valor_total=total_valor)
        
        # Quando a quantidade do registro não zerar.
        else:
            list_produt = [pro_corrig, pro_edit] 
            
            
            for produt in list_produt:    
                # encontrando a instância a editar
                instance_produt = CadastrosVendaModel.objects.get(
                usuario=user, unidade=unid, produto=produt, data=date)
                             
                # Produto apontado para a correção.
                if produt == pro_corrig:
                        
                        # alterar a quantidade
                    quant_corrigida = instance_produt.quantidade - int(quant_form)
                    valor_final = quant_corrigida * instance_produt.valor_unitario

                # Novo produto para atualização       
                else:
                     # alterar a quantidade
                    quant_corrigida = instance_produt.quantidade + int(quant_form)
                    valor_final = quant_corrigida * instance_produt.valor_unitario

                # atualizando   
                atualizar = CadastrosVendaModel.objects.filter(usuario=user,
                unidade=unid, produto=produt).update(quantidade=quant_corrigida,valor_total=valor_final)



    def pesquisa_data(user,unid,data_pesquisa):
        # user = usuário, unid = unidade
        """ O método pesquisa_data realiza uma filtragem  """


        query = CadastrosVendaModel.objects.filter(usuario=user,unidade=unid,
        data=data_pesquisa).values('produto', 'quantidade','valor_unitario',
        'valor_total', 'data')
        print(f'Query: {query}')
        total = CadastrosVendaModel.objects.filter(usuario=user,unidade=unid,
        data=data_pesquisa).aggregate(
            quantidade_total=Sum('quantidade'),
            valor_total=Sum('valor_total')
            )
        quantidade_total = total['quantidade_total']
        valor_total = total['valor_total']
      
        return query, quantidade_total, valor_total
    

    def pesq_venda_inter_data(data_inicio):
        data_final = datetime.now()

        
        query_entre_datas = DebitoModel.objects.filter(data__range=(data_inicio,data_final)).values(
            'produto__produto', 'quantidade','valor_unitario','valor_total', 'data',
            ).order_by('data')
        total_entre_datas = DebitoModel.objects.filter(data__range=(data_inicio,data_final)).aggregate(
            quantidade_total=Sum('quantidade'),
            valor_total=Sum('valor_total')
            )
        quant_total = total_entre_datas['quantidade_total']
        valor_total = total_entre_datas['valor_total']
      
        return query_entre_datas, quant_total, valor_total


    def atualiza(self,user, unid, produto,data,quantidade):
        # user(usuário), unid(unidade)
        '''O método "atualiza" realizar a definição dos valores para os campos "quantidade"
          e "valor_total" no modelo CadastroVendaModel.'''
        
        # Checagem de registro da venda do produto para a data especificada
        existe_registro = CadastrosVendaModel.objects.filter(usuario=user,
        unidade=unid, produto=produto, data=data).exists()
       
        if existe_registro:
            print('Entrou na condição para atualizar')
            # Indentificando a instância
            registro_venda = CadastrosVendaModel.objects.get(usuario=user, unidade=unid,
            data=data,produto=produto)
            print( 'Parâmetros do atualize:', user, unid, produto, data, quantidade)

            # acrescentamos a quantidade do produto vendito a quantidade existente no banco.
            nova_quantidade = registro_venda.quantidade + Decimal(quantidade )
            
            # Definição do valor total
            novo_valor = Decimal(registro_venda.valor_total) + (Decimal(quantidade) * registro_venda.valor_unitario)
            # Realizando as atualizações
            atualizar = CadastrosVendaModel.objects.filter(usuario=user,unidade=unid,produto=produto, data=data).update(quantidade=nova_quantidade,valor_total=novo_valor) 
           
   
    def update_venda_estoque(self,user, unid, produto,data,quantidade_form,quantidade_inicial):
       
        ''' O método update_venda_estoque realiza as correções de saidas 
        e entradas de produtos no estoque decorrentes de vendas ou atualizações da mesma.
          '''
        
        # Checagem de registro da venda do produto para a data especificada.
        existe_registro = CadastrosVendaModel.objects.filter(usuario=user, unidade=unid,
        produto=produto, data=data).exists()
        
        if existe_registro:
           

            # Indentificando a instância.
            instance_vendas = CadastrosVendaModel.objects.get(usuario=user, unidade=unid,
            data=data,produto=produto) 
            # Definindo o valor total.          
            novo_valor = Decimal(quantidade_form)*instance_vendas.valor_unitario
            # Atualização no "db cadastro de vendas".
            atualize_vendas = CadastrosVendaModel.objects.filter(usuario=user, unidade=unid,
            produto=produto, data=data).update(
            quantidade=quantidade_form,valor_total=novo_valor)

            # Corrigindo a quantidade no estoque.
            # Definindo a quantidade que será altualizada(quantidade_inicial é o valor a ser corrigido)
            diferenca = int(quantidade_inicial ) - int(quantidade_form) #quantidade_form é o valor de corre print('quantidade_inicial:',int(quantidade_inicial),'quantidade_form',int(quantidade_form))
            if diferenca > 0:
                estoque_model = EstoqueModel()
                atualize_estoque = estoque_model.acresce_db_estoque(user, unid,
                produto,diferenca)
            elif diferenca < 0:
                estoque_model = EstoqueModel()
                diferenca
                atualize_estoque = estoque_model.subtrai_db_estoque(produto,diferenca)
    
    import datetime

    def gerentec(self,user,unid,produto,quantidade,data,valor_unidade):

        """O método gerentec estabelece o critério de que ,para a criação de registro no modelo 
        CadastrosVendaModel, não deverá existir registro do produto na data especificada, sendo realizado
        somente a atualização dos campos "quantidade" e "valor_total". O método gerentec também é responsável
        por realizar a dinâmica de atualização do estoque correlacionada a venda, o método retorna um 
        dicionário cuja a chave "sucesso" possui valor  boleano True.
         """
        
        cadastro_venda = CadastrosVendaModel(          
        usuario=user,
        unidade=unid,
        produto=produto,
        quantidade=quantidade,          
        data=data,
        valor_unitario = valor_unidade,
        valor_total=valor_unidade*Decimal(quantidade),

        )
        # Existindo a venda do produto na data, atualizamos a quantidade e o valor total
        if CadastrosVendaModel.objects.filter(usuario=user, unidade=unid,
            produto=produto, data=data).exists():  
            quary_set = CadastrosVendaModel()
            atualizando_db_vendas = quary_set.atualiza(user, unid,
            produto,data, quantidade) 
        else: # Se a condição acima não for sartisfeita realizamos
             #o registro completo do produto na tabela.
            cadastro_venda.save()
      
        contexto = {
            'sucesso':True,
        }  

        #-->  Atualização do produto no estoque em função das venda. 
        estoque = EstoqueModel()
        atualizando_estoque = estoque.atualize_db_estoque(user,
        unid ,produto, quantidade) 

        return contexto


    def gerentec_update(self,user, unid, produt_corrigir,produt_edit,
        quantidade_form,quantidade_inicial,data):
        # user = usuario , unid = unidade
        
        """O método gerentec estabelece o critério de que ,para a criação de registro no modelo 
        CadastrosVendaModel, não deverá existir registro do produto na data especificada, sendo realizado
        somente a atualização dos campos "quantidade" e "valor_total". O método gerentec também é responsável
        por realizar a dinâmica de atualização do estoque correlacionada a venda, o método retorna um 
        dicionário cuja a chave "sucesso" possui valor  boleano True.
         """
       
        # Se editarmos o produto
        if produt_corrigir != produt_edit:
            # Corrigindo a tabela de vendas.
            vendas_model = CadastrosVendaModel()
            # atualize = vendas_model.gerentec(user,unid,produt_edit,quantidade_form,data,valor_unitario)
            
            dif_quant = int(quantidade_inicial) - int(quantidade_form)         

           # Quando a correção zerar a quantidade do produto na data especificada no registro de vendas.
            if dif_quant <= 0 :

                # Atualizando o banco de dados de registro de vendas.      
                atualizar_vendas = CadastrosVendaModel().acres(usuario=user,unidade=unid,
                pro_corrig=produt_corrigir, pro_edit=produt_edit,
                qut_form=quantidade_form, date=data, delete=True
                )  

                # Atualizando o banco de dados do estoque: 
                atualizar = EstoqueModel().corrige_db_estoque( user, unid, 
                produt_corrigir, produt_edit,quantidade_form )

              
            # Quando a correção não zera a quantidade do produto na data especificada no registro de vendas. 
            else:
                
            # Atualizando registro de vendas.
                atualiza_vendas = CadastrosVendaModel().acres(
                usuario=user,unidade=unid, pro_corrig=produt_corrigir,
                pro_edit=produt_edit, qut_form=quantidade_form, date=data
                )                
            # Atualizando os registros no estoque.

                atualiza_estoque = EstoqueModel().corrige_db_estoque( user, unid, 
                produt_corrigir, produt_edit,quantidade_form )
           
           
        #Somente será autulaizado  a quatidade
        else:
            # Atualizando a quantidade do produto no "db vendas" e no "db estoque" 
            vendas_model = CadastrosVendaModel()          
            atualize = vendas_model.update_venda_estoque(user, unid, produt_corrigir,
            data, quantidade_form, quantidade_inicial)        
      
        contexto = {
            'sucesso':True,
        }  


        
    def __str__(self):
        return self.produto
   


class TesteEstoqueModel(models.Model):
    usuario = models.CharField(verbose_name='Usuário',max_length=25, )
    unidade = models.CharField(verbose_name='Unidade', max_length=25,null=True,default='s/dados')
    produto = models.CharField(verbose_name='Produto',max_length=25)
    quantidade = models.CharField(verbose_name='Quantidade',max_length=25)
    valor = models.IntegerField(verbose_name='Valor')

    def __etr_(self):
        return self.usuario



class UsuariosModel(models.Model):
    username = models.CharField(verbose_name='Username', max_length=25)
    password = models.CharField(verbose_name='Password',max_length=25)

    def __str__(self):
        return self.username



class UnidModel(models.Model):
    usuario = models.CharField(verbose_name='Ususario',max_length=25)
    unidade = models.CharField(verbose_name='Unidade', max_length=25)




    def __str__(self):
        return self.unidade
    
