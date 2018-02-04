from django.conf.urls import url
from gestorProyectos.views import Proyecto, verProyecto, editProyecto, asociarProyecto
from gestorProyectos.views_validar import validar
from gestorProyectos.views_revisor import ver_proyecto

urlpatterns = [

    url(r'^proyecto/$',Proyecto ),
    url(r'^revisor/$', verProyecto),
    url(r'^proyecto/(?P<id_proyecto>\d+)$',verProyecto),
    url(r'^editProyecto/(?P<id_objeto>\d+)$',editProyecto),
    url(r'^asociarProyecto/(?P<id_objeto>\d+)$',asociarProyecto),
    url(r'^validar/(?P<id_proyecto>\d+)$',validar),
    url(r'^ver_proyecto/$',ver_proyecto, name='ver_proyecto'),
]