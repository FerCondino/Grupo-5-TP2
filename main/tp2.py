import csv
import os
import googlemaps
import speech_recognition as sr
import matplotlib.pyplot as plt
import numpy as np
from pruebaredneuronal import detectar_patente


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


def main():
    AUTO: str = 'WhatsApp Image 2022-11-28 at 20.51.11.jpg'
    datos: list[dict] = lectura()
    guardar_datos(datos, AUTO)
    diccionario_denuncias: dict = {
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
    mostrar_grafico_denuncias(diccionario_denuncias)


main()