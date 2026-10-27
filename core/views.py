from functools import wraps

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AdministradorForm, CadastroForm, FotoFormSet, PublicacaoForm
from .models import Publicacao


def somente_admin(view):
    """Exige login e papel de administrador (is_staff)."""
    @login_required
    @wraps(view)
    def _view(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return _view


def _formulario(request, form, titulo, botao, **extra):
    return render(request, "core/formulario.html", {"form": form, "titulo": titulo, "botao": botao, **extra})


def index(request):
    return render(request, "core/index.html")


def cadastro(request):
    form = CadastroForm(request.POST or None)
    if form.is_valid():
        login(request, form.save())
        messages.success(request, "Cadastro concluído. Bem-vindo(a)!")
        return redirect("core:index")
    return _formulario(request, form, "Criar conta", "Cadastrar")


def novidades(request):
    qs = Publicacao.objects.all()
    total = qs.aggregate(t=Sum("pessoas_atendidas"))["t"] or 0
    return render(request, "core/novidades.html", {"publicacoes": qs, "total_acoes": qs.count(), "total_pessoas": total})


def novidade(request, pk):
    return render(request, "core/novidade.html", {"p": get_object_or_404(Publicacao, pk=pk)})


@somente_admin
def painel(request):
    return render(request, "core/painel.html", {"publicacoes": Publicacao.objects.all()})


@somente_admin
def publicacao_salvar(request, pk=None):
    obj = get_object_or_404(Publicacao, pk=pk) if pk else None
    form = PublicacaoForm(request.POST or None, request.FILES or None, instance=obj)
    fotos = FotoFormSet(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid() and fotos.is_valid():
        p = form.save(commit=False)
        if not p.autor_id:
            p.autor = request.user
        p.save()
        fotos.instance = p
        fotos.save()
        messages.success(request, "Ação salva.")
        return redirect("core:painel")
    return _formulario(request, form, "Editar ação" if obj else "Nova ação", "Salvar", fotos=fotos)


@somente_admin
def publicacao_excluir(request, pk):
    obj = get_object_or_404(Publicacao, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Ação excluída.")
        return redirect("core:painel")
    return _formulario(request, None, f"Excluir “{obj.titulo}”?", "Excluir", aviso="Esta ação não pode ser desfeita.")


@login_required
def administrador_novo(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = AdministradorForm(request.POST or None)
    if form.is_valid():
        u = form.save()
        messages.success(request, f"Administrador “{u.username}” criado.")
        return redirect("core:painel")
    return _formulario(request, form, "Novo administrador", "Criar administrador")
