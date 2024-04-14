from django.urls import path
from rest_framework import routers
from .views import (create_unid, view_login, view_cadastro_aluno,
view_cadastro, view_cadastro_aluno, view_cadastro_debito, view_cadastro_funcionario,
view_cadastro_estoque, view_cadastro_usuario, view_cadastro_vendas, view_categoria_produto, view_home_carden, view_unid)
from deleta.views import delete_lista_debito, view_delete_aluno, view_delete_produto
from pesquisa.views import ( view_lista_aluno, result_deb_aluno,
 view_listar_estoque, view_pesquisa, view_pesquisa_aluno,
 view_pesquisa_debito_aluno, view_lista_debito,view_lista_vendas,
   view_pesquisa_venda_data, view_pesquisa_venda_entre_data,result_vendas)

from upadate.views import  (update, 
 view_update_aluno,view_update_estoque, view_update_vendas)

app_name = "cadastro"

urlpatterns = [
    
    path('home-carden/',view_home_carden, name='home-carden'),
    path('login/',view_login, name='login'), 
    path('unidade/',view_unid, name='unidade'),


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
  

    path('lista-aluno/',view_lista_aluno, name='lista-aluno'),
    path('lista-vendas/',view_lista_vendas, name='lista-vendas'),
    path('lista-estoque/',view_listar_estoque, name='lista-estoque'),
    path('lista-debito/',view_lista_debito, name='lista-debito'),
    path('pesquisa-alunos/',view_pesquisa_aluno, name='pesquisa-alunos'),  
    path('pesquisa-venda-data/',view_pesquisa_venda_data, name='pesquisa-venda-data'),
    path('result-venda-data/<str:dat_pesq>/', result_vendas, name='result-venda-data'),
    path('result-deb-aluno/<str:estudante>/', result_deb_aluno, name='result-deb-aluno'),

    path('pesquisa-venda-entre-data/',view_pesquisa_venda_entre_data, name='pesquisa-venda-entre-data'),
    path('pesquisa-debito-aluno/',view_pesquisa_debito_aluno, name='pesquisa-debito-aluno'),
    path('pesquisa/',view_pesquisa, name='pesquisa'),
        
    path('delete-registro-debito/',delete_lista_debito, name='delete-registro-debito'),
    path('delete-produto/',view_delete_produto, name='delete-produto'),
    path('delete-aluno/',view_delete_aluno, name='delete-aluno'),

]


