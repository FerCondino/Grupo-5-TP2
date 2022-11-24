
import speech_recognition as sr
from os import path
import csv
import os


def lectura():
    datos : list[dict]=[]
    id:int=0
    os.chdir("../TP2 (2C2022)/main")
    nombre_archivo ="reclamos.csv"
    with open( nombre_archivo,"r") as archivo:
        lector = csv.reader(archivo, delimiter=",")
        next(lector, None)
        for row in archivo:
            id+=1
            row=row.split(',')
            datos.append({'id':id,'Timestamp':row[0],'Telefono_celular':row[1],'coord_latitud':row[2],'coord_longitud':row[3],'ruta_foto':row[4],'descripcion_texto':row[5],'ruta_Audio':row[6][:len(row[6])-1]})
    print(datos)
    return datos

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


def main():
    datos=lectura()
    transcribir_audio(datos)
main()