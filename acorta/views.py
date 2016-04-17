# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from models import Pages
from django.views.decorators.csrf import csrf_exempt
import pickle

# ================= Funciones =================
# ----------------- initFile -----------------
def initFile(name):
    try:
        File = open(name, 'r')
        File.close
    except:
        File = open(name, 'wb')
        File.close
        
# ----------------- LoadURLs and SaveURLs -----------------
def LoadURLs(name ):
    try:
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return {}
def SaveURLs(Dic, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(Dic, f, pickle.HIGHEST_PROTOCOL)
        
# ----------------- decorateHTML -----------------
def decorateHTML (text):
    return ("<html><body>" + text + "</body></html>")
    
# ----------------- myURL -----------------
def myURL ():
    return 'http://127.0.0.1:8000'


# ================= Vistas =================
# ----------------- homePage -----------------
@csrf_exempt
def homePage(request):
    # Creates file "URLs.pkl" for further use, if doesn't exists 
    urlsLargas = 'URLsLong'
    urlsCortas = 'URLsShort'
    initFile((urlsLargas+'.pkl'))
    initFile((urlsCortas+'.pkl'))
    # Loads data of files
    urlLargas = {} # URL   SeqN
    urlLargas = LoadURLs(urlsLargas)
    urlCortas = {} # SeqN  URL
    urlCortas = LoadURLs(urlsCortas)
    seqNumb = len(urlLargas)
    
    if request.method == 'GET':
        # _________________ GET _________________
        respuesta = '<html><body>'\
                    +'<form method="POST" action="">'\
                    +'URL: <input type="text" name="url"><br>'\
                    +'<input type="submit" value="Enviar">'\
                    +'</form>'\
                    +'<p1>En Cache: '+str(urlLargas)+'</p1>'\
                    +'</body><title>Acortador</title>'\
                    +'</html>'
    elif request.method == 'POST' or request.method == 'PUT':
        # _________________ POST or PUT _________________
        print 'Almacenando...'
        cuerpo=request.body.replace('%3A',':') # Recibo estos strings...
        cuerpo=request.body.replace('%2F','/')
        print cuerpo
        if cuerpo[0:4] == 'url=': # POST de formulario o poster con "url..."
            cuerpo = cuerpo[4:] # Quito el url=
        if cuerpo[0:7] != 'http://': # http:// en caso de no haberlo
            cuerpo = 'http://' + cuerpo
        print cuerpo
            
        if cuerpo in urlCortas:
            urllarga = urlCortas[cuerpo]
            urlCorta = cuerpo
            cuerpo = urllarga
            respuesta = decorateHTML('<title>URL Acortada</title>'\
                                    +'<h3>URL corta ya incluida:</h3>'\
                                    +'<p1>URL Larga: <a href= '\
                                    +cuerpo + '>' + cuerpo + '</a></p>'\
                                    +'<p>URL Corta: <a href= '\
                                    +urlCorta + '>'\
                                    +urlCorta + '</a></p>')
        else:
            try: # Entrego la url corta al navegador
                urlCorta = urlLargas[cuerpo]
                print 'URL encontrada, devolviendo almacenada'
            except KeyError:
                print 'URL no encontrada, creando...'
                urlCorta = myURL()+'/'+str(seqNumb)
                urlLargas[cuerpo] = urlCorta # Larga, Corta
                urlCortas[urlCorta] = cuerpo
                # Almacenamiento en ficheros:
                SaveURLs(urlLargas, urlsLargas)
                SaveURLs(urlCortas, urlsCortas)
            respuesta = decorateHTML('<title>URL Acortada</title>'\
                                    +'<p1>URL Larga: <a href= '\
                                    +cuerpo + '>' + cuerpo + '</a></p>'\
                                    +'<p>URL Corta: <a href= '\
                                    +urlCorta + '>'\
                                    +urlCorta + '</a></p>')
    else:
        # _________________ FAIL METHOD _________________
        print 'Error: Recibido metodo desconocido'
        respuesta = ''
    
    return HttpResponse(respuesta)
    
# ----------------- favicon -----------------
def favicon(request):
    respuesta=''
    return HttpResponse(respuesta)

# ----------------- GetShort ----------------- FALTA PROBARLA TRAS POST !!!!!!!
def GetShort(request, recurso):
    # Creates file "URLs.pkl" for further use, if doesn't exists 
    urlsCortas = 'URLsShort'
    initFile((urlsCortas+'.pkl'))
    urlCortas = {} # SeqN  URL
    urlCortas = LoadURLs(urlsCortas)
    urlCorta = myURL()+'/'+str(int(recurso))
    try:
        print('Iniciando Busqueda...')
        urlDestino = urlCortas[urlCorta]
        #httpCode = '303 See Other\r\nLocation: ' + urlDestino
        # Ya no se puede??
        print('URL destino: ' + urlDestino)
        respuesta = decorateHTML('<meta http-equiv="Refresh" content="0;'\
                                +'url='+urlDestino+'">')
    except KeyError:
        print 'Detectada peticion inconsistente'
        #httpCode = '404 Not Found' # Ya no se puede??
        respuesta = decorateHTML('<h3>Recurso no disponible</h3>'\
                                +'<p>Codigo de error: 404</p>')    
    return HttpResponse(respuesta)





# ================= Vistas OLD, SOBRA... ================= 
def pickPage(request, pageID):
    if request.user.is_authenticated():
        respuesta = 'Hola! ' + request.user.username\
                    + ' <a href="/logout">Logout</a> '
    else:
        respuesta = 'Hola desconocido, desea hacer \
                     <a href="/login">Login</a> ?'
    try:
        print(pageID)
        pagina = Pages.objects.get(name=pageID)
        respuesta += '<br><br>La pagina "' + pagina.name\
                    + '" dice: ' + pagina.page + '<br><br>'\
                    +'<form method="GET" action="/home/">'\
                    +'<br><input type="submit" value="Home">'\
                    +'</form>'
    except:
        respuesta += '<br><br><p1> No se encontro esa pagina </p1>'\
                    +'<form method="GET" action="/home/">'\
                    +'<br><br><input type="submit" value="Home">'\
                    +'</form>'
    return HttpResponse(respuesta)

    
@csrf_exempt    
def createPage(request):
    print(request.method)
    if request.method == 'POST':
        print (request.body)
        body = request.body
        info=body.split('&')
        pagina = info[0].split('=')[1]
        texto = info[1].split('=')[1]
        pagina=pagina.replace('+',' ')
        texto=texto.replace('+',' ')
        pageAux = Pages(name=pagina, page=texto)
        pageAux.save()
        respuesta = 'Pagina Almecenada adecuadamente, continuemos!'\
                    + '<meta http-equiv="Refresh" content="2;\
                    url=http://127.0.0.1:8000/mod/">'
    else:
        respuesta = 'Página no permitida, redirigiendo...'\
                    + '<meta http-equiv="Refresh" content="3;\
                    url=http://127.0.0.1:8000/">'

    return HttpResponse(respuesta)
    

def managePages(request):
    respuesta = '<h3>Edición de Páginas</h3>'\
                +'<form method="POST" action="/createPage/">'\
                +'Título Página: <input type="text" name="pagina"><br>'\
                +'Texto: <input type="text"name="texto"><br>'\
                +'<input type="submit" value="Subir">'\
                +'</form>'\
                +'<form method="GET" action="/home/">'\
                +'<input type="submit" value="Home">'\
                +'</form>'
    return HttpResponse(respuesta)

def redirectHome(request):
    respuesta = '<meta http-equiv="Refresh" content="0;\
                 url=http://127.0.0.1:8000/">'
    return HttpResponse(respuesta)





    
    
    
    
 
