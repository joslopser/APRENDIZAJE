from django.shortcuts import render, render_to_response , get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
import repositorio.lib.Opciones as opc
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

#@login_required(login_url='/ingresar')
def categoria(request, id_categoria):
	"""
	Vista que despliega las sub categorías y objetos pretenecientes a dicha catagoría.
	"""
	padre=None
	abuelo=None
	categoria = RutaCategoria.objects.get(pk=id_categoria)
	catn1 = list(RutaCategoria.objects.filter(cat_padre=categoria))
	padre = categoria.cat_padre
	if padre:
		abuelo = padre.cat_padre
	if request.user.is_authenticated():
		objetos = Objeto.objects.filter(ruta_categoria=categoria).filter(repositorio__grupos=request.user.groups.all()).filter(publicado=True) | Objeto.objects.filter(ruta_categoria=categoria).filter(repositorio__publico=True).filter(publicado=True)
		objetos = list(set(objetos)) #quitar duplicados en la lista
		data={'usuario':request.user, 'categoria':categoria, 'objetos':objetos, 'catn1':catn1, 'padre':padre, 'abuelo':abuelo}
	else:
		objetos = Objeto.objects.filter(ruta_categoria=categoria).filter(publicado=True).filter(repositorio__publico=True)
		data={'usuario':False,'categoria':categoria, 'objetos':objetos, 'catn1':catn1, 'padre':padre, 'abuelo':abuelo}
	return render_to_response('categoria.html',data,context_instance=RequestContext(request))


#@login_required(login_url='/ingresar')
def objeto(request, id_objeto):
	"""
	En esta vista se desplegarán la información del Objeto seleccionado
	"""
	obj=get_object_or_404(Objeto, pk=id_objeto)#anteriormente tenía obj=Objeto.objects.get(pk=id_objeto), lo cual generaba un error 500 al no encontrarlo, por eso la mejor opción es esta
	gruposobj = obj.repositorio.grupos.all()
	gruposu = request.user.groups.all()
	puedever=False
	for go in gruposobj:
		for gu in gruposu:
			if go == gu:
				puedever=True
	if puedever | obj.repositorio.publico:
		idiom={}
		nivel_a={}
		format={}
		tipo_i={}
		nivel_i={}
		contex={}
		[idiom.update({k:v}) for k,v in opc.get_idiomas()]
		[nivel_a.update({k:v}) for k,v in opc.get_nivel_agregacion()]
		[format.update({k:v}) for k,v in opc.get_tipo_recurso()]
		[tipo_i.update({k:v}) for k,v in opc.get_tipo_interactividad()]
		[nivel_i.update({k:v}) for k,v in opc.get_nivel_interactividad()]
		[contex.update({k:v}) for k,v in opc.get_contexto()]
		if request.user.is_authenticated():
			data={'usuario':request.user, 'objeto':obj, 'espec':obj.espec_lom, 'autores':obj.autores.all(), 'keywords':obj.palabras_claves.all(),'idioma':idiom[obj.espec_lom.lc1_idioma],'niv_agr':nivel_a[obj.espec_lom.lc1_nivel_agregacion],'formato':format[obj.espec_lom.lc4_tipo_rec],'tipo_i':tipo_i[obj.espec_lom.lc4_tipo_inter],'nivel_i':nivel_i[obj.espec_lom.lc4_nivel_inter],'context':contex[obj.espec_lom.lc4_contexto]}
		else:
			data={'objeto':obj, 'espec':obj.espec_lom, 'autores':obj.autores.all(), 'keywords':obj.palabras_claves.all(),'idioma':idiom[obj.espec_lom.lc1_idioma],'niv_agr':nivel_a[obj.espec_lom.lc1_nivel_agregacion],'formato':format[obj.espec_lom.lc4_tipo_rec],'tipo_i':tipo_i[obj.espec_lom.lc4_tipo_inter],'nivel_i':nivel_i[obj.espec_lom.lc4_nivel_inter],'context':contex[obj.espec_lom.lc4_contexto]}
		return render_to_response('objeto.html',data,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

@login_required(login_url='/ingresar')
def cerrar(request):
	"""
	Vista que permite cerrar sesión de manera segura en el sistema.
	"""
	logout(request)
	return HttpResponseRedirect('/')
