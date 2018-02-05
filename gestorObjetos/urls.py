from django.conf.urls import url
from gestorObjetos.views import index, ingresar, redirige, downloadEdit, docObjeto, download, crearAutor, editObjeto, principal, privado, categoria, objeto, cerrar, buscar, busqueda


urlpatterns = [

    #url(r'^$', views.post_list),
    #url(r'^principal/', principal),
    url(r'^ingresar/', ingresar),
    #url(r'^privado/', privado),
    url(r'^$', principal),
    url(r'^privado/', privado),
    url(r'^categoria/(?P<id_categoria>\d+)$', categoria),
    url(r'^objeto/(?P<id_objeto>\d+)$',objeto),
    url(r'^cerrar/$', cerrar),
    url(r'^buscar/$', buscar, name='buscar'),
    url(r'^busqueda/$', busqueda, name='busqueda'),
    url(r'^crearAutor/$', crearAutor, name='crearAutor'),
    url(r'^categoria/(?P<id_categoria>\d+)$', categoria),
    url(r'^docente/$', docObjeto),
    url(r'^descarga/(?P<id>.+)$', download),
    url(r'^editObjeto/objeto/(?P<id_objeto>\d+)$', editObjeto),
    url(r'^admin/gestorObjetos/objeto/(?P<id>.+)/objetos/.+$', download),
    url(r'^admin/logout/$', redirige),
]

