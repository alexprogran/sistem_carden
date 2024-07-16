import io
from django.core.cache import cache
import random
import datetime
from django.http import HttpResponse
from django import forms
from django.db import models
from django.core.validators import RegexValidator
from django.db.models import Max
from decimal import Decimal
from django.db.models import Sum
import numpy as np
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch


class AlunoModel(models.Model):
  
    usuario = models.CharField(verbose_name='Usuáiro',max_length=25,null=True, blank=True)
    unidade = models.CharField(verbose_name='Unidade',max_length=25, null=True, blank=True) 
    nome = models.CharField(verbose_name='Nome',max_length=25)
    turma = models.CharField(verbose_name='Turma',max_length=20,)
    responsavel = models.CharField( verbose_name='Responsavel',max_length=25)
    telefone_responsavel = models.CharField(verbose_name='Contato do responsável',max_length=25)   
    
    def exist_aluno(self, usuario, unidade, name_aluno):
        """O método checa a não existência do registro"""
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

        """ O método  realiza a checagem de existência do produto no estoque."""

        if not EstoqueModel.objects.filter(usuario=user, unidade=unid, produto=product).exists():
            invalid = {'produto_invalido':True}
            return invalid


    def sum_col(self,user,unid):
        '''
        O método  realiza a soma das colunas especificadas em uma a
        agregação e retorna um dicionário cuja as chaves posuem 
        como valor o resultado da adição.
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
        O método gera númerais a serem utilizados como códigos nos 
        variados cadastramentos.

        """
        registro_estoque = EstoqueModel.objects.count()#buscando registros 
        if registro_estoque > 0:
            id_code = EstoqueModel.objects.aggregate(Max('id'))['id__max']
            codigo = id_code + 1
        else: # caso a tabela esta vazia, sem registros.
            codigo = 1
        return codigo
    

    def atualize_db_estoque(self, user , unid,produt_form,quant_form):       
        
        '''  O método realiza atualizações no estoque . '''           
        
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


    def corrig_db_estoque  (*args,**kwargs):
        '''  
        O método realizar ajustes no  estoque decorrentes de
        correções do banco de dados de registro de vendas.
        
        A Args:

            user: usuário,
            unid: unidade,
            produt_inicio: produto que é incicializado, no formulário, para a correção,
            produt_final : produto final para atualização,
            quant_inicio: quantidade do produto incializado para correção,
            quant_editada: quantidade fornecida pelo usuário para correção,
            date: data do registro

            Kwargs:

                unic: True -  indica que irá ter apenas um produto para atualizar.

        '''
        user = kwargs.get('usuario')
        unid = kwargs.get('unidade')
        produt_inicio = kwargs.get('produt_inicial')
        produt_final = kwargs.get('produt_final')
        quant_editada = kwargs.get('quant_editada')
        quant_inicio=kwargs.get('quant_inicio')
        unic = kwargs.get('unic')
                 

        # Para atualizar um único produto no estoque.
        if unic: 
             
            # Indentificando a instância a ser atualizada.
            instance = EstoqueModel.objects.get(usuario=user,
            unidade=unid, produto=produt_inicio)           

            #Condição para acrescentar ou diminuir a quantidade no estoque.
            result = int(quant_inicio) - int(quant_editada)
            # Critério para adicionar ou subtrair da quantidade.
            if result < 0:
                new_quant = int(instance.quantidade) + result # "+" para troca de sinais 

            else:
               
                new_quant = instance.quantidade + result
            
            # Definindo os dados.           
            novo_total_custo = int(new_quant) * int(instance.preco_custo)            
            novo_total_varejo = int(new_quant) * int(instance.preco_varejo)
                   
            # Realizando a atualização com os novos valores.
            atualizando_estoque = EstoqueModel.objects.filter(usuario=user,unidade=unid,
            produto=produt_inicio).update(quantidade=new_quant,
            total_varejo=novo_total_varejo , total_custo=novo_total_custo)

        # Atualizando mais de um produto no estoque.     
        else:
             # lista de campos que irá definir a instâcia à atualização.
            lista_produto = [produt_final, produt_inicio]

            for produt in lista_produto:

                
                # Indentificando a instância a ser atualizada.
                instance = EstoqueModel.objects.get(usuario=user,
                unidade=unid, produto=produt)
                    
                # Subtraindo a quantidade do produto  de correção no estoque
                if produt == produt_inicio:          
                    
                    
                    # os novos valores dos campos a serem atualizados
                    nova_quantidade =  instance.quantidade + int(quant_editada)
                    novo_total_custo = int(nova_quantidade) * int(instance.preco_custo)
                    novo_total_varejo =int( nova_quantidade) * int(instance.preco_varejo)
                   
                # Devolvendo a quantidade  registrada(errada) de saida do produto
                elif produt == produt_final :                           

                    # os novos valores dos campos a serem atualizados
                    nova_quantidade = int(instance.quantidade) - int( quant_editada )       
                    novo_total_custo = nova_quantidade * instance.preco_custo
                    novo_total_varejo = nova_quantidade * instance.preco_varejo
                                
                        
                # Realizando a atualização com os novos valores.
                atualizando_estoque = EstoqueModel.objects.filter(usuario=user,unidade=unid,
                produto=produt).update(quantidade=nova_quantidade,
                total_varejo=novo_total_varejo , total_custo=novo_total_custo)
            
                cache.clear()


    def  subtrai_db_estoque(self, user, unid, produto_form,diferenca):       
        # user = usuario, unidade = unid
        '''  
        O método realiza ajustes na quantidade de produto do estoque em função da venda,
        subtraindo do estoque a diferença indacada na atualização.
        '''           
                
        instance = EstoqueModel.objects.get(usuario=user, unidade=unid,produto=produto_form)#instância a ser atualizada

        # os novos valores dos campos a serem atualizados
        nova_quantidade = int(instance.quantidade) + int(diferenca)# o sinal "+" - diferença sempre negativa
        novo_total_custo = nova_quantidade * instance.preco_custo
        novo_total_varejo = nova_quantidade * instance.preco_varejo       
     
        # Realizando a atualização com os novos valores.
        atualizando_estoque = EstoqueModel.objects.filter(usuario=user, unidade=unid,
        produto=produto_form).update(quantidade=nova_quantidade,
        total_varejo=novo_total_varejo , total_custo=novo_total_custo)

               
    def acresce_db_estoque(self,user, unid, produto_form, form_quantidade):
       #user = usuario , unid = unidade
       
        ''' O método realiza ajustes no estoque adicionado a quantidade 
        que lhe foi subtraido na venda. Aqui ocorrem correções nos registros 
        de de saidas que foram acometidos erroneamente.
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
       

    def percent_lucro(self, user,unid):
        """
        O método calcular a margem de lucro total do estoque.
        Args:
            user - ususario, 
            unid - unidade
        
        Return: 
            porcentagem de lucro  total do estoque.
          
            """
        
        instance = EstoqueModel.objects.filter(usuario=user, unidade=unid)
        

        lista_lucro = []
        lista_custo = []
        total_varejo = 0
        for produto in list(instance):
            

            varejo = produto.total_varejo
            custo = produto.total_custo
            lucro = varejo - custo

            lista_lucro.append(lucro)
            lista_custo.append(custo)
            
        total_custo = sum(lista_custo)
        total_lucro = sum(lista_lucro)       

        
        porcento_lucro = float(total_lucro*100 /total_custo)

        
        return np.around(porcento_lucro, decimals=2), total_lucro
    

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
    criado_em = models.DateTimeField(verbose_name='Criado em',auto_now_add=True)
    status = models.CharField(verbose_name='Stuatus',max_length=25,default='pendente')
    
    def gera_pdf_(self,user, unid, aluno):        
        # Realize o queryset
        query = DebitoModel.objects.filter(usuario=user, unidade=unid, aluno=aluno,status='pendente')

        # Crie um buffer de bytes para armazenar o PDF
        buffer = io.BytesIO()

        # Crie um documento PDF
        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Adicione os dados do queryset como texto formatado ao PDF
        data_text = []
        for objeto in query:
            data_text.append(
                            f"{objeto.data}"
                            f" {objeto.produto}"
                            f"Valor unitário {objeto.valor_unitario}"
                            f"Quantidade: {objeto.quantidade}"
                            f"Valor total: {objeto.valor_total}\n"
                            
                            )

        # Junte todas as linhas em uma única string
        data_text = ''.join(data_text)

        # Adicione um parágrafo ao PDF com os dados formatados
        style = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=12,
            spaceBefore=0.5 * inch,  # Espaço na borda superior (por exemplo, 0.5 polegadas)
            alignment=1,  # Alinhamento central
        )
        p = Paragraph(data_text, style)
        elements.append(p)

        # Construa o PDF
        pdf.build(elements)

        # Retorne o PDF como resposta HTTP
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="resultado_queryset.pdf"'
        response.write(buffer.getvalue())
        buffer.close()
        return response


    def gera_pdf(self,user, unid, aluno):        

        # Realize o queryset
        
        query = DebitoModel.objects.filter(usuario=user, unidade=unid, aluno=aluno,status='pendente')

        # Crie um buffer de bytes para armazenar o PDF
        buffer = io.BytesIO()

        # Crie um documento PDF
        # pdf = SimpleDocTemplate(buffer, pagesize=letter)
        # elements = []

        # Ajuste as margens do documento PDF
        pdf = SimpleDocTemplate(buffer, pagesize=letter,
            rightMargin=20, leftMargin=20,
            topMargin=20, bottomMargin=20)  # Margens menores para expandir o conteúdo
        elements = []

        # Cabeçalhos da tabela
        headers = ["Data", "Produto", "Valor unitario", "Quantidade",  "Total", ]

        # Adicione os cabeçalhos à lista de dados
        data = [headers]
        total = 0
        # Adicione os dados do queryset à tabela no PDF
        for objeto in query:
            if objeto.data:
                objeto.data = datetime.datetime.strftime(objeto.data,'%d/ %m/%Y')
            elif objeto.valor_total:
                objeto.valor_total = int(objeto.valor_total)
            total = total + int(objeto.valor_total)   
            data.append([objeto.data, objeto.produto, objeto.valor_unitario,
            objeto.quantidade, objeto.valor_total])

        table = Table(data)       

        # Estilize a tabela
        style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),  # Fundo branco para o cabeçalho
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Cor do texto do cabeçalho
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Alinhamento central para o cabeçalho
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fonte em negrito para o cabeçalho
        ('FONTSIZE', (0, 0), (-1, -1), 12),  # Tamanho da fonte para toda a tabela
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaçamento inferior do cabeçalho
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Fundo branco para as linhas de dados
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Cor do texto para as linhas de dados
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),  # Alinhamento central para as linhas de dados
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Fonte normal para os dados
        ('LEFTPADDING', (0, 0), (-1, -1), 10),  # Espaçamento à esquerda para todas as células
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),  # Espaçamento à direita para todas as células
        ('TOPPADDING', (0, 0), (-1, -1), 10),  # Espaçamento superior para todas as células
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),  # Espaçamento inferior para todas as células
    ])               

        table.setStyle(style)
        elements.append(table)

        # Estilize o parágrafo
        paragraph_style = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=12,
            spaceBefore=0.5 * inch,  # Espaço na borda superior (por exemplo, 0.5 polegadas)
            alignment=1,  # Alinhamento central
        )
        

        # Adicione um parágrafo ao PDF        
        p = Paragraph("Total dos lanches de {}: {},00".format(aluno,total), paragraph_style)
        l_inf  = Paragraph('========================================================================================')

        elements.append(p)  
        elements.append(l_inf)      

        # Construa o PDF
        pdf.build(elements)

        # Retorne o PDF como resposta HTTP
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="consumo_cantina.pdf"'
        response.write(buffer.getvalue())
        buffer.close()
        return response

    
    def atualiza_db_debito(self,unid,user,produto_form,data_form,quantidade_form,aluno_form):
       
        '''
        O método realizar as atualizações  nos campo "quantidade" 
        e "valor_total" do modelo.
        '''        
        existe_registro = DebitoModel.objects.filter(usuario=user,unidade=unid,aluno=aluno_form,
        produto=produto_form, data=data_form).exists()

        if existe_registro:
            registro_debito = DebitoModel.objects.get(usuario=user, unidade=unid, 
            aluno=aluno_form, data=data_form, produto=produto_form,status='pendente')
            nova_quantidade = registro_debito.quantidade + quantidade_form 
            novo_valor_total = registro_debito.valor_total + (quantidade_form*registro_debito.valor_unitario)
            atualizar = DebitoModel.objects.filter(usuario=user, unidade=unid,
            aluno=aluno_form, produto=produto_form, data=data_form).update(
            quantidade=nova_quantidade,valor_total=novo_valor_total)  

    # def gerador_de_codigo(self):
    #     '''Esta método utiliza o utimo id gerado no próprio modelo, DebitoModel, com 
    #      um dos elementos para construir números sequências.
            
    #     '''
    #     id_code = DebitoModel.objects.aggregate(Max('id'))['id__max']
    #     if id_code == None:
    #         codigo = 1 # Se a tebela não possuir registros
    #         return codigo
    #     codigo = id_code + 1 #--> valor para o campo código

    #     return codigo
          
   
    def gerentec(self,unid,user,aluno_form,
        produto_form, quantidade_form, data_form, valor_unitario_form):

        """O método estabelece  critérios para a criação ou somenete 
        a atualização do registro de débito. O método retorna um dicionário cuja 
        a chave "sucesso" possui valor boleano.
         """
        
        cadastro_debito = DebitoModel(
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
            produto=produto_form, data=data_form,status='pendente').exists():
            quary_set = DebitoModel()
            atualiza = quary_set.atualiza_db_debito(
                unid,
                user, 
                produto_form,
                data_form,quantidade_form,
                aluno_form
            )        
        else: # Realizando um  registro completo do produto na tabela.
            
            cadastro_debito.save()
        # quary_set = DebitoModel()

        contexto = {
            'sucesso':True,
        }  
        return contexto


    
      
    
    
    def __str__(self):
        return self.aluno


class HistoricoDebitoModel(models.Model):
 
    # arquivo = models.FileField()
    usuario = models.CharField(verbose_name='Usuáiro',max_length=25,null=True, blank=True)
    unidade = models.CharField(verbose_name='Unidade',max_length=25, null=True, blank=True)     
    aluno =  models.CharField(verbose_name='Aluno', max_length=25)
    produto =  models.CharField(verbose_name='Produto', max_length=25)
    valor = models.DecimalField(verbose_name='Valor',max_digits=5,decimal_places=3)
    data = models.DateField(verbose_name='Data')
        
   


    def __str__(self):
        return self.aluno


class FuncionarioModel(models.Model):
    
    usuario = models.CharField(verbose_name='Usuáiro',max_length=25,null=True, blank=True)
    unidade = models.CharField(verbose_name='Unidade',max_length=25, null=True, blank=True) 
    funcionario = models.CharField(verbose_name='Funcionário',max_length=25)
    telefone = models.CharField(verbose_name='Telefone', max_length=25)
    criado_por = models.ForeignKey('auth.User', models.SET_NULL, null=True, blank=True)

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
        Este método é realizar correções nos registros de venda.

        Args:

            user: usuário,
            unid: unidade,
            produt_corrigir: produto que é incicializado, no formulário, para a correção,
            produt_edit: produto final para a correção,
            quant_inicio: quantidade do produto incializado para correção,
            quant_final: quantidade fornecida para correção,
            date: data do registro           

            unic: True -  indica que irá ter apenas um produto a ser corrigido

            delete: True - indica que a quantidade do produto na correção            
            irá zerá e que o mesmo deverá ser deleteado

            update: True - irá ocorrer atualização do produto e seus valores.

        """  

        user = kwargs.get('usuario')
        unid = kwargs.get('unidade')
        pro_corrig = kwargs.get('pro_corrig')
        pro_edit = kwargs.get('pro_edit')
        date = kwargs.get('date')
        quant_inicio = kwargs.get('quant_inicio')
        quant_final = kwargs.get('qut_form')
        unic = kwargs.get('unic')
        update = kwargs.get('update')

        
        

        # "Deletetando o registro zerado na conrreção"
        if kwargs.get('delete'):

            # encontrando a instância a ser deletada.            

            delete_instance = CadastrosVendaModel.objects.get(
            usuario=user, unidade=unid, produto=pro_corrig, data=date).delete()
    
            # Edite a nova quantidade para o produto corrigido:
            
                # encontrando a instância a editar
            produto_edit = CadastrosVendaModel.objects.get(usuario= user, unidade=unid ,
            produto=pro_edit ,data=date )

            # Alterar a quantidade
            quant_edit = produto_edit.quantidade + int(quant_final)
            total_valor = quant_edit * produto_edit.valor_unitario
            
            # atualizando                       
            atualizar = CadastrosVendaModel.objects.filter(usuario=user,
            unidade=unid, data=date, produto=produto_edit).update(quantidade=quant_edit,valor_total=total_valor)
        
        elif kwargs.get('update'):
            
            product = CadastrosVendaModel.objects.get(usuario= user, unidade=unid,
            produto=pro_edit ,data=date )
            quant_edit = quant_final
            total_valor =  int(quant_final) * Decimal(product.valor_unitario)

            atualizar = CadastrosVendaModel.objects.filter(usuario=user,
            unidade=unid, data=date, produto=pro_edit).update(quantidade=quant_edit,valor_total=total_valor) 
        


        elif unic:        
            
            # encontrando a instância a editar
           

            unic_produt = CadastrosVendaModel.objects.get(usuario= user, unidade=unid,
            produto=pro_corrig ,data=date)
        
            # Ajustando o valor total.
            new_total = int(quant_final) * int(unic_produt.valor_unitario)
            
            # atualizando 
                              
            atualizar = CadastrosVendaModel.objects.filter(usuario=user,
            unidade=unid, data=date, produto=unic_produt).update(quantidade=quant_final,valor_total=new_total)
        

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
                    quant_corrigida = int(quant_final)
                    valor_final = quant_corrigida * instance_produt.valor_unitario

                # Novo produto para atualização       
                else:
                    dif = int(quant_inicio) - int(quant_final)
                    
                    quant_corrigida = instance_produt.quantidade + dif
                    valor_final = quant_corrigida * instance_produt.valor_unitario

                # atualizando 
                
                atualizar = CadastrosVendaModel.objects.filter(usuario=user,
                unidade=unid, produto=produt).update(quantidade=quant_corrigida,valor_total=valor_final)
    
       

    def pesquisa_data(user,unid,data_pesquisa):
        # user = usuário, unid = unidade
        """ O método realiza uma filtragem em função da data."""


        query = CadastrosVendaModel.objects.filter(usuario=user,unidade=unid,
        data=data_pesquisa).values('produto', 'quantidade','valor_unitario',
        'valor_total', 'data')
        
        total = CadastrosVendaModel.objects.filter(usuario=user,unidade=unid,
        data=data_pesquisa).aggregate(
            quantidade_total=Sum('quantidade'),
            valor_total=Sum('valor_total')
            )
        quantidade_total = total['quantidade_total']
        valor_total = total['valor_total']
      
        return query, quantidade_total, valor_total
    

    def inter_data(data_inicio):
        """
        O método realiza uma filtragem baseado  na data de referência, informada pelo 
        usuário, e retorna um queryset como resultado da solicitação.

        """
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
        '''Realizar atualizações de valores para os campos "quantidade"
          e "valor_total" no modelo CadastroVendaModel.'''
        
        # Checagem de registro da venda do produto para a data especificada
        existe_registro = CadastrosVendaModel.objects.filter(usuario=user,
        unidade=unid, produto=produto, data=data).exists()
       
        if existe_registro:
           
            # Indentificando a instância
            registro_venda = CadastrosVendaModel.objects.get(usuario=user, unidade=unid,
            data=data,produto=produto)          
           

            # acrescentamos a quantidade do produto vendito a quantidade existente no banco.
            nova_quantidade = registro_venda.quantidade + Decimal(quantidade )
            
            # Definição do valor total
            novo_valor = Decimal(registro_venda.valor_total) + (Decimal(quantidade) * registro_venda.valor_unitario)
            # Realizando as atualizações
            atualizar = CadastrosVendaModel.objects.filter(usuario=user,unidade=unid,produto=produto, data=data).update(quantidade=nova_quantidade,valor_total=novo_valor) 
           
   
    def update_venda_estoque(self,user, unid, produto,data,quantidade_form,quantidade_inicial):
       
        ''' Este método realiza as correções de saidas e entradas
        de produtos no estoque decorrentes de vendas ou atualizações da mesma.
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
    
  

    def gerentec(self,user,unid,produto,quantidade,data,valor_unidade):

        """ 
        Este método estabelece o critério para salvar um "registro completo 
        na data base de vendas ou salvar de forma parcial, neste caso,a atualização 
        ocorrerá apenas nos campos quantidade e valor_total.
        
        Args:
            user (usuário),
            unidade = (unidade),
            produto (produto para pesquisa)
            quantidade(quantidade do produto)
            data(data de venda)
            valor_unitário(valor unitário do produto)
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
        
        """
        O método é responsável por relaizar atualizações nos
        registros de vendas que ocorrem em paralelo no registro de estoque.
        
        Args:

            user: usuário,
            unid: unidade,
            produt_corrigir: produto que é incicializado, no formulário, para a correção,
            produt_edit: produto apontado no formulário para ter a quantidade corrigida,
            quantidade_incial: quantidade inicializada do produt_corrigir,
            data: data em que ocorreu o registro
        
        O método ainda retorna um dicionário cuja chave "quant_superior" tem o valor 
        boleno True - ocorre sempre que a "quantidade incial" for inferior a final.

        Os métodos responsáveis por atualizações no banco de dados de vendas e do estoque 
        são repectivamente:
            acress e o corrig_db_estoque.       
       
         """
       
            
        if int(quantidade_inicial) >= int(quantidade_form):

            # Quando o produto "inicializado" difere do produto "final" na autualição.            
            if produt_corrigir != produt_edit:

                # Corrigindo a tabela de vendas.
                vendas_model = CadastrosVendaModel()                
                
                dif_quant = int(quantidade_inicial) - int(quantidade_form)         

                # Quando a correção zerar a quantidade do produto na data especificada no registro de vendas.
                if dif_quant <= 0 :

                    # Atualizando o banco de dados de registro de vendas.      
                    atualizar_vendas = CadastrosVendaModel().acres(usuario=user,unidade=unid,
                    pro_corrig=produt_corrigir, pro_edit=produt_edit,quant_inicio=quantidade_inicial,
                    qut_form=quantidade_form, date=data, delete=True
                    )  

                    
                    # Atualizando o banco de dados do estoque: 
                    atualizar = EstoqueModel().corrig_db_estoque( usuario=user,unidade=unid, 
                    produt_inicial=produt_corrigir, produt_final=produt_edit,quant_editada=quantidade_form )
            
                # Quando a correção não zera a quantidade do produto na data especificada no registro de vendas. 
                else:

                # Atualizando registro de vendas.
                    atualiza_vendas = CadastrosVendaModel().acres(
                    usuario=user,unidade=unid, pro_corrig=produt_corrigir,
                    pro_edit=produt_edit, qut_form=quantidade_form,quant_inicio=quantidade_inicial, date=data
                    )             

                    # Atualizando os registros no estoque.
                    atualiza_estoque =  EstoqueModel().corrig_db_estoque( usuario=user,unidade=unid, 
                    produt_inicial=produt_corrigir, produt_final=produt_edit,quant_editada=quantidade_form )
            else:
                # Atualizando o registro no cadastro de venda. 
                vendas_model = CadastrosVendaModel().acres(
                usuario=user,unidade=unid, pro_edit=produt_edit, 
                qut_form=quantidade_form,quant_inicio=quantidade_inicial,
                date=data, update=True
                )             
            # Atualizando o registro no cadastro de estoque.  
                atualiza_estoque = EstoqueModel().corrig_db_estoque( usuario=user,unidade=unid, 
                produt_inicial=produt_corrigir,quant_editada=quantidade_form,
                quant_inicio=quantidade_inicial ,unic=True )

        # Atualização apenas para um único produto.
        elif produt_corrigir == produt_edit:           
           
            # Atualizando o registro no cadastro de venda. 
            vendas_model = CadastrosVendaModel().acres(
                usuario=user,unidade=unid, pro_edit=produt_edit, 
                qut_form=quantidade_form,quant_inicio=quantidade_inicial,
                date=data, update=True
                )             
            # Atualizando o registro no cadastro de estoque.  
            atualiza_estoque = EstoqueModel().corrig_db_estoque( usuario=user,unidade=unid, 
                produt_inicial=produt_corrigir,quant_editada=quantidade_form,
                quant_inicio=quantidade_inicial ,unic=True )
            
        # "Exceção - quantidade incial inferior a final."
        elif int(quantidade_inicial) < int(quantidade_form):
        
            
            contexto = {
                'quant_superior': True
                  } 

            return  list(contexto.keys())[0]
        
        
       
        
    def __str__(self):
        return self.produto
   

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
    

class ModelAluno(models.Model):
   
    usuario = models.CharField(verbose_name='Usuáiro',max_length=25)
    unidade = models.CharField(verbose_name='Unidade',max_length=25) 
    nome = models.CharField(verbose_name='Nome',max_length=25)
    turma = models.CharField(verbose_name='Turma',max_length=20,)
    responsavel = models.CharField( verbose_name='Responsavel',max_length=25)
    tel_responsavel = models.CharField(verbose_name='Contato do responsável',max_length=25)

    def __str__(self):
        return self.nome   