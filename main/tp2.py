#import speech_recognition as sr
from os import path
import csv
import os


def lectura(datos) -> None:
    id:int=0
    
    nombre_archivo ="reclamos.csv"
    with open( nombre_archivo,"r") as archivo:
        lector = csv.reader(archivo, delimiter=",")
        next(lector, None)
        for row in archivo:
            id+=1
            row=row.split(',')
            datos.append({'id':id,'Timestamp':row[0],'Telefono_celular':row[1],'coord_latitud':row[2],'coord_longitud':row[3],'ruta_foto':row[4],'descripcion_texto':row[5],'ruta_Audio':row[6][:len(row[6])-1]})
   

def transcribir_audio(datos):
    os.chdir("audios")
    for i in datos:
        AUDIO:str= i['ruta_Audio']
        recgnizer = sr.Recognizer()
        with sr.AudioFile(AUDIO) as source:
            audio = recgnizer.record(source)

        try:
            print("Google Speech Recognition thinks you said " + recgnizer.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


def guardar_datos(datos:list) -> None:

    archivo: str = 'BaseDenuncias.csv'
    campos: tuple = ('Timestamp', 'Teléfono', 'Dirección_infracción', 'Localidad', 'Provincia', 'patente', 'descripción_texto', 'descripción_audio')

    with open(archivo,"w",newline = '') as f:
        csv_writer = csv.writer(f,delimiter = ",")
        csv_writer.writerow(campos)
        for denuncia in datos:
            csv_writer.writerow((denuncia["id"], denuncia["Timestamp"], denuncia["Telefono_celular"], denuncia["descripcion_texto"]))


def main():
    datos : list[dict]=[]
    lectura(datos)
    guardar_datos(datos)
    #transcribir_audio(datos)
    
main()