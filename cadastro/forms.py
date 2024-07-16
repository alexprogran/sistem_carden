
import re
from django import forms
# from flask.typing import ResponseValue
from .models import  ( AlunoModel,DebitoModel, CategoriaProdutoModel,
DebitoModel, FuncionarioModel, EstoqueModel, ModelAluno, UnidModel)


class AlunosForms(forms.ModelForm):
    """
    Fomulário para cadastro de aluno.

    """
    class Meta:
        model = AlunoModel
        fields = ['nome','turma','responsavel','telefone_responsavel']

    
    # Resgatando o usuário e a unidade da view
    def __init__(self,*args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        self.unidade = kwargs.pop('unidade', None)
        super().__init__(*args,**kwargs)

       
            
    # Validações.
    def clean(self):
        cleaned_data = super().clean()
        telefone = self.cleaned_data['telefone_responsavel']
        nome = cleaned_data.get('nome')

        
        # Validando campo aluno
        if  ModelAluno.objects.filter(usuario=self.usuario,
            unidade=self.unidade,nome=nome).exists():
            campo = nome                  
            raise forms.ValidationError(
            f"""{nome} já consta em nossos cadastos."""
            )
            
        # Validando campo telefone
        elif not re.match(r'^\d{2}-\d+$', telefone): 

            raise forms.ValidationError(
            """*Telefone inválido, este exemplo "99-999999999"  é a 
                formatação esperada para o campo telefone.
            """)


class EstoqueFomModel(forms.ModelForm):

    """ Fomulário de cadastro de produto no estoque."""
    
    class Meta:
        model = EstoqueModel
        fields = ['produto','quantidade','preco_varejo','preco_custo','categoria']

    def __init__(self, *args, **kwargs):
        # Recupera o usuário da sessão ao inicializar o formulário
        
        self.usuario = kwargs.pop('usuario', None)
        self.unidade = kwargs.pop('unidade',None)
        super(EstoqueFomModel, self).__init__(*args, **kwargs)
       
    # Adiciona o campo ao formulário com base no usuário da sessão
       
        if self.usuario:
           
            self.fields['categoria'] = forms.ModelChoiceField(
            queryset=CategoriaProdutoModel.objects.filter(usuario=self.usuario,unidade=self.unidade), 
            to_field_name='categoria',          
            empty_label="Selecione uma categoria")
        
    def clean_produto(self):
        produto_form = self.cleaned_data['produto']
        existe_produto = EstoqueModel.objects.filter(
            produto=produto_form,usuario=self.usuario, unidade=self.unidade).exists()
        if existe_produto:
             raise forms.ValidationError(f'Produto inválido, este produto já foi cadastrado. ')
        return produto_form

    def clean_categoria(self): # Caso a tabela de categoria estaja vazia, é gerado um exceção.
        categoria = self.cleaned_data['categoria']
        if categoria == None:
            raise forms.ValidationError('Comando inválido. Cadastre pelo menos uma categoria')
        return categoria    


class FuncionarioModelForm(forms.ModelForm):
    
    """
    Formulário para cadastro de funcionáro.

    Raise:
        forms.Validations.Erros - caso o nome para cadastro do
        funcionário já exista nos registros ou se o telefone 
        informado par cadastro não esteja no formato esperado.
      
     """    
    
    class Meta:
        model = FuncionarioModel
        fields = ['funcionario','telefone']

        # Inicializar o formulário com o usuario e unidade .
    def __init__(self, *args,**kwargs):
        self.usuario = kwargs.pop('usuario',None)
        self.unidade = kwargs.pop('unidade',None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        funcionarios = self.cleaned_data['funcionario']
        telefone = self.cleaned_data['telefone']
        
        # Validando campo funcionário.
        if  FuncionarioModel.objects.filter(usuario=self.usuario,
            unidade=self.unidade,funcionario=funcionarios).exists():
                              
            raise forms.ValidationError(
            f"""Olá {self.usuario}, {funcionarios} já consta nos registros 
            de funcionários.
            """
            )
            
        # Validando campo telefone
        elif not re.match(r'^\d{2}-\d+$', telefone): 

            raise forms.ValidationError(
            """*Telefone inválido, este exemplo "99-999999999"  é a 
                formatação esperada para o campo telefone.
            """)


class CadastroDebitoFormModel(forms.ModelForm):

    """Formulário para cadastro de valores em aberto."""

    data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))     

    class Meta:
        model = DebitoModel
        fields = ['aluno','produto','quantidade','data']

        

    # Inicializar o formulário com o usuario e unidade .
    def __init__(self, *args,**kwargs):
        self.usuario = kwargs.pop('usuario',None)
        self.unidade = kwargs.pop('unidade',None)
        super().__init__(*args, **kwargs)
       
        self.fields['produto'] = forms.ModelChoiceField(
            queryset=EstoqueModel.objects.filter(usuario=self.usuario,
            unidade=self.unidade).order_by('produto'),
            to_field_name='produto',  
            empty_label="Selecione um produto",            
        )

        self.fields['aluno'] = forms.ModelChoiceField(
            queryset=ModelAluno.objects.filter(usuario=self.usuario,
            unidade=self.unidade).order_by('nome'),
            to_field_name='nome',
            empty_label="Selecione um cliente",

        )


    # def clean(self):
    #     cleaned_data = super().clean()
    #     nome_aluno = self.cleaned_data.get('aluno')
    #     data = self.cleaned_data.get('data')

    #     # Validando aluno
    #     if not ModelAluno.objects.filter(nome=nome_aluno,
    #     usuario=self.usuario, unidade=self.unidade).exists():
    #         raise forms.ValidationError('Aluno não encontrado em nosso registros')
        
    #     elif self.cleaned_data['produto'] == None:
    #         raise forms.ValidationError('Selecione um produto para o cadastro.')
                   
        # Validando data
        # elif not re.match(r'^\d{2}/\d{2}/\d{4}$',str(data)):
        #     raise forms.ValidationError(
        #     """*Data inválida, siga o exemplo para o formato esperado:
        #     12/12/0000
        #     """)
 

class CadastroVendaFormModel(forms.ModelForm):
    """ Fomulário para cadastro de vendas."""
   
    class Meta:
        model = DebitoModel
        fields =['produto', 'quantidade']  


    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        self.unidade = kwargs.pop('unidade', None)
        super().__init__(*args, **kwargs)


        self.fields['produto'] = forms.ModelChoiceField(
            queryset=EstoqueModel.objects.filter(usuario=self.usuario, unidade=self.unidade),
            to_field_name='produto',  
            empty_label="Selecione um produto",
        )


class CategoriaProdutoFormModel(forms.ModelForm):

    """ 
    O formúlario para cadastro de  produto.

    Raise:
        forms.Validations.Error - se a categoria informada para
        cadastro constar nos registros. 
    
    """

    class Meta:
        model = CategoriaProdutoModel
        fields = ['categoria']



    def __init__(self,*args,**kwargs):
        self.usuario = kwargs.pop('usuario')
        self.unidade = kwargs.pop('unidade')
        super().__init__(*args, **kwargs)

    def clean(self):
        campo_categoria = self.cleaned_data['categoria']
        cleaned_data = super().clean()

        if CategoriaProdutoModel.objects.filter(usuario=self.usuario,
        unidade=self.unidade,categoria=campo_categoria,).exists():

            raise forms.ValidationError(f"""
            Olá {self.usuario}, a categoria {campo_categoria} já foi 
            cadastrada, informe uma outra categoria para registro.
            
            """
            )           


class UnidModelForm(forms.Form):
    """
    Este fomulário para unidade.
    
    Raise:
        *forms.ValidationError: se o usuário não tiver cadastrado unidade
         para acesso ou se a unidade informada não for encontrada
         no banco de dados.
    
    """

    unidade = forms.CharField(label='Unidade',max_length=25)

    def __init__(self, *args, **kwargs):
        # Recupera o usuário da sessão ao inicializar o formulário
        self.usuario = kwargs.pop('usuario', None)
        
        super().__init__(*args, **kwargs)
        
    def clean(self):
        unid = self.cleaned_data['unidade']
        cleaned_data = super().clean()
        # Verificando se existe registros de unidade.
        quant_register_unid = UnidModel.objects.filter(usuario=self.usuario,
        ).count()        

        # Não existindo registro de unidade.
        if quant_register_unid == 0:
            raise forms.ValidationError( 
            f'''Olá {self.usuario}, você ainda não criou um unidade. 
            Faça clicando no batão abaixo "Criar unidade". '''
            )
        # Se a unidade não for encontrada
        elif not UnidModel.objects.filter(usuario=self.usuario,unidade=unid).exists():
            raise forms.ValidationError(f'''Olá {self.usuario}, você não 
                    cadastrou {unid} como uma de suas unidades.''')
    


class CreateUnidModelForm(forms.Form):

    """ 
    O formulário para cadastro de usuário.
    
    Raise: 
        forms.Validation.error - Se a unidade informada para 
        cadastro existir.
    
    """  



    unidade = forms.CharField(label='Unidade',max_length=25)

    def __init__(self, *args, **kwargs):
        # Recupera o usuário da sessão ao inicializar o formulário
        self.usuario = kwargs.pop('usuario', None)
        super(CreateUnidModelForm, self).__init__(*args, **kwargs)

    def clean(self):
      # Checa a unidade à ser criada evitando duplicações de unidade para usuário.   
        unidade = self.cleaned_data['unidade']  
             
        if  UnidModel.objects.filter(usuario=self.usuario, unidade=unidade).exists():
            raise forms.ValidationError(f'''Unidade inválida, {unidade} 
            é uma unidade já existente para esse usuário.''')
        
   

