from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Coleta, FotoPublicacao, Publicacao, TipoMaterial


class CadastroForm(UserCreationForm):
    first_name = forms.CharField(label="Nome", max_length=150)
    email = forms.EmailField(label="E-mail")

    class Meta:
        model = User
        fields = ("username", "first_name", "email")


class AdministradorForm(CadastroForm):
    """Cria um usuário com papel de administrador (is_staff)."""

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user


class PublicacaoForm(forms.ModelForm):
    class Meta:
        model = Publicacao
        fields = ("titulo", "data_acao", "local", "pessoas_atendidas", "texto", "imagem", "video_arquivo", "video_url")
        widgets = {"data_acao": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}

    def clean_video_arquivo(self):
        v = self.cleaned_data.get("video_arquivo")
        if v and v.size > 100 * 1024 * 1024:
            raise forms.ValidationError("O vídeo deve ter no máximo 100 MB.")
        return v


class FotoForm(forms.ModelForm):
    class Meta:
        model = FotoPublicacao
        fields = ("imagem", "legenda")

    def clean_imagem(self):
        img = self.cleaned_data.get("imagem")
        if img and getattr(img, "size", 0) > 10 * 1024 * 1024:
            raise forms.ValidationError("Cada foto deve ter no máximo 10 MB.")
        return img


FotoFormSet = forms.inlineformset_factory(Publicacao, FotoPublicacao, form=FotoForm, extra=3, can_delete=True)


class TipoMaterialForm(forms.ModelForm):
    class Meta:
        model = TipoMaterial
        fields = ("nome", "unidade")


class ColetaForm(forms.ModelForm):
    class Meta:
        model = Coleta
        fields = ("tipo", "data_coleta", "quantidade", "destinacao", "certificado", "observacoes")
        widgets = {"data_coleta": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
                   "observacoes": forms.Textarea(attrs={"rows": 3})}

    def clean_certificado(self):
        c = self.cleaned_data.get("certificado")
        if c and getattr(c, "size", 0) > 10 * 1024 * 1024:
            raise forms.ValidationError("O certificado deve ter no máximo 10 MB.")
        return c
