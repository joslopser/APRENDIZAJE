# encoding:utf-8
from apps.gestorObjetos.models import Objeto, EspecificacionLOM, Repositorio, PalabraClave, Autor, RutaCategoria, UserProfile
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.sites.models import Site

admin.site.unregister(User)


"""
Registro de los modelos en la interfaz de administración para ser editados por los administradores
"""
admin.site.register(User)

admin.site.register(Objeto)
admin.site.register(EspecificacionLOM)
admin.site.register(Repositorio)
admin.site.register(PalabraClave)
admin.site.register(Autor)
admin.site.register(RutaCategoria)
admin.site.unregister(Site)