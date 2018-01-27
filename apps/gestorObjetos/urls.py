from django.conf.urls import url, include, patterns
from apps.gestorObjetos.views import index, ingresar, principal, privado


urlpatterns = [

    #url(r'^$', views.post_list),
    url(r'^principal/', principal),
    url(r'^ingresar/', ingresar),
    #url(r'^privado/', privado),
    url(r'^$', index, name='Primera view 3'),
    url(r'^privado/', privado)

]

