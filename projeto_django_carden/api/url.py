from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AlunoModelViewSet, AlunoViewSet, criar_categoria, lita_categoria, CategoriaProdutoViewSet
app_name = 'api'

router = DefaultRouter()
router.register('alunos',AlunoModelViewSet,basename='alunos')
# router.register('aluno', AlunoViewSet,basename='aluno')
urlpatterns =[
    path('lista-categoria',lita_categoria,name='lista-categoria'),
    path('criar-categoria',criar_categoria,name='criar-categoria'),
    path('aluno', AlunoViewSet.as_view({'get': 'list', 'post': 'create'}), name='aluno'),
    path('aluno/<int:pk>/', AlunoViewSet.as_view({
    'get':'retrieve', 'patch': 'partial_update','put': 'update','delete':'delete' }), name='patch-update-delete'),
    # path('aluno/<int:pk>/', AlunoViewSet.as_view({'delete':'delete' }), name='aluno-delete'),
        

]

urlpatterns = urlpatterns + router.urls