from cadastro.forms import CreateUnidModelForm
from cadastro.models import UnidModel
from django import forms



class Check():   
   
    def __init__(self, usuario_logado):
        self.usuario_logado = usuario_logado
  

    def check_create(self,model,field,user):  
       
        if model.objects.filter(usuario=self.usuario_logado, unidade=field).exists():
            raise forms.ValidationError (f'''Nome inválida, {field}, 
            unidade já existente em nossos registros.''')
        
        return True

