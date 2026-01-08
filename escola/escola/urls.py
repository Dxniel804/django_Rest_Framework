from django.contrib import admin
from django.urls import path, include # include → importa rotas de outro app

urlpatterns = [
    path('api/v1/', include('cursos.urls')),
    path('admin/', admin.site.urls),
    # Isso adiciona rotas de login/logout do Django REST Framework.
    path('auth/', include('rest_framework.urls'))
]
