from urllib.parse import parse_qs, urlparse

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models


class Publicacao(models.Model):
    titulo = models.CharField("título", max_length=150)
    texto = models.TextField("texto")
    imagem = models.ImageField("foto", upload_to="fotos/", blank=True)
    video_arquivo = models.FileField(
        "vídeo (mp4 ou webm, até 100 MB)", upload_to="videos/", blank=True,
        validators=[FileExtensionValidator(["mp4", "webm"])],
    )
    video_url = models.URLField("link de vídeo (YouTube)", blank=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "publicação"
        verbose_name_plural = "publicações"

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
