import re
import datetime
from collections.abc import Mapping
from typing import Any
from django import forms
from django.forms.utils import ErrorList


from cadastro.models import AlunoModel, CadastrosVendaModel, CategoriaProdutoModel, DebitoModel, EstoqueModel, ModelAluno

class FormUpdateDebitoModelAluno(forms.Form):
    nome_atual = forms.CharField(label='Aluno',max_length=25)   
    codigo = forms.CharField(label='Código',max_length=25)    
    update_novo_nome = forms.CharField(label='Aluno para update',max_length=25)   
    
    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']       
        if not DebitoModel.objects.filter(codigo=codigo).exists():
            raise forms.ValidationError("Não existe registro com o código {}. Informe um código válido.".format(codigo))
        return codigo 
    
    def clean_nome_atual(self):        
        nome_atual = self.cleaned_data['nome_atual']               
        if not AlunoModel.objects.filter(nome=nome_atual).exists():
            raise forms.ValidationError("Não existe registro com o nome de {}. Digite um nome válido.".format(nome_atual))
        else:
            aluno = AlunoModel.objects.get(nome=nome_atual)
            if not DebitoModel.objects.filter(aluno=aluno.id).exists():                
                raise forms.ValidationError("Não foi encontrado débito para {}".format(nome_atual))
            
        return nome_atual
    
    #-->O nome atualizado será retirado do modelo DebitoModel 
    def clean_update_novo_nome(self):
        nome_atual = self.cleaned_data['nome_atual']         
        nome_update = self.cleaned_data['update_novo_nome']               
        if not AlunoModel.objects.filter(nome=nome_update).exists():
            raise forms.ValidationError("Não existe registro com o nome de {}. Digite um nome válido.".format(nome_update))
        else:
            aluno = AlunoModel.objects.get(nome=nome_update)
            if not DebitoModel.objects.filter(aluno=aluno.id).exists():                
                raise forms.ValidationError("Não foi encontrado débito para {}".format(nome_update))
            elif nome_atual == nome_update:
             raise forms.ValidationError("Para atualizar digite um nome diferente de {}".format(nome_update))   
        return nome_update




class FormUpadateDebitoModelProduto(forms.Form):
    produto_exitente = forms.CharField(label='Produto',max_length=25)
    update_nome_produto = forms.CharField(label='Produto para update',max_length=25)

    def clean_produto_exitente(self):        
        nome_produto = self.cleaned_data['produto_exitente']        

        if not EstoqueModel.objects.filter(produto=nome_produto).exists():
            raise forms.ValidationError("Não existe registro com o nome de {}".format(nome_produto))
        else:
            produtos = EstoqueModel.objects.get(produto=nome_produto)
            if not DebitoModel.objects.filter(produto=produtos.id).exists():                
                raise forms.ValidationError("Não foi encontrado débito para {}".format(nome_produto))
        return nome_produto   


    def clean_update_nome_produto(self):        
        produto_update = self.cleaned_data['update_nome_produto']             
        nome_produto = self.cleaned_data['produto_exitente'] 

        if not EstoqueModel.objects.filter(produto=produto_update).exists():
            raise forms.ValidationError("Não existe registro com o nome {}. Digite o produto válido.".format(produto_update))
        elif produto_update == nome_produto:  
             raise forms.ValidationError("Os produtos não devem ser os mesmos para validação. Digite um produto válido.")
        return produto_update   




class FormUpdateEstoque(forms.ModelForm):
    """"
    Formulário populado com os dados do estoque a serem editados.
    
    * Observação: 
        foi necessário apresentar o campo "produto" como campo oculto 
        e em paralelo criar um campo (campo_oculto) inicializado com
        o valor do campo produto para edita-lo e devolver a alteração 
        feita  ao campo produto no momento do update.
        Manobra necessária devido a problemas para editar o 
        campo produto diretamente - presume-se que seja o fato deste 
        campo "representar" o modelo EstoqueModel no método "__str__".

    """

   # criamos um campo oculto e opcional para o produto
    produto = forms.CharField(widget=forms.HiddenInput(), required=False)

   
    campo_oculto = forms.CharField(label='Produto',max_length=25)
    
    class Meta:
        model = EstoqueModel
        fields = ['campo_oculto','produto','quantidade','preco_varejo','preco_custo'] 
        labels ={'produto':'*Para alterar o produto click abaixo em "Alterar produto" ',} 


        
    def __init__(self, *args, **kwargs):
        
        self.usuario = kwargs.pop('usuario')        
        self.unidade = kwargs.pop('unidade')
        super(FormUpdateEstoque, self).__init__(*args, **kwargs)
        
        # Preencha o campo produto_original com o valor atual do campo produto
        if self.instance:
            self.fields['campo_oculto'].initial = self.instance.produto 

      
        self.fields['categoria'] = forms.ModelChoiceField(
        queryset=CategoriaProdutoModel.objects.filter(unidade=self.unidade, usuario=self.usuario),
        to_field_name='categoria',  
        empty_label="Selecione uma categoria",

    )  




class FormUpdateEstoquePorProduto(forms.Form):    

    """Formulário para a pesquisa do produto a ser atualizado no estoque."""


    produto = forms.CharField(label='Produto',max_length=25)

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario')
        self.unidade = kwargs.pop('unidade')
        super(FormUpdateEstoquePorProduto,self).__init__(*args, **kwargs)

    # Checando a existência do produto.  
    def clean(self):
        produt = self.cleaned_data.get('produto')
        cleand_data = super().clean()

        if not EstoqueModel.objects.filter(usuario=self.usuario,
        unidade=self.unidade,produto=produt):
            raise forms.ValidationError('Produto inválido, não encontrado nos registros.')




class UpdateAlunoFormPesquisa(forms.Form):

    nome_aluno = forms.CharField(label='Nome', max_length=25)

    def __init__(self, *args,**kwargs):

        self.usuario = kwargs.pop('usuario')
        self.unidade = kwargs.pop('unidade')
        super().__init__(*args, **kwargs)
    # Formulário de pesquisa aluno
    
    def clean(self):
        cleaned_data = super().clean()
        aluno = self.cleaned_data.get('nome_aluno')
        
        if not AlunoModel.objects.filter(
        usuario=self.usuario, unidade=self.unidade,nome=aluno).exists():
            raise forms.ValidationError("Nome inválido, não cadastrado.")
        return cleaned_data
       



class UpdateAlunoForms(forms.ModelForm):
   # Formulário do aluno populado com dados da instâcia.    
    
    # criamos um campo oculto e opcional para o produto
    nome = forms.CharField(widget=forms.HiddenInput(), required=False)
   
    # este campo recebe 
    clone_fild_name = forms.CharField(label='Nome',max_length=25)


    class Meta:
        model = AlunoModel
        fields = ['clone_fild_name','nome','turma', 'responsavel','telefone_responsavel']

    def __init__(self, *args, **kwargs):
       
        super().__init__(*args, **kwargs)
        
        if self.instance:
            self.fields['clone_fild_name'].initial = self.instance.nome
            
  


class UpdateVendasformPesquisa(forms.ModelForm):
    """
    Este fomulário realiza a pesquisa para a indetificação  
    do registro de vendas.

    Raise:
        forms.Validations - 
        * se o produto informado não for encontrado nos cadastros, 

        * se não houver registro da venda do produto na data especificada,
        
        *se a data informada não estiver no formato esperado.

    """
    
    class Meta:
        model = CadastrosVendaModel
        fields = ['produto','data']
        labels = {
            'data': '*Infomr a data da venda'
            }
        

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario')
        self.unidade = kwargs.pop('unidade')
        super().__init__(*args, **kwargs)

    # Validações.  
    def clean(self):
        data_form = self.cleaned_data.get('data')
        produto_form = self.cleaned_data.get('produto')
        clean_data = super().clean()

        # Validações do produto
        if not EstoqueModel.objects.filter(usuario=self.usuario, 
            unidade=self.unidade, produto=produto_form).exists():
                raise forms.ValidationError(f'''Digite um produto váldo,                                             
                não houve venda de {produto_form} neste data.''') 
        
        elif not CadastrosVendaModel.objects.filter(usuario=self.usuario, 
            unidade=self.unidade, produto=produto_form, data=data_form).exists():
                # if not data_form == None:
                    # data_formatada = datetime.datetime.strftime(data_form, '%d/%m/%Y')

                raise forms.ValidationError(f'''Não encontrado venda de {produto_form}
                na data especificada.''') 
        
        # Validações de data
        elif not data_form == None:
           
            if not CadastrosVendaModel.objects.filter(data=data_form).exists():
                raise forms.ValidationError('Não existe registro de venda para esta data.')
        
        else:
            raise forms.ValidationError('''Data inválida.
            Formato esperado, exemplo: "00/00/0000 (mês/dia/ano).     
            '''
            )
  


   
class UpdateVendasForm_(forms.ModelForm): 

 # FORMULÁRIO UpdateVendasForm - POPULADO COM OS DADOS DA INSTÂNCIA 

    # Campo oculto e opcional para o produto
    produto = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    # Campo oculto e opcional para quantidade.
    quantidade_inicial = forms.CharField(widget=forms.HiddenInput(), required=False)
   

    # este campo é inicializado com o valor do campo produto
    # recebe_produto = forms.CharField(label='Edite o produto,*OPCIONAL',max_length=25)

   
    # O campo Quantidade será somente para leitura do usuário
    quantidade = forms.CharField(
        label='*Edite aqui a quantidade total para data referente.*OPCIONAL.',max_length=25
        )

    
    class Meta:
        model = CadastrosVendaModel
        fields = ['produto','quantidade','valor_unitario','data']    
    
    
    # Inicializador  
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario')
        self.unidade = kwargs.pop('unidade')
        super().__init__(*args, **kwargs)
        #tornando os campo "valor_unitario" e "data" para somente leitura
        self.fields['valor_unitario'].widget.attrs['readonly'] = True
        self.fields['data'].widget.attrs['readonly'] = True
        

        self.fields['recebe_produto'] = forms.ModelChoiceField(
            queryset=EstoqueModel.objects.filter(usuario=self.usuario,
            unidade=self.unidade) , 
            to_field_name='produto',
            empty_label='Selecione produto',      
        )


        # icializar o campo "receber_produtot" e quantidade_inicial com os valores atuais da tabela tratada.
        if self.instance:
            self.fields['recebe_produto'].initial = self.instance.produto 
            self.fields['quantidade_inicial'].initial = self.instance.quantidade
    



class UpdateVendasForm(forms.ModelForm):
    
    """ Formulário populado com os dados da intância a ser atualaizada. """     

    # Campo oculto e opcional para o produto
    # produto = forms.CharField(widget=forms.HiddenInput(), required=False)
    produto = forms.CharField(
        label='*Produto indicado para correção',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)


    field_clone = forms.CharField(max_length=25)

    # Campo oculto e opcional para quantidade.
    quantidade_inicial = forms.CharField(widget=forms.HiddenInput(), required=False)

    
    quantidade = forms.CharField(
        label='*Quantidade para o produto de troca.*OPCIONAL.',max_length=25
    )

    class Meta:
        model = CadastrosVendaModel
        fields = ['produto','field_clone', 'quantidade', 'valor_unitario', 'data']    

    
    # Inicializador  
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario')
        self.unidade = kwargs.pop('unidade')
        super().__init__(*args, **kwargs)
        self.fields['valor_unitario'].widget.attrs['readonly'] = True
        self.fields['data'].widget.attrs['readonly'] = True

        self.fields['field_clone'] = forms.ModelChoiceField(
            label='*Selecione o produto para troca',           
            queryset=EstoqueModel.objects.filter(usuario=self.usuario,
            unidade=self.unidade).order_by('produto') , 
            to_field_name='produto',
             empty_label='Selecione produto',                       
        )       

        # Inicializar o campo "quantidade_inicial" com o valor atual da instância
        if self.instance:
            self.fields['quantidade_inicial'].initial = self.instance.quantidade
            self.fields['field_clone'].initial = self.instance.produto




class UpadatePesquisaRegistroAluno(forms.ModelForm):
    # Fomulário de pesquisa para update de registro do aluno.
    class Meta:
       model = ModelAluno
       fields = ['nome']

    
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario')
        self.unidade = kwargs.pop('unidade')
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'placeholder':'*Informe aluno para atualização.'})


    def clean(self):
        nome_aluno = self.cleaned_data['nome']
        cleaned_data  = super().clean()

        if not ModelAluno.objects.filter(usuario=self.usuario, 
        unidade=self.unidade, nome=nome_aluno).exists():
            raise forms.ValidationError(f'Nome inválido, {nome_aluno} não se encontra em nossos registros.')
    

       

class UpdateCadastroAluno(forms.ModelForm):

    # Formulário para registro do aluno.
    
    nome = forms.CharField(widget=forms.HiddenInput(), required=False)
    clone_fild_name = forms.CharField(label='Aluno',max_length=25)

    class Meta:
        model = ModelAluno
        fields = ['clone_fild_name','nome', 'turma', 'responsavel', 'tel_responsavel']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields['clone_fild_name'].initial = self.instance.nome
    

class UpdatePesquisaDebito(forms.ModelForm):

    # Fomulário para pesquisa de débito do aluno

    data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = DebitoModel
        fields = ['aluno','produto','data']

   
    def __init__(self, *args, **kwargs):
        
        self.usuario = kwargs.pop('usuario')
        self.unidade = kwargs.pop('unidade')
        super().__init__(*args, **kwargs)
        self.fields['produto'] = forms.ModelChoiceField(
            queryset=EstoqueModel.objects.filter(usuario=self.usuario, unidade=self.unidade).order_by('produto'),
            to_field_name='produto',
            empty_label='Seleciono um produto',
        )

    



class UpdateDebito(forms.ModelForm):
    
    # Fomulário populado com os dados da instância.
    clone_fild_name = forms.CharField(label='Aluno',max_length=25)
    aluno = forms.CharField(widget=forms.HiddenInput())


    data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = DebitoModel
        fields = ['clone_fild_name','aluno','produto','valor_unitario','quantidade','data']

    def __init__(self,*args, **kwargs):
        self.usuario = kwargs.pop('usuario')
        self.unidade = kwargs.pop('unidade')
        super().__init__(*args,**kwargs)
        
        # self.fields['produto']= forms.ModelChoiceField(
        #         label='*Selecione um produto',           
        #         queryset=EstoqueModel.objects.filter(usuario=self.usuario, unidade=self.unidade,
        #         ).order_by('produto') , 
        #         to_field_name='produto',
        #         empty_label='Selecione produto',                       
        #     )

        if self.instance:
            self.fields['clone_fild_name'].initial = self.instance.aluno
            # self.fields['data'].initial = self.instance.data
    