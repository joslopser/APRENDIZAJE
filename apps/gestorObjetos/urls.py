from django.conf.urls import url, include, patterns
from apps.gestorObjetos.views import index, ingresar


urlpatterns = [

    #url(r'^$', views.post_list),
    url(r'^ingresar/', ingresar),
    #url(r'^privado/', privado),
    url(r'^$', index, name='Primera view :3'),

]

