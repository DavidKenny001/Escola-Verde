from django.contrib import admin

from .models import Coleta, Publicacao, TipoMaterial

admin.site.register([Publicacao, TipoMaterial, Coleta])
