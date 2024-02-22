from typing import Any
from django import forms

from cadastro.models import AlunoModel, CadastrosVendaModel, DebitoModel, EstoqueModel


class PesquisaDebitoAlunoForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=25)

    def clean_nome(self):
        nome_form = self.cleaned_data['nome']
        if not AlunoModel.objects.filter(nome=nome_form).exists():
            raise forms.ValidationError("Digite um nomve válido. {} não se encontra em nossos registros.".format(nome_form))
        else:
            
            if not DebitoModel.objects.filter(aluno=nome_form).exists():
                
                raise forms.ValidationError("Não foi encontrado débito para {}".format(nome_form))
        return nome_form
    
    
class PesquisaVendaDataForm(forms.Form):


    data = forms.DateField(label='Data',required=False)
 

    def clean_data(self):
        data_form = self.cleaned_data['data']
        instance = CadastrosVendaModel.objects.filter(data=data_form).exists()

        if not instance:
            raise forms.ValidationError('Não existe registro de venda para esta data.')
        
        return data_form
    

class EstoqueModelForm(forms.ModelForm):
    
    class Meta:
        model = EstoqueModel
        fields = ['produto','codigo','quantidade','preco_custo','total_custo',
        'preco_varejo','total_varejo','categoria'
        ]    
        

class AlunoFormModl(forms.Form):

    
    def __init__(self,*args, **kwargs):
        self.usuario = kwargs.pop('usuario',None)
        self.unidade = kwargs.pop('unidade',None)
        super(AlunoFormModl,self).__init__(*args,**kwargs)


    nome_aluno = forms.CharField(label='Nome',max_length=25)  

    # def clean(self):
    #     cleaned_data = super().clean()
    #     nome_form = cleaned_data.get('nome_aluno')
    #     user = self.usuario
    #     unid = self.unidade

    #     if not AlunoModel.objects.filter(usuario=user, unidade=unid, nome=nome_form).exists():
    #         raise forms.ValidationError(f'Digite um aluno válido, {nome_form} não foi encontrado nos registros')