from django import forms

from cadastro.models import EstoqueModel


class PesquisaEstoqueFormDelete(forms.ModelForm):
    class Meta:
        model = EstoqueModel
        fields = ['produto']


class DeleteProdutoEstoque(forms.ModelForm):
    class Meta:
        model = EstoqueModel
        fields = ields = ['produto','quantidade','preco_varejo','preco_custo'] 
