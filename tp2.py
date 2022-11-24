
import speech_recognition as sr
from os import path
import csv
import os


def lectura():
    datos = list()
    os.chdir("tp2\Grupo-5-TP2")
    os.getcwd()
    nombre_archivo ="reclamos.csv"
    with open( nombre_archivo,"r") as archivo:
        lector = csv.reader(archivo, delimiter=",")
        next(lector, None)
        for row in archivo:
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