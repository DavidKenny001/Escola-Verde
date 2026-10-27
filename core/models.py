from urllib.parse import parse_qs, urlparse

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone


class Publicacao(models.Model):
    titulo = models.CharField("título da ação", max_length=150)
    data_acao = models.DateField("data da ação", default=timezone.localdate)
    local = models.CharField("local", max_length=150, blank=True)
    pessoas_atendidas = models.PositiveIntegerField("número de pessoas atendidas", null=True, blank=True)
    texto = models.TextField("descrição")
    imagem = models.ImageField("foto de capa", upload_to="fotos/", blank=True)
    video_arquivo = models.FileField(
        "vídeo (mp4 ou webm, até 100 MB)", upload_to="videos/", blank=True,
        validators=[FileExtensionValidator(["mp4", "webm"])],
    )
    video_url = models.URLField("link de vídeo (YouTube)", blank=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_acao", "-criado_em"]
        verbose_name = "ação"
        verbose_name_plural = "ações"

    def __str__(self):
        return self.titulo

    @property
    def video_embed(self):
        u = urlparse(self.video_url)
        if "youtu.be" in u.netloc:
            vid = u.path.strip("/")
        elif "youtube.com" in u.netloc:
            vid = parse_qs(u.query).get("v", [""])[0]
        else:
            return ""
        return f"https://www.youtube.com/embed/{vid}" if vid else ""


class FotoPublicacao(models.Model):
    publicacao = models.ForeignKey(Publicacao, on_delete=models.CASCADE, related_name="fotos")
    imagem = models.ImageField("foto", upload_to="fotos/")
    legenda = models.CharField("legenda", max_length=150, blank=True)

    class Meta:
        verbose_name = "foto"
        verbose_name_plural = "fotos"

    def __str__(self):
        return self.legenda or f"Foto {self.pk}"
