import csv
import datetime
import os
import googlemaps
import speech_recognition as sr
import matplotlib.pyplot as plt
import numpy as np
from geopy import distance
from datetime import *
from pruebaredneuronal import detectar_patente
import cv2
import folium
import webbrowser


OPCIONES: tuple = (
    "Listar denuncias cerca del estadio de Boca Juniors.",
    "Listar denuncias cerca del estacio de River Plate.",
    "Listar todas las infracciones dentro del centro de la ciudad",
    "Emitir alerta por auto robado.",
    "Ingresar patente.",
    "Mostrar grafico de las denuncias mensuales.",
    "Salir."
)

GOOGLE_API_KEY: str = "AIzaSyDL9J82iDhcUWdQiuIvBYa0t5asrtz3Swk"


def lectura() -> list:

    '''
    Leo el archivo reclamos y lo guardo en una lista datos.
    Pre: 
    Post: Devuelve una lista con los datos del archivo reclamos.
    '''

    id: int = 0
    datos: list = []
    nombre_archivo: str = "reclamos.csv"
    os.chdir("..\Grupo-5-TP2/main")

    try:
        with open(nombre_archivo, "r") as archivo:
            lector = csv.reader(archivo, delimiter=",")
            next(lector, None)
            for row in archivo:
                id += 1
                row: list = row.split(',')
                datos.append({'id': id, 'Timestamp': row[0], 'Telefono_celular': row[1], 'coord_latitud': row[2],
                            'coord_longitud': row[3], 'ruta_foto': row[4], 'descripcion_texto': row[5], 'ruta_Audio': row[6][:len(row[6])-1]})
        
    except FileNotFoundError:
        print("No se encontró el archivo de reclamos")
        
    
    return datos
    
def transcribir_audio(datos, path) -> None:
    
    '''
    Paso a texto el audio proveniente de whatsapp.
    Pre: Recibe la lista datos con la ruta donde está guardado el audio.
    Post: No devuelve nada por ser solo un procedimiento.
    '''

    os.chdir(path+"/audios")
    AUDIO: str = datos['ruta_Audio']
    recgnizer = sr.Recognizer()
    with sr.AudioFile(AUDIO) as source:
        audio = recgnizer.record(source)

    try:
        return recgnizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(e))

def localizacion_lat_Long(lat, long) -> list:
    
    '''
    Obtengo una ubiación mediante una latitud y una longitud.
    Pre: Recibe dos strings.
    Post: Devuelve una lista con la ubiación que aportan ambas coordenadas.
    '''
    
    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
    reverse_geocode_result = gmaps.reverse_geocode((lat, long))
    
    ubi: list = []

    direccion: str = reverse_geocode_result[0]['formatted_address'].split(',')[0]
    localidad: str = reverse_geocode_result[0]['address_components'][2].get('long_name')
    provincia: str = reverse_geocode_result[0]['address_components'][2].get('short_name')
    
    ubi.append(direccion)
    ubi.append(localidad)
    ubi.append(provincia)
    
    return ubi

def localizacionUbi(direccion) -> list:

    '''
    Guarda en una lista un par de coordenadas.
    Pre: Recibe un string de una cierta dirección.
    Post: Devuelve una lista con una latitud y una longitud.
    '''

    GOOGLE_API_KEY = "AIzaSyDL9J82iDhcUWdQiuIvBYa0t5asrtz3Swk"
    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
    geocode_result = gmaps.geocode(baseDenuncia)

    coordenadas: list = []

    lat: str = geocode_result[0]["geometry"]["location"]["lat"]
    lon: str = geocode_result[0]["geometry"]["location"]["lng"]
    
    coordenadas.append(lat)
    coordenadas.append(lon)
    
    return coordenadas

def guardar_datos(datos) -> None:
    
    '''
    Guardo los reclamos de reclamos.csv en BaseDenuncias.csv.
    Pre: Recibe una lista datos.
    Post: No devuelve nada por ser un procedimiento.
    '''

    main_path = os.getcwd()

    archivo: str = 'BaseDenuncias.csv'
    campos: tuple = ('Timestamp', 'Teléfono', 'Direcc_infracción', 'Localidad',
                     'Provincia', 'patente', 'ruta_foto','descrip_texto', 'descrip_audio')

    os.chdir(main_path)

    with open(archivo, "w", newline='') as f:
        csv_writer = csv.writer(f, delimiter=",")
        csv_writer.writerow(campos)
        for denuncia in datos:
            lat: str = denuncia.get('coord_latitud')
            long: str = denuncia.get('coord_longitud')
            ubi: list = localizacion_lat_Long(lat, long)
            descripcion_audio: str = transcribir_audio(denuncia,main_path)
            patente: str = detectar_patente(denuncia.get('ruta_foto'),main_path)

            csv_writer.writerow(( denuncia["Timestamp"], denuncia["Telefono_celular"],
                                ubi[0], ubi[1], ubi[2], patente.upper(),denuncia["ruta_foto"], denuncia["descripcion_texto"], descripcion_audio))

def lecturaDenuncias(ruta_inicial) -> list:

    '''
    Lee todas las denuncias en BaseDenuncias.csv y las guarda en una lista.
    Pre: Recibe la ruta donde esta ubicado el archivo BaseDenuncias.
    Post: Devuelve la lista datos con cada denuncia leida.
    '''

    id: int = 0
    datos: list[dict] = []
    nombre_archivo: str = "BaseDenuncias.csv"
    os.chdir(ruta_inicial+"/main")

    try:
            with open(nombre_archivo, "r") as archivo:
                lector = csv.reader(archivo, delimiter=",")
                next(lector, None)
                for row in archivo:
                    id += 1
                    row: list = row.split(',')
                    datos.append({'id': id, 'Timestamp': row[0], 'Teléfono': row[1], 'Direcc_infracción': row[2],
                                'Localidad': row[3], 'Provincia': row[4],  'patente': row[5], "ruta_foto": row[6],'descrip_texto':row[7], 'descrip_audio':row[8]})
    
    except IOError:
        print("No se encontró el archivo BaseDenuncias. Compruebe que esta ubicado en la misma carpeta')")
    
    
    return datos

def centro_ciudad(datos) -> list:

    '''
    Valido que infracción se produjo dentro de un cierto cuadrante.
    Pre: Recibe una lista datos.
    Post: Devuelve una lista con las infracciones validas.
    '''

    callao_rivadavia = (-34.609011264866574, -58.39190378633095)
    callao_cordoba = (-34.5994954103333, -58.392975888179365)
    alem_rivadavia = (-34.60704028343274, -58.37036293050827)
    alem_cordoba = (-34.5982236139002, -58.370915557495614)
    
    infracciones_centro: list = []
    for denuncia in datos:
        coordenadas= localizacionUbi(denuncia["Direcc_infracción"])
        lat = float(coordenadas[0])
        long = float(coordenadas[1])
        
        if ((lat >= callao_rivadavia[0] or lat >= alem_rivadavia[0]) and (lat <= callao_cordoba[0] or lat <= alem_cordoba[0])) and ((long >= callao_cordoba[1] or long >= callao_rivadavia[1]) and (long <= alem_rivadavia[1] or alem_cordoba[1])):
            infracciones_centro.append(denuncia)
            
    if(len(infracciones_centro)>0):
        print("\n")
        print("Se encontraron infracciones en el centro de la ciudad, cantidad: ",len(infracciones_centro))
        for i in infracciones_centro:
            print("Horario de la infraccion ", i.get("Timestamp"),"Patente", i.get("patente"),"Direccion", i.get("Direcc_infracción"))
    else:
        print("No se encontraron infracciones en el centro de la ciudad")
        
    return infracciones_centro

def mostrar_grafico_denuncias(denuncias:dict,baseDenuncia) -> None:
    """
    Pre:Recibe un diccionario donde cada key es un mes del año y cada value es la cantidad de denuncias que hubo en ese mes.
        Donde los meses se guardan en una lista "x", y la cantidad de denuncias en otra lista "y"
    Post:
    """
    plt.style.use('_mpl-gallery')
    x: list = []
    y: list = []
             
    for key,value in denuncias.items():
        for i in baseDenuncia:
            date=datetime(int(i.get("Timestamp").split("-")[0]),int(i.get("Timestamp").split("-")[1]),int(i.get("Timestamp").split("-")[2].split(" ")[0]))
            formateado= date.strftime("%d %B %y").split(" ")[1]
            if key == formateado:
                value +=1
        x.append(key)
        y.append(value)
    plt.plot(x,y)
    plt.show()

def detectar_sospechoso(denuncias):

    '''
    Detecta patentes sospechosas y muestra por pantalla la ubicación y fecha.
    Pre: Recibe la lista denuncias.
    Post: No devuelve nada por ser un procedimiento.
    '''     
    
    try:
        with open('robados.txt', 'r') as archivo:
            print(os.getcwd())
            for robado in archivo:
                for denuncia in denuncias:
                    if (denuncia.get("patente") == robado.strip()):
                        print("\n")
                        print('------ALERTA------','\n')
                        print('------INFRACCIÓN DE AUTO SOSPECHOSO------', '\n')
                        print(f'Ubicación: {denuncia.get("Direcc_infracción")}, Fecha: {denuncia.get("Timestamp")}','\n')

    
    except IOError:
        print('No se encuentra el archivo robados.txt. Compruebe que esta ubicado en la misma carpeta')
                    
def distancia_kilometro(baseDenuncia, lugar: str) -> None:

    '''
    Muestra por pantalla si hubo infracciones a 1 km del monumental o de la bombonera.
    Pre: Recibe la lista baseDenuncia y un string lugar.
    Post: No devuelve nada por ser un procedimiento.
    '''
    
    if lugar == "bombonera":
        bombonera: tuple = (-34.63543610792076, -58.364793559470996)
        infracciones_kilometro_bom: list = []
        for denuncia in baseDenuncia:
            coordenadas: list= localizacionUbi(denuncia["Direcc_infracción"])
            lat = float(coordenadas[0])
            long = float(coordenadas[1])
            distancia_bombonera = distance.distance((lat,long), bombonera).km
            if distancia_bombonera <= 1:
                infracciones_kilometro_bom.append(denuncia)

        if(len(infracciones_kilometro_bom)>0):
            print("\n")
            print("Se encontraron infracciones a menos de 1km de la Bombonera, cantidad: ",len(infracciones_kilometro_bom))
            for i in infracciones_kilometro_bom:
                print("En la Bombonera : Horario de la infraccion ", i.get("Timestamp"),"Patente", i.get("patente"),"Direccion", i.get("Direcc_infracción"))

    if lugar == "monumental":   
        monumental: tuple = (-34.544512440093, -58.449832118513015)
        infracciones_kilometro_mon: list = []
        for denuncia in baseDenuncia:
            coordenadas: list = localizacionUbi(denuncia["Direcc_infracción"])
            lat = float(coordenadas[0])
            long = float(coordenadas[1])
            distancia_monumental = distance.distance((lat,long), monumental).km
        
            if distancia_monumental <= 1:
                infracciones_kilometro_mon.append(denuncia)
            
        if(len(infracciones_kilometro_mon)>0):
            print("\n")
            print("Se encontraron infracciones a menos de 1km del Monumental, cantidad: ",len(infracciones_kilometro_mon))
            for i in infracciones_kilometro_mon:
                print(" En el Monumental Horario de la infraccion ", i.get("Timestamp"),"Patente", i.get("patente"),"Direccion", i.get("Direcc_infracción"))
    
def buscar_patente(baseDenuncia) -> str:

    '''
    Busca en la lista baseDenuncia la patente de un auto.
    Pre: Recibe la lista baseDenuncia.
    Post: Devuelve el string patente si este existe, sino devuelve none.
    '''

    patente: str = input("Ingrese el numero de patente: \n")
    patente.upper()

    for denuncia in baseDenuncia:
        if patente == denuncia.get("patente"):
            os.chdir(os.getcwd()+'/fotodenuncias')
            try:
                img= cv2.imread(os.getcwd()+'/'+denuncia.get("ruta_foto"))
                #mostrar la fotografía asociada a la misma y un mapa de google con la
                cv2.imshow('ImageWindow', img)
                cv2.waitKey(0)
                cv2.destroyAllWindows 
                mostrar_en_mapa(denuncia)
                return img
            except:
                print("No se encontro la foto,intente mas tarde")
                return
    print("No hay un auto robado con esa patente")
    
def mostrar_en_mapa(denuncia):
    coordenadas= localizacionUbi(denuncia["Direcc_infracción"])
    lat = float(coordenadas[0])
    long = float(coordenadas[1])
    mapObj = folium.Map(location = [lat,long], zoom_start = 15)
    markerObj = folium.Marker(location = [lat,long])
    markerObj.add_to(mapObj)
    mapObj.save("map.html")
    webbrowser.open("map.html", new=2) 

    
def validar_dato_ingresado(entrada: str) -> bool:

    """
    Pre:Recibe un dato ingresado por el usuario para validar si es un dato numerico
    Post: devuelve True en caso de que sea numerico y False en caso contrario.
    """
    while ((entrada.isnumeric()) == False):
        entrada = input(f"Error no ingresó un numero. Ingrese el número: ")
    
    return entrada

def mostrar_opciones(OPCIONES) -> None:

    '''
    Muestra por pantalla las distintas opciones de un menú.
    Pre: Recibe la constante OPCIONES.
    Post: No devuelve nada por ser un procedimiento.
    '''

    print("Menu de opciones:")
    for x in range(len(OPCIONES)):
        print(f"{x + 1}) {OPCIONES[x]}")

def menu () -> None:

    '''
    Valida la opción elegida por el usuario.
    Pre: No recibe nada.
    Post: No devuelve nada por ser un procedimiento.
    '''
    #"1-Listar denuncias cerca del estadio de Boca Juniors.",
    #"2-Listar denuncias cerca del estacio de River Plate.",
    #"3-Listar todas las infracciones dentro del centro de la ciudad, dado por el cuadrante, Av. Callao, Av. Rivadavia, Av. Córdoba, Av. Alem."
    #"4-Emitir alerta por auto robado."
    #"5-Ingresar patente."
    #"6-Mostrar grafico de las denuncias mensuales."
    #"7-Salir."
    ruta_incial = os.getcwd()
    datos: list[dict] = lectura()
    guardar_datos(datos)
    baseDenuncia:list[dict] = lecturaDenuncias(ruta_incial)
    diccionario_denuncias: dict = {
    "January":0,
    "February":0,
    "March":0,
    "April":0,
    "May":0,
    "June":0,
    "July":0,
    "August":0,
    "September":0,
    "October":0,
    "November":0,
    "December":0
    }
    
    mostrar_opciones(OPCIONES)
    
    op: int = input("ingrese una opcion:")
    op = int(validar_dato_ingresado(op))
    while op > 7 or op < 1:
        print("Error:Debe ingresar una opcion valida.")
        mostrar_opciones(OPCIONES)
        op = input("Ingrese una opcion valida:")
        op = int(validar_dato_ingresado(op))

    while op != 7:

        if op == 1 :
            lugar: str = "bombonera"
            distancia_kilometro(baseDenuncia,lugar)

        elif op == 2:
            lugar: str = "monumental"
            distancia_kilometro(baseDenuncia,lugar)

        elif op == 3:
            centro_ciudad(baseDenuncia)

        elif op == 4:
            detectar_sospechoso(baseDenuncia)  

        elif op == 5:
            buscar_patente(baseDenuncia)

        elif op == 6:
            mostrar_grafico_denuncias(diccionario_denuncias,baseDenuncia)


        mostrar_opciones(OPCIONES)
        op = input("ingrese una opcion:")
        op = int(validar_dato_ingresado(op))
        while op > 7 or op < 1:
            print("Error:Debe ingresar una opcion valida.")
            mostrar_opciones(OPCIONES)
            op = input("Ingrese una opcion valida:")
            op = int(validar_dato_ingresado(op))
    
def main():
    menu()   
main()