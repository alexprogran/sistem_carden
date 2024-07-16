import re
import datetime
from typing import Any
from django import forms


from cadastro.models import  CadastrosVendaModel, DebitoModel, EstoqueModel, ModelAluno


class PesquisaDebitoAlunoForm(forms.Form):
    
    
    """
    Formulário para pesquisa de débito do aluno.
    """

    nome = forms.CharField(label='Nome', max_length=25)


    def __init__(self,*args, **kwargs):
        self.usuario = kwargs.pop('usuario')
        self.unidade = kwargs.pop('unidade')
        super().__init__(*args, **kwargs)


    def clean(self):
       
        nome_form = self.cleaned_data['nome']
        cleaned_data = super().clean()
        #Checando o registro do aluno.
        if not  ModelAluno.objects.filter(usuario=self.usuario,
            unidade=self.unidade, nome=nome_form).exists():
            raise forms.ValidationError("""Digite um nome válido. {} não se encontra
            em nossos cadastros.""".format(nome_form))
        
        # Checando se o aluno possui débito.   
        elif not DebitoModel.objects.filter(aluno=nome_form, status='pendente').exists():
                
            raise forms.ValidationError("Não foi encontrado débito para {}".format(nome_form))
      
    
class PesquisaVendaDataForm(forms.Form):

    """
    Fomulário para a pesquisa de venda.

    Raise:
        forms.Validations.Error - Caso a data informada para a pesquisa não
        esteja no formato esperado ou não seja encontrada nos registros.
    
    """

    data = forms.DateField(label='Data')


    def clean(self):
        data_form = self.cleaned_data.get('data')
        clean_data = super().clean()

        if not data_form == None:
           
            if not CadastrosVendaModel.objects.filter(data=data_form).exists():
                raise forms.ValidationError('Não existe registro de venda para esta data.')
        
        else:
            raise forms.ValidationError('''Data inválida.
            Formato esperado, exemplo: "00/00/0000 (mês/dia/ano).            ''')
        
      
class PesquisaAlunoForm(forms.Form):
    """
    Formúlario para pesquisa do aluno.

    """
    nome_aluno = forms.CharField(label='Nome',max_length=25) 
    
    def __init__(self,*args, **kwargs):
        self.usuario = kwargs.pop('usuario',None)
        self.unidade = kwargs.pop('unidade',None)
        super(PesquisaAlunoForm,self).__init__(*args,**kwargs)
        self.fields['nome_aluno'].widget.attrs.update({'placeholder':'*Informe o nome do aluno.'})

    

    # Checagem do registro do aluno
    def clean(self):
        cleaned_data = super().clean()
        nome_form = cleaned_data.get('nome_aluno')
       
        if not ModelAluno.objects.filter(usuario=self.usuario,                                         
            unidade=self.unidade, nome=nome_form).exists():
            raise forms.ValidationError(f'Digite um aluno válido, {nome_form} não foi encontrado nos registros')