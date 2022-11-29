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
#     os.chdir("..\TP2 (2C2022)\main")
    os.chdir("..\TP2 (2C2022)\main")

    with open(nombre_archivo, "r") as archivo:
        lector = csv.reader(archivo, delimiter=",")
def guardar_datos(datos, AUTO) -> None:
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
    diccionario_denuncias = {"Enero":2,"Febrero":4,"Marzo":5,"Abril":0,"Mayo":0,"Junio":6,"Julio":8,"Agosto":10,"Septiembre":0,"Octubre":1,"Noviembre":3,"Diciembre":4}
    mostrar_grafico_denuncias(diccionario_denuncias)


main()