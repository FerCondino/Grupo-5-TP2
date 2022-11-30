import csv
import os
import googlemaps
import speech_recognition as sr
import matplotlib.pyplot as plt
import numpy as np
from pruebaredneuronal import detectar_patente
import cv2
OPCIONES: tuple = (
    "1-Listar denuncias cerca del estadio de Boca Juniors.",
    "2-Listar denuncias cerca del estacio de River Plate.",
    "3-Listar todas las infracciones dentro del centro de la ciudad, dado por el cuadrante, Av. Callao, Av. Rivadavia, Av. Córdoba, Av. Alem."
    "4-Emitir alerta por auto robado."
    "5-Ingresar patente."
    "6-Mostrar grafico de las denuncias mensuales."
    "7-Salir."
)

def lectura() -> list:
    id: int = 0
    datos: list[dict] = []
    nombre_archivo = "reclamos.csv"
    os.chdir("..\Grupo-5-TP2/main")

    with open(nombre_archivo, "r") as archivo:
        lector = csv.reader(archivo, delimiter=",")
        next(lector, None)
        for row in archivo:
            id += 1
            row = row.split(',')
            datos.append({'id': id, 'Timestamp': row[0], 'Telefono_celular': row[1], 'coord_latitud': row[2],
                         'coord_longitud': row[3], 'ruta_foto': row[4], 'descripcion_texto': row[5], 'ruta_Audio': row[6][:len(row[6])-1]})
    return datos


def transcribir_audio(datos) -> str:
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


def localizacion(lat, long):
    GOOGLE_API_KEY = "AIzaSyDL9J82iDhcUWdQiuIvBYa0t5asrtz3Swk"
    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
    reverse_geocode_result = gmaps.reverse_geocode((lat, long))
    ubi = []
    direccion = reverse_geocode_result[0]['formatted_address'].split(',')[0]
    localidad = reverse_geocode_result[0]['address_components'][2].get(
        'long_name')
    provincia = reverse_geocode_result[0]['address_components'][2].get(
        'short_name')
    ubi.append(direccion)
    ubi.append(localidad)
    ubi.append(provincia)
    return ubi

def localizacion_Lat_Long(lat, long):
    GOOGLE_API_KEY = "AIzaSyDL9J82iDhcUWdQiuIvBYa0t5asrtz3Swk"
    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
    reverse_geocode_result = gmaps.reverse_geocode((lat, long))
    ubi = []
    direccion = reverse_geocode_result[0]['formatted_address'].replace(",", "")
    localidad = reverse_geocode_result[0]['address_components'][2].get(
        'long_name')
    provincia = reverse_geocode_result[0]['address_components'][2].get(
        'short_name')
    ubi.append(direccion)
    ubi.append(localidad)
    ubi.append(provincia)
    return ubi

def localizacionUbi(baseDenuncia):
    GOOGLE_API_KEY = "AIzaSyDL9J82iDhcUWdQiuIvBYa0t5asrtz3Swk"
    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
    geocode_result = gmaps.geocode(baseDenuncia)
    coordenadas = []
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]
    coordenadas.append(lat)
    coordenadas.append(lon)
    return coordenadas

def guardar_datos(datos, AUTO) -> None:
    main_path = os.getcwd()

    archivo: str = 'BaseDenuncias.csv'
    campos: tuple = ('Timestamp', 'Teléfono', 'Direcc_infracción', 'Localidad',
                     'Provincia', 'patente', 'descrip_texto', 'descrip_audio')

    os.chdir(main_path)
    patente: str = detectar_patente(AUTO)

    with open(archivo, "w", newline='') as f:
        csv_writer = csv.writer(f, delimiter=",")
        csv_writer.writerow(campos)
        os.chdir("audios")
        for denuncia in datos:
            lat = denuncia.get('coord_latitud')
            long = denuncia.get('coord_longitud')
            ubi = localizacion(lat, long)
            descripcion_audio: str = transcribir_audio(denuncia)
            csv_writer.writerow((denuncia["id"], denuncia["Timestamp"], denuncia["Telefono_celular"],
                                ubi[0], ubi[1], ubi[2], patente.upper(), denuncia["descripcion_texto"], descripcion_audio))

def centro_ciudad(datos):
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
            for i in infracciones_centro:
                print("\n")
                print("Se encontraron infracciones en el centro de la ciudad, cantidad: ",len(infracciones_centro))
                print("Horario de la infraccion ", i.get("Timestamp"),"Patente", i.get("patente"),"Direccion", i.get("Direcc_infracción"))
        else:
            print("No se encontraron infracciones en el centro de la ciudad")
        
    return infracciones_centro

def mostrar_grafico_denuncias(denuncias:dict) -> None:
    """
    Pre:Recibe un diccionario donde cada key es un mes del año y cada value es la cantidad de denuncias que hubo en ese mes.
        Donde los meses se guardan en una lista "x", y la cantidad de denuncias en otra lista "y"
    Post:
    """
    plt.style.use('_mpl-gallery')
    x: list = []
    y: list = []

    for key,value in denuncias.items():
        x.append(key)
        y .append(value)
    
    plt.plot(x,y)
    plt.show()

def validar_dato_ingresado(entrada: str) -> bool:
    """
    Pre:Recibe un dato ingresado por el usuario para validar si es un dato numerico
    Post: devuelve True en caso de que sea numerico y False en caso contrario.
    """
    while ((entrada.isnumeric()) == False):
        entrada = input(f"Error no ingresó un numero. Ingrese el número: ")
    return entrada

def mostrar_opciones(OPCIONES) -> None:
    print("Menu de opciones:")
    for x in range(len(OPCIONES)):
        print(f"{x + 1}) {OPCIONES[x]}")

def cargar_denuncias_mensuales(datos: list, denuncias_mensuales: dict) -> dict:
    return denuncias_mensuales

def menu (datos: list, denuncias_mensuales: dict) ->None:
    mostrar_opciones(OPCIONES)
    #"1-Listar denuncias cerca del estadio de Boca Juniors.",
    #"2-Listar denuncias cerca del estacio de River Plate.",
    #"3-Listar todas las infracciones dentro del centro de la ciudad, dado por el cuadrante, Av. Callao, Av. Rivadavia, Av. Córdoba, Av. Alem."
    #"4-Emitir alerta por auto robado."
    #"5-Ingresar patente."
    #"6-Mostrar grafico de las denuncias mensuales."
    #"7-Salir."

    op: int = input("ingrese una opcion:")
    op = int(validar_dato_ingresado(op))
    while op > 7 or op < 1:
        print("Error:Debe ingresar una opcion valida.")
        mostrar_opciones(OPCIONES)
        op = input("Ingrese una opcion valida:")
        op = int(validar_dato_ingresado(op))

    while op != 7:

        if op == 1 :
            pass

        elif op == 2:
            pass

        elif op == 3:
            print(centro_ciudad(datos))

        elif op == 4:
            pass    
            #alerta auto robado.

        elif op == 5:
            #ingresar patente
            patente: str = input("Ingrese el numero de patente:\n")
            patente.upper()
            for denuncia in datos:
                if patente == denuncia[6]:
                    #mostrar la fotografía asociada a la misma y un mapa de google con la
                    cv2.imshow("Imagen",denuncia["Ruta foto"])
                    cv2.waitKey(0)
                    cv2.destroyAllWindows 
                    #ubicación de la misma marcada con un punto.

        elif op == 6:
            cargar_denuncias_mensuales(datos, denuncias_mensuales)
            mostrar_grafico_denuncias(denuncias_mensuales)


        mostrar_opciones(OPCIONES)
        op = input("ingrese una opcion:")
        op = int(validar_dato_ingresado(op))
        while op > 7 or op < 1:
            print("Error:Debe ingresar una opcion valida.")
            mostrar_opciones(OPCIONES)
            op = input("Ingrese una opcion valida:")
            op = int(validar_dato_ingresado(op))
    

def main():
    AUTO: str = 'WhatsApp Image 2022-11-28 at 20.51.11.jpg'
    datos: list[dict] = lectura()
    guardar_datos(datos,AUTO)
    denuncias_mensuales: dict = {
    "Enero":0,
    "Febrero":0,
    "Marzo":0,
    "Abril":0,
    "Mayo":0,
    "Junio":0,
    "Julio":0,
    "Agosto":0,
    "Septiembre":0,
    "Octubre":0,
    "Noviembre":0,
    "Diciembre":0
    }
    menu(datos,denuncias_mensuales)

main()