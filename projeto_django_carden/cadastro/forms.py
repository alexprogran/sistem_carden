
import re
from django import forms
from flask.typing import ResponseValue
from .models import  (AlunoModel, DebitoModel, CategoriaProdutoModel,
DebitoModel, FuncionarioModel, EstoqueModel, TesteEstoqueModel, UnidModel, UsuariosModel)




class AlunoForms(forms.ModelForm):
    
    class Meta:
        model = AlunoModel
        fields = ['nome', 'turma', 'responsavel','telefone_responsavel']

    # Resgatando o usuário e a unidade da view
    def __init__(self,*args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        self.unidade = kwargs.pop('unidade', None)
        super(AlunoForms,self).__init__(*args,**kwargs)

    """
    *PROBLEMA: o implemento das validações abaixo, por algum 
     motivo  estão invalidando os dados, a view retorna um formulário vazio.
    a solução foi criar uma  validação "a nível de servidor".

    """ 

    # def clean_nome(self):
    #     cleaned_data = super().clean()
    #     nome_aluno = self.cleaned_data['nome'] 
       
    #     if AlunoModel.objects.filter(usuario=self.usuario,
    #     unidade=self.unidade, nome=nome_aluno).exists():                        
    #         raise forms.ValidationError('{} é um nome existente em nossos cadastros'.format(nome_aluno))
    #     return super().clean()
       
    # def clean_telefone_reponsavel(self):
    #     telefone = self.cleaned_data['telefone']
        
    #     # Utilizando uma expressão regular para verificar se o telefone contém apenas dígitos
    #     if not re.match(r'^\d{2}-\d+$', telefone):
    #         raise forms.ValidationError("Apenas dígitos exemplo: 71-99999999.")

    #     return telefone


class EstoqueFomModel(forms.ModelForm):
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
        
      
    
   
    
    
    # categoria = forms.ModelChoiceField(# O campo categoria "selecionável".
    #     ini= __init__(),
    #     queryset=CategoriaProdutoModel.objects.filter(usuario=__init__.self.user, unidade=__init__.self.unid),
    #     to_field_name='categoria',  
    #     empty_label="Selecione uma categoria",
    # )


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

    class Meta:
        model = FuncionarioModel
        fields = ['funcionario','telefone']


class CadastroDebitoFormModel(forms.ModelForm):
    """Formulário de cadastro de débito."""
    class Meta:
        model = DebitoModel
        fields = ['produto','quantidade','data']

    # Inicializar o formulário com o usuario e unidade .
    def __init__(self, *args,**kwargs):
        self.usuario = kwargs.pop('usuario',None)
        self.unidade = kwargs.pop('unidade',None)
        super(CadastroDebitoFormModel,self).__init__(*args, **kwargs)
       
        self.fields['produto'] = forms.ModelChoiceField(
            queryset=EstoqueModel.objects.filter(usuario=self.usuario,
            unidade=self.unidade),
            to_field_name='produto',  
            empty_label="Selecione um produto",
            required=False # este campo é opcional
        )
        self.fields['aluno'] = forms.ModelChoiceField(
            queryset=AlunoModel.objects.filter(usuario=self.usuario, 
            unidade=self.unidade),
            to_field_name='nome',  
            empty_label="Selecione um aluno",
            required=False
            )     

    def clean_produto(self):
        produto = self.cleaned_data['produto']
        registro = EstoqueModel.objects.filter(
        usuario=self.usuario, unidade=self.unidade).count()
        if registro<=0: # No caso de não haver produto no estoque.     
            raise forms.ValidationError(
            'Comando inválido. Cadastre pelo menos um produto no estoque.'
        )
        elif produto == None:# No caso de não haver uma seleção para o campo.
            raise forms.ValidationError('Campo obrigatório.')             
        return produto    
     

    def clean_aluno(self):
        aluno = self.cleaned_data['aluno']
        registro = AlunoModel.objects.filter(
            usuario=self.usuario, unidade=self.unidade).count()
        if registro<=0: # No caso de não haver alunos registrados  no banco de dados.
            raise forms.ValidationError(
            'Sem registro no cadastro de aluno. Cadastre pelo menos um aluno.'
        )
        elif aluno == None: # No caso de não haver um selação para o campo.
            raise forms.ValidationError('Campo obrigatório.')             
        return aluno


class CadastroVendaFormModel(forms.ModelForm):
   
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
                
         
    # def clean_produto(self):
    #     produto_form = self.cleaned_data['produto']
    #     quant_form = self.cleaned_data['quantidade']
    #     instance = EstoqueModel.objects.get(produto=produto_form)
        
    #     if produto_form == None: #Caso o estoque não tenha produtos cadastrados.
    #          raise forms.ValidationError('Comando inválido. Cadastre pelo menos um produto no estoque.') 
        
    #     elif quant_form > instance.quantidade :# Caso a quantidade de venda supere a quantidade no estoque.        
        
    #         raise forms.ValidationError(f'A quantidade no estoque de {produto_form} é {instance.quantidade}.')
    #     return produto_form


class CategoriaProdutoFormModel(forms.ModelForm):
    class Meta:
        model = CategoriaProdutoModel
        fields = ['categoria']

    # def clean_categoria(self):
    #     campo_categoria = self.cleaned_data['categoria']
    #     if CategoriaProdutoModel.objects.filter(
    #         categoria=campo_categoria,).exists():
    #         raise forms.ValidationError('Categoria existente.')           
      
    #     return campo_categoria   


class FormTesteEstoque(forms.ModelForm):
    class Meta:
        model = TesteEstoqueModel
        fields = ['produto','quantidade','valor']


class UnidModelForm(forms.Form):

    unidade = forms.CharField(label='Unidade',max_length=25)



    def __init__(self, *args, **kwargs):
        # Recupera o usuário da sessão ao inicializar o formulário
        usuario_logado = kwargs.pop('usuario_logado', None)
        super(UnidModelForm, self).__init__(*args, **kwargs)
        
        # # Adiciona o campo ao formulário com base no usuário da sessão
        # if usuario_logado:
        #     self.fields['unidade'] = forms.ModelChoiceField(
        #         queryset=UnidModel.objects.filter(usuario=usuario_logado),
        #         to_field_name='usuario',
        #         empty_label="Selecione uma unidade",
        #     )
    


class CreateUnidModelForm(forms.Form):   
    unidade = forms.CharField(label='Unidade',max_length=25)

    def __init__(self, *args, **kwargs):
        # Recupera o usuário da sessão ao inicializar o formulário
        self.usuario = kwargs.pop('usuario', None)
        super(CreateUnidModelForm, self).__init__(*args, **kwargs)

    def clean_unidade(self):
      # Checa a unidade à ser criada evitando duplicações de unidade para usuário.   
        unidade = self.cleaned_data['unidade']       
        if UnidModel.objects.filter(usuario=self.usuario, unidade=unidade).exists():
            raise forms.ValidationError(f'''Nome inválida,{unidade}, 
            unidade já existente em nossos registros.''')
        return unidade
   

