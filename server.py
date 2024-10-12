from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import uuid
import cv2
import face_recognition

app = Flask(__name__)
# Configurar CORS para permitir solicitudes desde cualquier origen
CORS(app, resources={r"/*": {"origins": "*"}})  

# Carpeta donde se guardan las imágenes
image_folder = "image/"

# Si la carpeta no existe, la creamos
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# Ruta para guardar la imagen recibida
@app.route('/guardar_imagen', methods=['POST'])
def guardar_imagen():
    try:
        # Obtención de los datos de la imagen y el nombre de usuario
        data = request.json
        image_data = data.get('image')
        username = data.get('username')

        if not image_data or not username:
            return jsonify({'success': False, 'message': 'Faltan datos: imagen o nombre de usuario'}), 400

        # Decodificación de la imagen de base64 a bytes
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image_filename = os.path.join(image_folder, f'{username}_{uuid.uuid4()}.jpg')

        # Guardamos la imagen decodificada en el servidor
        with open(image_filename, 'wb') as f:
            f.write(image_bytes)

        print(f"Imagen guardada: {image_filename}")

        return jsonify({'success': True, 'message': 'Imagen guardada correctamente.', 'filename': image_filename}), 200
    except Exception as e:
        print(f"Error en /guardar_imagen: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Listas para guardar los encodings de los rostros conocidos y los nombres asociados
known_face_encodings = []
known_face_names = []

# Cargamos las imágenes existentes en la carpeta para hacer la comparación
def cargar_conocidos():
    global known_face_encodings, known_face_names
    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(image_folder, filename)
            image = cv2.imread(image_path)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)
            if face_encodings:
                known_face_encodings.append(face_encodings[0])
                known_face_names.append(filename.split("_")[0])
                print(f"Cargado encoding para: {filename.split('_')[0]}")
            else:
                print(f"No se detectaron rostros en la imagen: {filename}")

# Inicializamos los encodings conocidos al iniciar el servidor
cargar_conocidos()

# Función para iniciar sesión a partir del encoding facial
def iniciar_sesion(face_encoding_in_frame, tolerance=0.2):
    results = face_recognition.compare_faces(known_face_encodings, face_encoding_in_frame, tolerance=tolerance)
    if True in results:
        return known_face_names[results.index(True)]
    else:
        return None

# Ruta para reconocer rostros
@app.route('/recognize', methods=['POST'])
def recognize_face():
    try:
        # Verificamos que se reciba una imagen
        data = request.json
        if 'image' not in data:
            return jsonify({'success': False, 'message': 'No se recibió la imagen'}), 400

        image_data = data.get('image')
        print("Imagen recibida para reconocimiento.")

        # Decodificamos la imagen en base64 a bytes
        image_bytes = base64.b64decode(image_data.split(',')[1])

        # Guardamos la imagen temporalmente
        temp_image_path = "temp_image.jpg"
        with open(temp_image_path, 'wb') as f:
            f.write(image_bytes)

        print(f"Imagen temporal guardada en: {temp_image_path}")

        # Leemos la imagen guardada y detectamos los rostros
        image = cv2.imread(temp_image_path)
        face_locations = face_recognition.face_locations(image)
        
        # Si se detectan rostros, hacemos el reconocimiento
        if face_locations:
            face_encodings = face_recognition.face_encodings(image, face_locations)
            if not face_encodings:
                print("No se pudo obtener el encoding del rostro.")
                os.remove(temp_image_path)
                return jsonify({'success': False, 'message': 'No se pudo obtener el encoding del rostro'}), 200

            face_encoding_in_frame = face_encodings[0]
            usuario = iniciar_sesion(face_encoding_in_frame)
            if usuario:

                user_data = {
                    # 'username': usuario.username if hasattr(usuario, 'username') else usuario['username'],  # Asegúrate de adaptar esto según la estructura del objeto 'usuario'
                    'username': 'test',
                    # 'email': usuario.email if hasattr(usuario, 'email') else usuario['email'],
                    'email': 'test',
                    # 'name': usuario.name if hasattr(usuario, 'name') else usuario['name'],
                    'name': 'test',
                    'user': usuario
                }

                message = {
                    'success': True, 
                    'message': f'Inicio de sesión exitoso como: {usuario}',
                    'data': user_data
                }

                print(message['message'])
            else:
                message = {'success': False, 'message': 'Usuario no reconocido'}
                print(message['message'])
        else:
            message = {'success': False, 'message': 'No se detectó ningún rostro, inténtalo de nuevo'}
            print(message['message'])
        
        # Eliminamos la imagen temporal
        os.remove(temp_image_path)
        print(f"Imagen temporal {temp_image_path} eliminada.")

        return jsonify(message), 200
    
    except Exception as e:
        print(f"Error en /recognize: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Inicializamos la aplicación Flask
if __name__ == "__main__":
    app.run(debug=True)
