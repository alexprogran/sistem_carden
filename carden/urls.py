from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView




urlpatterns = [
    path("api-auth/",include('rest_framework.urls')), 
    # path("api/token/",TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path("admin/", admin.site.urls),
    path('carden/', lambda request: redirect('cadastro:login'), name='home'),
    path('carden/', include('cadastro.url', namespace='cadastro')),
    path('api/',include('api.url',namespace='api'))
   ]  
  


