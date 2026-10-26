from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("entrar/", auth_views.LoginView.as_view(
        template_name="core/formulario.html", redirect_authenticated_user=True,
        extra_context={"titulo": "Entrar", "botao": "Entrar"}), name="entrar"),
    path("sair/", auth_views.LogoutView.as_view(), name="sair"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("novidades/", views.novidades, name="novidades"),
    path("novidades/<int:pk>/", views.novidade, name="novidade"),
    path("painel/", views.painel, name="painel"),
    path("painel/nova/", views.publicacao_salvar, name="publicacao_nova"),
    path("painel/<int:pk>/editar/", views.publicacao_salvar, name="publicacao_editar"),
    path("painel/<int:pk>/excluir/", views.publicacao_excluir, name="publicacao_excluir"),
    path("painel/administrador/", views.administrador_novo, name="administrador_novo"),
]
