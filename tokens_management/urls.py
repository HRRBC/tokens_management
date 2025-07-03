from django.contrib import admin
from django.urls import path
from tokens_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('area_administrativa/', views.admin, name='admin'),
    path("", views.home, name="home"),
    path("lista_tokens/", views.lista_tokens, name="lista_tokens"),
    path("lista_tokens/<str:funcao>/", views.lista_tokens_funcao, name="lista_tokens_funcao"),
    path("novos_tokens/", views.atualizar_lista, name="atualizar_lista"),
    path("atualizar_token/<int:token_id>/", views.atualizar_token, name="atualizar_token"),
    path("novo_token/", views.novo_token, name="novo_token"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("exportar_planilha/", views.exportar_planilha, name="exportar_planilha"),
]


