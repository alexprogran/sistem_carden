from django import forms

from cadastro.models import  EstoqueModel, ModelAluno


class PesquisaEstoqueFormDelete(forms.ModelForm):

    # Fomulário de pesquisa do produto a ser deletado.    
   
    class Meta:
        model = EstoqueModel
        fields = ['produto']

    #  # Resgatando o usuário e a unidade da view
    def __init__(self,*args, **kwargs):
        self.usuario = kwargs.pop('usuario')
        self.unidade = kwargs.pop('unidade')
        super(PesquisaEstoqueFormDelete,self).__init__(*args, **kwargs)


    def clean(self):
       
        produt = self.cleaned_data['produto']
        cleaned_data = super().clean()

        print(produt)
        if not EstoqueModel.objects.filter(usuario=self.usuario,
        unidade=self.unidade,produto=produt).exists(): 

            raise forms.ValidationError(
            "*Produto inválido, não encontrado nos registros."
            )
    # Formulári com os dados da intância à ser deletada.

class DeleteProdutoEstoque(forms.ModelForm):
    class Meta:
        model = EstoqueModel
        fields = ields = ['produto','quantidade','preco_varejo','preco_custo'] 



class PesquisaAlunoFormDelete(forms.ModelForm):

    # Fomulário de pequisa do aluno à ser excluido no banco de dados.

    class Meta:
        model = ModelAluno
        fields = ['nome']
        labels = {'nome': 'Aluno',}

    # Resgatando o usuário e a unidade da view.
    def __init__(self,*args, **kwargs):
        self.usuario = kwargs.pop('usuario')
        self.unidade = kwargs.pop('unidade')
        super().__init__(*args, **kwargs)


    #Checando a existência do aluno no cadastro de alunos.
    def clean(self):
        
        aluno = self.cleaned_data['nome']
        cleaned_data = super().clean()

       
        if not ModelAluno.objects.filter(usuario=self.usuario,
        unidade=self.unidade,nome=aluno).exists(): 

            raise forms.ValidationError(
            f'Nome inválido, não encontrado {aluno} nos registros.'
            )


class DeleteAlunoModelForm(forms.ModelForm):


    # Fomulário com os dados da instância a ser deletada. 
    
    class Meta:
        model = ModelAluno
        fields = ['nome','turma','responsavel','tel_responsavel'] 


