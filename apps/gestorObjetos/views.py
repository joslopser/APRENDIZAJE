from django.shortcuts import render, render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import login, authenticate, logout
#from apps.gestorObjetos.forms import EspecificacionForm, cEspecificacionForm, ObjetosForm, cObjetosForm

def index(request):
    return HttpResponse("index")

def ingresar(request):
	"""
		Vista que permite realizar el respectivo inicio de sesión para los Usuarios del sistema
	"""
	#Validación del usuario activo que ingresa a la página
	if not request.user.is_anonymous():
		#si es administrador se redirigirá a la interfaz de administración de lo contrario a la vista privado
		if request.user.profile.rol == "paolita":
			return HttpResponseRedirect('/admin')
		else:
			return HttpResponseRedirect('/privado')
	#Si la petición a la vista ya contiene un objeto formulario diligenciado
	if request.method == 'POST':
		#Se instancia el formulario de autenticación por defecto de Django
		formulario = AuthenticationForm(request.POST)
		#Se valida el formualario en sus campos.
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					if request.user.profile.rol == "paolita":
						return HttpResponseRedirect('/admin')
					else:
						return HttpResponseRedirect('/privado')
				else:
					return render_to_response('noactivo.html', context_instance=RequestContext(request))
			else:
				return render_to_response('nousuario.html', context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('ingresar.html', {'formulario':formulario}, context_instance = RequestContext(request))

