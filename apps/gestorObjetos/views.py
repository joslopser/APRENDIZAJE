from django.shortcuts import render, render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import login, authenticate, logout
from apps.gestorObjetos.forms import EspecificacionForm, cEspecificacionForm, ObjetosForm, cObjetosForm
from apps.gestorObjetos.models import Repositorio, Objeto, Autor, RutaCategoria, EspecificacionLOM, PalabraClave

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

def principal(request):
	"""
		Vista que muestra al usuario visitante la página inicial del sistema
	"""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/privado')
	else:
		repositorios = []
		if len(repositorios) == 0:
			repositorios = list(Repositorio.objects.filter(publico=True))
		else:
			repositorios.extend(list(Repositorio.objects.filter(publico=True)))
		repositorios = list(set(repositorios)) #quitar duplicados en la lista
		objetos = []
		for r in repositorios:
			if len(objetos) == 0:
				objetos = list(Objeto.objects.filter(repositorio=r).filter(publicado=True))
			else:
				objetos.extend(list(Objeto.objects.filter(repositorio=r).filter(publicado=True)))

		catn1 = RutaCategoria.objects.filter(cat_padre=None)
		catnTemp = list(RutaCategoria.objects.all().exclude(cat_padre=None))
		catn2=[]
		catn3=[]
		temp=0
		for c in catn1:
			for c1 in catnTemp:
				if c1.cat_padre == c:
					if c1 in catn2:
						temp=1 #variable temporal sin relevancia en la lógica
					else:
						catn2.append(c1)
		for d in catn2:
			for d1 in catnTemp:
				if d1.cat_padre == d:
					if d1 in catn3:
						temp=2 #variable temporal sin relevancia en la lógica
					else:
						catn3.append(d1)
		formulario=cEspecificacionForm
		return render_to_response('index.html',{'form':formulario, 'repos':repositorios, 'objetos':objetos, 'catn1':catn1, 'catn2':catn2, 'catn3':catn3},context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def privado(request):
	"""
	Vista que despliega la información dependiendo del usuario logueado en el sistema.
	"""
	repositorios = []
	for g in request.user.groups.all():
		repositorios.extend(list(Repositorio.objects.filter(grupos=g) | Repositorio.objects.filter(publico=True)))
	repositorios = list(set(repositorios)) #quitar duplicados en la lista
	objetos = []
	for r in repositorios:
		if len(objetos) == 0:
			objetos = list(Objeto.objects.filter(repositorio=r).filter(publicado=True))
		else:
			objetos.extend(list(Objeto.objects.filter(repositorio=r).filter(publicado=True)))

	catn1 = RutaCategoria.objects.filter(cat_padre=None)
	catnTemp = list(RutaCategoria.objects.all().exclude(cat_padre=None))
	catn2=[]
	catn3=[]
	temp=0
	for c in catn1:
		for c1 in catnTemp:
			if c1.cat_padre == c:
				if c1 in catn2:
					temp=1 #variable temporal sin relevancia en la lógica
				else:
					catn2.append(c1)
	for d in catn2:
		for d1 in catnTemp:
			if d1.cat_padre == d:
				if d1 in catn3:
					temp=2 #variable temporal sin relevancia en la lógica
				else:
					catn3.append(d1)
	formulario=cEspecificacionForm
	return render_to_response('privado.html',{'usuario':request.user, 'form':formulario, 'repos':repositorios, 'objetos':objetos, 'catn1':catn1, 'catn2':catn2, 'catn3':catn3},context_instance=RequestContext(request))