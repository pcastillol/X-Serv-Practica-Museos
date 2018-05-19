from django.shortcuts import render
import urllib.request
from .models import Museo, Comentario, Seleccionado, CSS
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from .xmlParser import myContentHandler
#from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from urllib.request import urlopen
from operator import itemgetter #seleccionar elemento de una N-Tupla
from django.core.exceptions import ObjectDoesNotExist   #coge excepciones de varios modelos
from django.contrib.auth import authenticate, login


# Create your views here.

##########################################
############ PAGINA PRINCIPAL ############
##########################################

def parse():
    # Load parser and driver
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

    # Ready, set, go!
    xmlFile = urlopen('https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full')
    theParser.parse(xmlFile)

    lista = theHandler.getLista()
    return lista #Devuelve lista de diccionarios, uno por cada museo


def dameLista(request):
    lista = parse()
    return HttpResponse(lista)


# XML ---> Database
def loadData(lista):
    for dicMuseo in lista:
        #dict_keys(['NOMBRE', 'CONTENT-URL', 'NOMBRE-VIA', 'NUM', 'CODIGO-POSTAL', 'BARRIO',
#'DISTRITO', 'TELEFONO', 'EMAIL', 'FAX', 'ACCESIBILIDAD', 'DESCRIPCION-ENTIDAD'])
        nombre = dicMuseo['NOMBRE']
        try:
            url = dicMuseo['CONTENT-URL']
        except KeyError:
            url = "-"
        try:
            nombreVia = dicMuseo['NOMBRE-VIA']
        except KeyError:
            nombreVia = "-"
        try:
            num = dicMuseo['NUM']
        except KeyError:
            num = "-"
        try:
            codigo = dicMuseo['CODIGO-POSTAL']
        except KeyError:
            codigo = "-"
        try:
            barrio = dicMuseo['BARRIO']
        except KeyError:
            barrio = "-"
        try:
            distrito = dicMuseo['DISTRITO']
        except KeyError:
            distrito = "-"
        try:
            telefono = dicMuseo['TELEFONO']
        except KeyError:
            telefono = "-"
        try:
            email = dicMuseo['EMAIL']
        except KeyError:
            email = "-"
        try:
            fax = dicMuseo['FAX']
        except KeyError:
            fax = "-"
        try:
            accesibilidad = dicMuseo['ACCESIBILIDAD']
        except KeyError:
            accesibilidad = "-"
        try:
            descripcion = dicMuseo['DESCRIPCION-ENTIDAD']
        except KeyError:
            descripcion = "-"

        direccion = nombreVia + ", " + num + ", " + "CP: " + codigo
        contacto = "tlf: " + telefono + ", " + "email: " + email + ", " + "fax: " + fax

        museo = Museo(nombre = nombre, enlace = url, direccion = direccion,
barrio = barrio, distrito = distrito, contacto = contacto, accesibilidad = accesibilidad, descripcion = descripcion)
        museo.save()

#Ordena la lista de museos por numero de comentarios, de mayor a menor.
def sortByComments(museos):
    dic = {}
    topMuseos = []

    for museo in museos:
        identificador = museo.id
        try:
            comentarios = Comentario.objects.filter(museo_id=identificador) #lista con los comentarios de museo
            dic[identificador] = len(comentarios) #{museo_id : numero de comentarios}
        except Comentario.DoesNotExist:
            print("No hay comentarios")

    topMuseos = sorted(dic.items(), key=itemgetter(1), reverse=True)

    return topMuseos    #devuelve lista de tuplas tipo [(idX, 5), (idY, 2), (idZ, 0)] donde cada tupla es un museo y su
                        #numero de comentarios, ordenada de mayor numero de comentarios a menor


@csrf_exempt
def pag_principal(request):
    topMuseos = []  #[(id_museo, numComentarios)]
    users = []  #[(usuario, titulo_pag)]

    museos = Museo.objects.all()

    #Si no estan los museos cargados en la BD, parseamos y los almacenamos
    if len(museos) < 1:
        lista_museos = parse() #lista de dicc
        loadData(lista_museos)

    topMuseos = sortByComments(museos)
    counter = 5 #Quiero que me muestre 5 museos
    lista_museos_aux = []   #lista de 5 o menos museos que se mostrara

    for tupla in topMuseos:
        if (counter > 0) and (tupla[1] > 0): #si contador mayor que 0 y el museo tiene comentarios
            counter = counter - 1
            try:
                museo = Museo.objects.get(id=tupla[0]) #cogemos el museo con ese id

                usuarios = User.objects.all()
                for usuario in usuarios:
                    try:
                        css = CSS.objects.get(user=usuario.username)
                        if len(users) < len(usuarios):    #si hay menos usuarios en la lista que en la BD
                            users.append((css.user, css.titulo)) #añadimos a la lista la tupla con el nombre y el titulo del usuario
                    except CSS.DoesNotExist:
                        if len(users) < len(usuarios):
                            users.append((usuario.username,('Pagina de ' + usuario.username)))

                lista_museos_aux.append(museo)  #añadimos por el final para que queden ordenados por nComments

            except ObjectDoesNotExist:
                print ("Museo no disponible")

    # respuesta = lista_museos_aux
    # return HttpResponse(respuesta)

    template = get_template('index_extension.html')
    context = {'museos': lista_museos_aux,
    			'usuarios': users}
    respuesta = template.render(context,request)
    return HttpResponse(respuesta)

@csrf_exempt
def loggin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username = username, password = password)
    if user is not None:
        login(request, user)
    else:
        pass

    return HttpResponseRedirect("/")
#https://docs.djangoproject.com/en/2.0/topics/auth/default/ - How to log a user in


############################################
############ PAGINA DEL USUARIO ############
############################################

@csrf_exempt
def pag_usuario(request, user):
    lista_museos = []
    try:
        css = CSS.objects.get(user=user)
        titulo = css.titulo
        us = user
        usuario = User.objects.get(username=user)
    except CSS.DoesNotExist:
        usuario = User.objects.get(username=user)
        us = usuario.username
        titulo = ""
    try:
        museos_seleccionados = Seleccionado.objects.filter(user=usuario)
        for museo in museos_seleccionados:
            lista_museos.append((museo))
    except ObjectDoesNotExist:
        print("No hay museos seleccionados")

    # respuesta = "lista museos: " + str(lista_museos) + "<br>" + "usuario: " + us + "<br>" + "titulo: " + titulo
    # return HttpResponse(respuesta)

    template = get_template('museos/plantilla_usuario.html')
    context = {'museos': lista_museos,
                'usuario': us,
                'titulo': titulo}

    return HttpResponse(template.render(context, request))

@csrf_exempt
def cambiarTitulo(request):
    lista_museos = []

    if request.user.is_authenticated():
        titulo = request.POST.get('titulo')
        username = request.user.username
        try:
            css = CSS.objects.get(user=username)
            css.titulo = titulo
            css.save()
            usuario = User.objects.get(username=username)
        except CSS.DoesNotExist:
            css = CSS(user = username, titulo = titulo, color = "#917b3b", size = 0.0)
            css.save()
            usuario = User.objects.get(username=username)

    else:
        titulo = ""
        usuario = User.objects.get(username=request.user.username)
        username = usuario.username

    try:
        museos_seleccionados = Seleccionado.objects.filter(user=usuario)
        for museo in museos_seleccionados:
            lista_museos.append((museo))
    except ObjectDoesNotExist:
        print("No hay museos seleccionados")

    # respuesta = "lista museos: " + str(lista_museos) + "<br>" + "usuario: " + username + "<br>" + "titulo: " + titulo
    # return HttpResponse()

    template = get_template('museos/plantilla_usuario.html')
    context = {'museos': lista_museos,
                'usuario': username,
                'titulo': titulo}

    return HttpResponse(template.render(context, request))


@csrf_exempt
def miPagina(request):
    if request.user.is_authenticated():
        username = request.user.username
        return HttpResponseRedirect("/" + username)
    else:
        return HttpResponseNotFound("No se cual es tu pagina. Aun no te conozco")


############################################
############ PAGINA UN MUSEO ###############
############################################

@csrf_exempt
def showMuseoId(request, id):
    try:
        museo = Museo.objects.get(id=id)
        comentarios = Comentario.objects.filter(museo_id=museo)
        if len(comentarios) == 0:
            comentarios = []
    except ObjectDoesNotExist:
        pass

    template = get_template('museos/plantilla_museoid.html')
    context = {'museo': museo,
                'comentarios': comentarios}

    return HttpResponse(template.render(context,request))

@csrf_exempt
def addSeleccionado(request, id):
    if request.user.is_authenticated():
        username = request.user.username
        try:
            user = User.objects.get(username=username)
            museo = Museo.objects.get(id=id)
            comentarios = Comentario.objects.filter(museo_id=museo)

            if len(comentarios) == 0:
                comentarios = []

            try:    #Vemos si el museo ya esta seleccionado por ese usuario
                Seleccionado.objects.get(user=user, museo_id=museo)

                template = get_template('museos/plantilla_museo_solicitado.html')
                context = {'museo': museo,
                            'comentarios': comentarios}

                return HttpResponse(template.render(context,request))

            except Seleccionado.DoesNotExist:   #Si no esta seleccionado, lo guardamos
                seleccionado = Seleccionado(museo_id = museo, user = user)
                seleccionado.save()

                template = get_template('museos/plantilla_museoid.html')
                context = {'museo': museo,
                            'comentarios': comentarios}

                return HttpResponse(template.render(context,request))

        except ObjectDoesNotExist:
            pass

@csrf_exempt
def addComentario(request, id):
    if request.user.is_authenticated():
        museo = Museo.objects.get(id=id)
        texto = request.POST.get("comentario")
        newComentario = Comentario(texto = texto, museo_id = museo)
        newComentario.save()

        return HttpResponseRedirect('/museos/' + str(id))

    else:
        return HttpResponseRedirect('/museos/' + str(id))


################################################
############ PAGINA TODOS MUSEOS ###############
################################################

@csrf_exempt
def showMuseos(request):
    museos = Museo.objects.all()
    template = get_template('museos/plantilla_museos.html')
    context = {'museos': museos}

    return HttpResponse(template.render(context,request))

@csrf_exempt
def filterMuseos(request):  #Filtro ACCESIBILIDAD y DISTRITO
    lista_museos = []
    distrito = request.POST.get('distrito')
    accesible = request.POST.get('accesible')
    todos = Museo.objects.all()

    if distrito in ['CENTRO', 'BARAJAS', 'RETIRO', 'MONCLOA-ARAVACA', 'CIUDAD LINEAL',
'SALAMANCA', 'CHAMARTIN', 'CHAMBERI', 'TETUAN', 'LATINA', 'PUENTE DE VALLECAS', 'FUENCARRAL-EL PARDO', 'ARGANZUELA']:
        lista_museos = Museo.objects.filter(distrito=distrito)
    elif distrito == "todos":
        lista_museos = Museo.objects.all()
    elif accesible in ['SI', 'NO']:
        lista_museos = Museo.objects.filter(accesibilidad=accesible)
    elif accesible == "todos":
        lista_museos == Museo.objects.all()

    template = get_template('museos/plantilla_museos.html')
    context = {'museos': lista_museos,
                'todos': todos}

    return HttpResponse(template.render(context,request))


#########################################
############ USUARIO XML ################
#########################################

@csrf_exempt
def showUsuarioXML(request, user):
    museos_seleccionados = []

    try:
        user = User.objects.get(username=user)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Lo sentimos. Necesitas registrarte.")

    seleccionados = Seleccionado.objects.filter(user=user)
    for seleccionado in seleccionados:
        museos_seleccionados.append(seleccionado)

    template = get_template('museos/plantilla_xml.xml')
    context = {'seleccionados': museos_seleccionados}

    return HttpResponse(template.render(context,request), content_type = 'text/xml')
    #https://djangobook.com/generating-non-html-content/


###################################
############ ABOUT ################
###################################

@csrf_exempt
def showAbout(request):
    template = get_template('museos/about.html')
    context = {}

    return HttpResponse(template.render(context,request))


######################################
############ OPTATIVAS ###############
######################################

###Canal RSS con los comentarios###
@csrf_exempt
def rssChannel(request):
    comentarios = Comentario.objects.all()

    template = get_template('museos/plantilla_rss.html')
    context = {'comentarios': comentarios}

    return HttpResponse(template.render(context,request))

###Registro de usuarios###
@csrf_exempt
def register(request):
    if request.method == "GET":
        template = get_template('museos/plantilla_registro.html')
        context = {}
        return HttpResponse(template.render(context,request))
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password'] #contraseña en crudo
        titulo = "Pagina de " + username

        user = User(username = username, password = password)   #creamos objeto con contraseña en crudo
        user.set_password(user.password)    #cifrado de la contraseña
        user.is_staff = True
        user.save()

        user = User.objects.get(username=username)  #User object que acabo de instancair
        css = CSS(user = user, titulo = titulo)
        css.save()

        return HttpResponseRedirect("/")
    else:
        return HttpResponseNotFound("Not Found")


###Canal XML Pagina Principal###
@csrf_exempt
def mainXml(request):
    if request.method == "GET":
        topMuseos = []  #[(id_museo, numComentarios)]
        users = []  #[(usuario, titulo_pag)]

        museos = Museo.objects.all()
        topMuseos = sortByComments(museos)  #lista ordenada
        counter = 5 #Quiero que me muestre 5 museos
        lista_museos_aux = []   #lista de 5 o menos museos que se mostrara

        for tupla in topMuseos:
            if (counter > 0) and (tupla[1] > 0): #si contador mayor que 0 y el museo tiene comentarios
                counter = counter - 1
                try:
                    museo = Museo.objects.get(id=tupla[0]) #cogemos el museo con ese id

                    usuarios = User.objects.all()
                    for usuario in usuarios:
                        try:
                            css = CSS.objects.get(user=usuario.username)
                            if len(users) < len(usuarios):    #si hay menos usuarios en la lista que en la BD
                                users.append((css.user, css.titulo)) #añadimos a la lista la tupla con el nombre y el titulo del usuario
                        except CSS.DoesNotExist:
                            if len(users) < len(usuarios):
                                users.append((usuario.username,('Pagina de ' + usuario.username)))

                    lista_museos_aux.append(museo)  #añadimos por el final para que queden ordenados por nComments

                except ObjectDoesNotExist:
                    print ("Museo no disponible")

        template = get_template('museos/plantilla_mainxml.xml')
        context = {'museos': lista_museos_aux,
                    'usuarios': users}
        return HttpResponse(template.render(context,request), content_type = 'text/xml')

    else:
        return HttpResponseNotFound("Not Found")
