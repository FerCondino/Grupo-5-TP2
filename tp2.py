import os
import speech_recognition as sr
from os import path
import csv


def lectura():
    datos = list()
    directorio = os.getcwd()
    ruta_del_archivo = os.path.join(directorio, "reclamos.csv")
    with open(ruta_del_archivo, newline='', encoding="UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter=',')
        next(csv_reader) 
        for row in csv_reader:
            datos.append(row)
    print(datos)

def transcribir_audio():
    
    AUDIO = 'audioprueba1.wav'

    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), AUDIO)
    sara = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = sara.record(source)

    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + sara.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def main():
    lectura()
    
main()