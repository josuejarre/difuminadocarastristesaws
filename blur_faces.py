#!/usr/bin/python3

import numpy as np
import cv2

def anonymize_face(buffer, response):
    # leemoa la imagen del buffer
    nparr = np.fromstring(buffer, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    height, width, _ = img.shape
#cambios
    for faceDetail in response['FaceDetails']:
        datoemocion=emocion(faceDetail)
        if faceDetail['Emotions'][datoemocion]['Type']=='SAD':
            box = faceDetail['BoundingBox']
            x = int(width * box['Left'])
            y = int(height * box['Top'])
            w = int(width * box['Width'])
            h = int(height * box['Height'])

            # develve la la zona de la cara
            roi = img[y:y+h, x:x+w]

            # aplicamos el borrado de la imagen en un area rectangular
            roi = cv2.GaussianBlur(roi, (83, 83), 30)

            # pone la zona borrosa en la imagen original y crea la nueva imagen con las caras borrosas
            img[y:y+roi.shape[0], x:x+roi.shape[1]] = roi

    print("El borrado de caras se ha ejecutado de manera exitosa")
    
    # codifica la imagen y devuelve la imagen con la cara borrada
    _, res_buffer = cv2.imencode('.jpg', img)
    return res_buffer

#funcion encargada de recorrer toda la lista de setimientos y devolver el sentimiento mas
#pesado
def emocion(cara):
    valorMaximo=0
    for i in range(0,7):
        if valorMaximo<=cara['Emotions'][i]['Confidence']:
            valorMaximo=i

    return valorMaximo
