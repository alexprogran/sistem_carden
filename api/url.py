from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import (AlunoModelViewSet,
 AlunoViewSet, DebAlunoModoViewSet, DebitoVeiwSet, DebitoVeiwSet, FuncionarioModelVeiwSet, criar_categoria, lista_categoria, CategoriaProdutoModelViewSet, sum_deb)
app_name = 'api'

router = DefaultRouter()
router.register('alunos',AlunoModelViewSet,basename='alunos')
router.register('categoria',CategoriaProdutoModelViewSet, basename='categoria')
router.register('agrup-debto',DebitoVeiwSet, 'agrup-debto')
router.register('debito', DebitoVeiwSet, 'debito')
router.register('deb-aluno', DebAlunoModoViewSet,'deb-aluno')
router.register('funcionario',FuncionarioModelVeiwSet, basename='funcionario')
urlpatterns =[
    path('sum-deb/',sum_deb, name='sum-deb'),
    path('lista-categoria/',lista_categoria,name='lista-categoria'),
    path('criar-categoria',criar_categoria,name='criar-categoria'),
    # path('aluno', AlunoViewSet.as_view({'get': 'list', 'post': 'create'}), name='aluno'),
    # path('aluno/<int:pk>/', AlunoViewSet.as_view({
    # 'get':'retrieve', 'patch': 'partial_update','put': 'update','delete':'delete' }), name='patch-update-delete'),
    # path('aluno/<int:pk>/', AlunoViewSet.as_view({'delete':'delete' }), name='aluno-delete'),
    ]

urlpatterns = urlpatterns + router.urls