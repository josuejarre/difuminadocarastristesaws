#importamos las librerias
import boto3, os, base64
from flask import Flask, request, Response, abort, jsonify
from dotenv import load_dotenv
from detect_faces import detect_faces
from blur_faces import anonymize_face
from compare_faces import looking_faces

#cargamos los datos de acceso
load_dotenv()
#ahora los asignamos a las variables
accesoId = os.environ.get('ACCESS_KEY_ID')
claveSecreta = os.environ.get('ACCESS_SECRET_KEY')
bucket_source = os.environ.get('BUCKET_SOURCE')
bucket_dest = os.environ.get('BUCKET_DEST')

main=Flask(__name__)

# Creamos el servicio s3 e introducimos las credenciales de las variables
s3 = boto3.Session(
    aws_access_key_id=accesoId,
    aws_secret_access_key=claveSecreta).resource('s3')
##añadir funcion de subir foto
@main.route('/api/subirImagen', methods=['POST'])
def subirImagen():
    try:
        with open(request.files['file'], request.files['filename']) as fd:
            response = s3.put_object(
                Bucket=bucket_source,
                Key=request.get_json().get('nombre'),
                Body=fd
            )
        #print(json.dumps(response, sort_keys=True, indent=4))
        print("Put Object exitoso")
        return True
    except FileNotFoundError:
        print("Archivo no encontrado")
        return False
    except Exception as e:
        print(str(e))
        return False



# api/analyze endpoint
@main.route('/api/analyze', methods=['POST'])
def analyzeImage():
    key = request.get_json()['key']
    if key is None:
        abort(400)

    try:
        response = detect_faces(key)

        fileObject = s3.Object(bucket_source, key).get()
        fileContent = fileObject['Body'].read()
        buffer_anon_img = anonymize_face(fileContent, response)

        img_enc = base64.b64encode(buffer_anon_img)
        img_dec = base64.b64decode(img_enc)
        s3.Object(bucket_dest, f"result_{key}").put(Body=img_dec)
    except Exception as error:
        print(error)
        abort(500)
    return Response(status=200)

@main.route('/api/comparar', methods=['POST'])
def comparadorRostros():
    keys = request.get_json()['keys']

    if keys is None:
        abort(400)

    try:
        response = looking_faces(keys)
        if len(response['FaceMatches'])>=1:
            for persona in response['FaceMatches']:
                if persona['Similarity']>=80:
                    print("hay una persona igual o si solo hay una es la misma persona")

        elif len(response['UnmatchedFaces'])>=1:
            print("No hay personas que se parezca")
    except Exception as error:
        print(error)
        abort(500)
    return Response(status=200)

# Run the app
if __name__ == "__main__":
    main.debug = True
    main.run()  # Running on http://127.0.0.1:5000/