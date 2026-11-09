from urllib.parse import parse_qs, urlparse

from django.conf import settings
from django.core.validators import FileExtensionValidator, MinValueValidator
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


class TipoMaterial(models.Model):
    UNIDADES = [("kg", "kg"), ("un", "unidades"), ("l", "litros")]
    nome = models.CharField("nome do material", max_length=80, unique=True)
    unidade = models.CharField("unidade de medida", max_length=2, choices=UNIDADES, default="kg")

    class Meta:
        ordering = ["nome"]
        verbose_name = "tipo de material"
        verbose_name_plural = "tipos de material"

    def __str__(self):
        return self.nome


class Coleta(models.Model):
    tipo = models.ForeignKey(TipoMaterial, on_delete=models.PROTECT, related_name="coletas", verbose_name="material")
    data_coleta = models.DateField("data da coleta/retirada", default=timezone.localdate)
    quantidade = models.DecimalField(
    "quantidade (na unidade do material)",
    max_digits=10,
    decimal_places=3,
    validators=[MinValueValidator(0)]
)
    destinacao = models.CharField("destinação (local ou empresa)", max_length=200, blank=True)
    certificado = models.FileField("certificado de descarte (PDF ou imagem)", upload_to="certificados/", blank=True,
                                   validators=[FileExtensionValidator(["pdf", "jpg", "jpeg", "png"])])
    observacoes = models.TextField("observações", blank=True)
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_coleta", "-criado_em"]
        verbose_name = "coleta"
        verbose_name_plural = "coletas"

    def __str__(self):
        return f"{self.tipo} em {self.data_coleta:%d/%m/%Y}"
