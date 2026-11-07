from django.apps import AppConfig
from django.db.models.signals import post_migrate

TIPOS_PADRAO = [
    ("Pilhas", "kg"),
    ("Vidro", "kg"),
    ("Luvas", "un"),
    ("Resíduos de laboratório", "kg"),
    ("Material seco reciclável", "kg"),
]


def criar_tipos_padrao(sender, **kwargs):
    from .models import TipoMaterial
    if not TipoMaterial.objects.exists():
        for nome, unidade in TIPOS_PADRAO:
            TipoMaterial.objects.create(nome=nome, unidade=unidade)


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        post_migrate.connect(criar_tipos_padrao, sender=self)
