from django.conf.urls import url
from gestorObjetos.views import catalogar, crearUsuario, borrarObjeto, thanks, index, ingresar, redirige, downloadEdit, docObjeto, download, crearAutor, editObjeto, principal, privado, categoria, objeto, cerrar, buscar, busqueda
from gestorProyectos.views import Proyecto, verProyecto, editProyecto, asociarProyecto
from gestorProyectos.views_validar import validar
from gestorProyectos.views_revisor import ver_proyecto, verProyectos
from django.conf import settings
from django.conf.urls.static import static

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
    url(r'^borrarObjeto/objeto/(?P<id_objeto>\d+)$', borrarObjeto),
    url(r'^admin/gestorObjetos/objeto/(?P<id>.+)/objetos/.+$', download),
    url(r'^admin/logout/$', redirige),
    url(r'^email/$', crearUsuario),
    url(r'^thanks/$', thanks),
    url(r'^catalogacion', catalogar),
    #url(r'^registrarUsu', c),

    url(r'^proyecto/$',Proyecto ),
    url(r'^revisor/$', verProyectos),
    url(r'^proyecto/(?P<id_proyecto>\d+)$',verProyecto),
    url(r'^editProyecto/(?P<id_objeto>\d+)$',editProyecto),
    url(r'^asociarProyecto/(?P<id_objeto>\d+)$',asociarProyecto),
    url(r'^validar/(?P<id_proyecto>\d+)$',validar),
    url(r'^ver_proyecto/$',ver_proyecto, name='ver_proyecto'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

