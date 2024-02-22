from django.urls import path
from rest_framework import routers
from cadastro.views import (create_unid, lista_teste_produto, view_login, view_cadastro_aluno,
view_cadastro, view_cadastro_aluno, view_cadastro_debito, view_cadastro_funcionario,
view_cadastro_estoque, view_cadastro_teste_produto, view_cadastro_usuario, view_cadastro_vendas, view_categoria_produto, view_home_carden, view_unid)
from deleta.views import view_delete_produto
from pesquisa.views import (delete_lista_debito, view_listar_estoque, view_pesquisa, view_pesquisa_aluno,
 view_pesquisa_debito_aluno, view_lista_debito,view_lista_vendas, view_pesquisa_venda_data, view_pesquisa_venda_entre_data)

from upadate.views import  (update_debito_model_aluno,update, update_debito_model_produto,
 view_update_aluno, view_update_estoque, view_update_vendas)
app_name = "cadastro"

urlpatterns = [
    
    path('home-carden/',view_home_carden, name='home-carden'),
    path('login/',view_login, name='login'), 
    path('unidade/',view_unid, name='unidade'),

    path('cadastro-teste-produto/', view_cadastro_teste_produto, name='cadastro-teste-produto'),
    path('lista-teste-produto/', lista_teste_produto, name='lista-teste-produto'),

    path('cadast-user/',view_cadastro_usuario, name='cadast-user'),
    path('aluno/',view_cadastro_aluno, name='aluno'),     
    path('cadast-unid/',create_unid, name='cadast-unid'),   
    path('cadast-vendas/',view_cadastro_vendas, name='cadast-vendas'),
    path('cadast-aluno/',view_cadastro_aluno, name='cadast-aluno'),
    path('cadast-estoque-produto/',view_cadastro_estoque, name='cadast-estoque-produto'),
    path('cadast-categoria-produto/',view_categoria_produto, name='cadast-categoria-produto'),
    path('cadast-funcionario/',view_cadastro_funcionario, name='cadast-funcionario'),
    path('cadast-debito/',view_cadastro_debito, name='cadast-debito'),
    path('cadastro/',view_cadastro, name='cadastro'),
    
    path('update/',update, name='update'),
    path('update-aluno/', view_update_aluno, name='update-aluno'),
    path('update-estoque/',view_update_estoque, name='update-estoque'),
    path('update-vendas/', view_update_vendas, name='update-vendas'),
    path('update-aluno/', update_debito_model_aluno, name='update-aluno'), #renomear este caminho.
    path('update-produto/', update_debito_model_produto, name='update-produto'),
    
    path('lista-vendas/',view_lista_vendas, name='lista-vendas'),
    path('lista-estoque/',view_listar_estoque, name='lista-estoque'),
    path('lista-debito/',view_lista_debito, name='lista-debito'),
    path('pesquisa-alunos/',view_pesquisa_aluno, name='pesquisa-aluno'),
    path('pesquisa-venda-data/',view_pesquisa_venda_data, name='pesquisa-venda-data'),
    path('pesquisa-venda-entre-data/',view_pesquisa_venda_entre_data, name='pesquisa-venda-entre-data'),
    path('pesquisa-debito-aluno/',view_pesquisa_debito_aluno, name='pesquisa-debito-aluno'),
    path('pesquisa/',view_pesquisa, name='pesquisa'),
        
    path('delete-registro-debito/',delete_lista_debito, name='delete-registro-debito'),
     path('delete-produto/',view_delete_produto, name='delete-produto'),

]


