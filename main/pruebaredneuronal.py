import cv2
import numpy as np
import json
import os
import requests


def detectar_auto(AUTO,main_path) -> str:

    '''
    Detecto si la foto es un auto u otra cosa.
    Pre: Recibe la constante AUTO.
    Post: Devuelve el str con el objeto de la foto.
    '''

    net = cv2.dnn.readNet('yolov3.cfg', 'yolov3.weights')

    tipo_de_objetos: list = []
    with open('coco.names', "r") as f:
        tipo_de_objetos = f.read().splitlines()
    
    os.chdir(main_path+'/fotoDenuncias')
    img = cv2.imread(AUTO)
    altura, ancho, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
    net.setInput(blob)

    nombre_capas_salida = net.getUnconnectedOutLayersNames()
    capa_salida = net.forward(nombre_capas_salida)

    boxes: list = []
    confianzas: list = []
    class_ids: list = []

    for salida in capa_salida:
        for deteccion in salida:
            puntaje = deteccion[5:]
            class_id = np.argmax(puntaje)
            coincidencia = puntaje[class_id]
            if coincidencia > 0.9:
                
                center_x: int = int(deteccion[0]*ancho)
                center_y: int = int(deteccion[1]*altura)
                w: int = int(deteccion[2]*ancho)
                h: int = int(deteccion[3]*altura)

                x: int = int(center_x - w/2)
                y: int = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confianzas.append((float(coincidencia)))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confianzas, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    colores = np.random.uniform(0, 255, size=(len(boxes),3))

    for i in indices.flatten():
        x, y, w, h = boxes[i]
        objeto_detectado = str(tipo_de_objetos[class_ids[i]]) #objeto_detectado es la variable que dice que objeto es.
        coincidencia = str(round(confianzas[i],2))
        color = colores [i]
        cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
        cv2.putText(img, objeto_detectado + " " + coincidencia, (x, y+20), font, 2, (255,255,255), 2)


    cv2.imshow("Image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows

    return objeto_detectado


def detectar_patente(AUTO,main_path) -> str: 

    '''
    Detecto los caracteres de la patente del AUTO.
    Pre: Recibe la constante AUTO.
    Post: Devuelve un string patente.
    '''

    os.chdir(main_path)

    if detectar_auto(AUTO, main_path) == 'car':
        regions: list = ['ar']
        
        with open(AUTO,'rb') as fp:
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                data = dict(regions=regions),
                files = dict(upload=fp),
                headers = {'Authorization':'Token f72818aea8aaa386a6d3250fdbe67a8c87835fde'})
            patente: str = response.json()["results"] [0] ["plate"]
        
        return patente
    
    else:
        print("la imagen enviada no es un auto")
    
    return patente