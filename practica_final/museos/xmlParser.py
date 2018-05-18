from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from urllib.request import urlopen
#import string   #string module. Useful to do string.function(text) where
                #function can be: upper, lower, join, split, replace, etc.

def normalize_whitespace(text):
    #Funcion que elimina los espacios redundantes de un string.
    return str.join(' ', str.split(text))

class myContentHandler(ContentHandler): #clase myContentHandler que hereda de
                                        #ContentHandler (de la cual usamos sus funciones)

    def __init__(self):
        self.inContent = 0  #variable booleana. Vale 0 o 1 en funcion de si tiene contenido o no.
        self.theContent = ""
        self.atributo = ""
        self.nombre = ""
        self.url = ""
        self.nombreVia = ""
        self.num = ""
        self.codigo = ""
        self.barrio = ""
        self.distrito = ""
        self.telefono = ""
        self.email = ""
        self.fax = ""
        self.accesibilidad = ""
        self.descripcion = ""
        self.dic = {}   #Cada museo sera un diccionario
        self.listDic = [] #Lista de diccionarios, uno por cada museo



    def startElement (self, name, attrs):
        if name == "atributo":
            self.atributo = normalize_whitespace(attrs.get('nombre'))
        if self.atributo in ['NOMBRE', 'CONTENT-URL', 'NOMBRE-VIA', 'NUM', 'CODIGO-POSTAL', 'BARRIO', 'DISTRITO', 'TELEFONO', 'EMAIL', 'FAX', 'ACCESIBILIDAD', 'DESCRIPCION-ENTIDAD']:
            self.inContent = 1

    def endElement (self, name):
        if self.inContent:
            self.theContent = normalize_whitespace(self.theContent)

        if self.atributo == 'NOMBRE':
            self.nombre = self.theContent
            self.dic[self.atributo] = self.nombre
            #print("NOMBRE: " + self.nombre)

        elif self.atributo == 'CONTENT-URL':
            self.url = self.theContent
            self.dic[self.atributo] = self.url

        elif self.atributo == 'NOMBRE-VIA':
            self.nombreVia = self.theContent
            self.dic[self.atributo] = self.nombreVia

        elif self.atributo == 'NUM':
            self.num = self.theContent
            self.dic[self.atributo] = self.num

        elif self.atributo == 'CODIGO-POSTAL':
            self.codigo = self.theContent
            self.dic[self.atributo] = self.codigo

        elif self.atributo == 'BARRIO':
            self.barrio = self.theContent
            self.dic[self.atributo] = self.barrio
            #print("BARRIO: " + self.barrio)

        elif self.atributo == 'DISTRITO':
            self.distrito = self.theContent
            self.dic[self.atributo] = self.distrito
            #print("DISTRITO: " + self.distrito)

        elif self.atributo == 'TELEFONO':
            self.telefono = self.theContent
            self.dic[self.atributo] = self.telefono

        elif self.atributo == 'EMAIL':
            self.email = self.theContent
            self.dic[self.atributo] = self.email

        elif self.atributo == 'FAX':
            self.fax = self.theContent
            self.dic[self.atributo] = self.fax

        elif self.atributo == 'ACCESIBILIDAD':
            if self.theContent == '1':
                self.accesibilidad = 'SI'
            else:
                self.accesibilidad = 'NO'

            self.dic[self.atributo] = self.accesibilidad
            #print("ACCESIBILIDAD: " + self.accesibilidad)

        elif self.atributo == 'DESCRIPCION-ENTIDAD':
            self.descripcion = self.theContent
            self.dic[self.atributo] = self.descripcion

        if name == "contenido":
            self.listDic.append(self.dic)
            self.dic = {}
            self.nombre = ""
            self.url = ""
            self.nombreVia = ""
            self.num = ""
            self.codigo = ""
            self.barrio = ""
            self.distrito = ""
            self.telefono = ""
            self.email = ""
            self.fax = ""
            self.accesibilidad = ""
            self.descripcion = ""

        self.inContent = 0
        self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

    def getLista(self):
        return self.listDic
"""
# --- Main prog

# Load parser and driver

theParser = make_parser()   #make_parser devuelve un XMLReader object (parseador).
theHandler = myContentHandler() #instancias la clase myContentHandler que hemos creado (manejador).
theParser.setContentHandler(theHandler) #al parseador le pasas el manejador.

# Ready, set, go!

xmlFile = urlopen('https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full')
theParser.parse(xmlFile)    #al parseador le pasas el documento XML. En esta linea se ejecuta la accion de parsear.

#lista = theHandler.getLista()
#print(lista)

print("Parse complete")
"""
