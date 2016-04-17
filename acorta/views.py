
from django.shortcuts import render
from django.http import HttpResponse
from models import urlLargas, urlCortas
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

# ----------------- getDBLength -----------------
def getDBLength (DB_in):
    DB = DB_in.objects.all()
    length = 0
    for item in DB:
        length = length + 1
    return length

# ================= Vistas =================
# ----------------- homePage -----------------
@csrf_exempt
def homePage(request):
    # Creates file "URLs.pkl" for further use, if doesn't exists 
#    urlsLargas = 'URLsLong'
#    urlsCortas = 'URLsShort'
#    initFile((urlsLargas+'.pkl'))
#    initFile((urlsCortas+'.pkl'))
    # Loads data of files
#    urlLargas = {} # URL   SeqN
#    urlLargas = LoadURLs(urlsLargas)
#    urlCortas = {} # SeqN  URL
#    urlCortas = LoadURLs(urlsCortas)
#    seqNumb = len(urlLargas)
    seqNumb = getDBLength(urlLargas)
    print('Longitud de urlLargas = ' +  str(seqNumb))
    if request.method == 'GET':
        # _________________ GET _________________
        respuesta = '<html><body>'\
                    +'<form method="POST" action="">'\
                    +'URL: <input type="text" name="url"><br>'\
                    +'<input type="submit" value="Enviar">'\
                    +'</form>'
        urls = urlLargas.objects.all()
        respuesta+='<br>URLs En Cache:<ol>'
        for url in urls:
            respuesta += '<li>' + url.urlCorta + '=>' + url.urlLarga
        respuesta += '</ol>'\
        +'</body><title>Acortador</title>'\
        +'</html>'
                    
    elif request.method == 'POST' or request.method == 'PUT':
        # _________________ POST or PUT _________________
        print 'Recibido POST or PUT...'
        cuerpo=request.body.replace('%3A',':') # Recibo estos strings...
        cuerpo=cuerpo.replace('%2F','/')
        if cuerpo[0:4] == 'url=': # POST de formulario o poster con "url..."
            cuerpo = cuerpo[4:] # Quito el url=
        if cuerpo[0:7] != 'http://': # http:// en caso de no haberlo
            cuerpo = 'http://' + cuerpo
        print (cuerpo)
        try:
            # Por si acaso estoy metiendo una corta...
            print ('Buscando coincidencia entre las cortas...')
            urlLarga = urlCortas.objects.get(urlCorta=cuerpo)
            urlLarga = urlLarga.urlLarga # el objeto obtengo la string
            urlCorta = cuerpo
            respuesta = decorateHTML('<title>URL Acortada</title>'\
                                    +'<h3>URL corta ya incluida:</h3>'\
                                    +'<p1>URL Larga: <a href= '\
                                    +urlLarga + '>' + urlLarga + '</a></p>'\
                                    +'<p>URL Corta: <a href= '\
                                    +urlCorta + '>'\
                                    +urlCorta + '</a></p>')
            print ('Encontrada!')
        except:
            # Buscar la url larga recibida y devolver o crear
            try:
                print ('Buscando coincidencia entre las largas...')
                urlCorta = urlLargas.objects.get(urlLarga=cuerpo)
                urlCorta = urlCorta.urlCorta # el objeto obtengo la string
                print 'URL encontrada, devolviendo almacenada'
            except:
                print 'URL no encontrada, creando...'
                urlCorta = myURL()+'/'+str(seqNumb)
                # Almacenando en BD...
                urlAux = urlLargas(urlLarga=cuerpo, urlCorta=urlCorta)
                urlAux.save()
                urlAux = urlCortas(urlCorta=urlCorta, urlLarga=cuerpo)
                urlAux.save()
                print ('Creada!')
            respuesta = decorateHTML('<title>URL Acortada</title>'\
                                    +'<p1>URL Larga: <a href= '\
                                    +cuerpo + '>' + cuerpo + '</a></p>'\
                                    +'<p>URL Corta: <a href= '\
                                    +urlCorta + '>'\
                                    +urlCorta + '</a></p>')
            print ('homePage.POSTorPUT OK!')
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
#    urlsCortas = 'URLsShort'
#    initFile((urlsCortas+'.pkl'))
#    urlCortas = {} # SeqN  URL
#    urlCortas = LoadURLs(urlsCortas)
    print('Recibido GET/...')
    urlCorta = myURL()+'/'+str(int(recurso))
    
    try:
        print('Buscando en cortas...')
        urlLarga = urlCortas.objects.get(urlCorta=urlCorta)
        urlLarga = urlLarga.urlLarga
        respuesta = decorateHTML('<meta http-equiv="Refresh" content="0;'\
                                +'url='+urlLarga+'">')
        print('Encontrado!')
    except:
        print 'Detectada peticion inconsistente'
        respuesta = decorateHTML('<h3>Recurso no disponible</h3>'\
                                +'<p>Codigo de error: 404</p>')    
    return HttpResponse(respuesta)



"""
urlAux = urlLargas(urlLarga=key, urlCorta=value)
urlAux.save()

urlAux = urlCorta(urlCorta=key, urlLarga=value)
urlAux.save()

try:
    urlCorta_L = urlLargas.objects.get(urlLarga=key)
except:

try:
    urlLarga_L = urlCortas.objects.get(urlCorta=key)
except:

urls = urlLargas.objects.all()
        respuesta+='<br>URLs almacenadas actualmente:<ol>'
        for url in urls:
            respuesta += '<li><a href="' + url.name + '">'\
                        + url.name + '</a>'
        respuesta += '</ol>'
"""




    
    
    
    
 
