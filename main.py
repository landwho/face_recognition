# import os
# import cv2
# import face_recognition

# image_folder = "image/"
# known_face_encodings = []
# known_face_names = []

# for filename in os.listdir(image_folder):
#     if filename.endswith(".jpg") or filename.endswith(".png"):
#         image_path = os.path.join(image_folder, filename)
#         image = cv2.imread(image_path)
#         face_locations = face_recognition.face_locations(image)
#         face_encodings = face_recognition.face_encodings(image, face_locations)
#         if face_encodings:
#             known_face_encodings.append(face_encodings[0])
#             known_face_names.append(filename)

# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame = cv2.flip(frame, 1)

#     face_locations_in_frame = face_recognition.face_locations(frame)

#     for face_location in face_locations_in_frame:

#         face_encoding_in_frame = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]
#         results = face_recognition.compare_faces(known_face_encodings, face_encoding_in_frame)
#         face_distances = face_recognition.face_distance(known_face_encodings, face_encoding_in_frame)

#         best_match_index = None
#         if results:
#             best_match_index = face_distances.argmin()

#         if best_match_index is not None and results[best_match_index]:
#             text = known_face_names[best_match_index]
#             print("TRUE")
#             color = (125, 220, 0)
#         else:
#             text = "Unknown"
#             color = (50, 50, 220)
            
#         cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), color, 2)
#         cv2.rectangle(frame, (face_location[3], face_location[2]), (face_location[1], face_location[2] + 30), color, -1)
#         cv2.putText(frame, text, (face_location[3], face_location[2] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

#     cv2.imshow("Frame", frame)

#     k = cv2.waitKey(1)
#     if k == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()








# import os
# import cv2
# import face_recognition

# image_folder = "image/"
# known_face_encodings = []
# known_face_names = []

# for filename in os.listdir(image_folder):
#     if filename.endswith(".jpg") or filename.endswith(".png"):
#         image_path = os.path.join(image_folder, filename)
#         image = cv2.imread(image_path)
#         face_locations = face_recognition.face_locations(image)
#         face_encodings = face_recognition.face_encodings(image, face_locations)
#         if face_encodings:
#             known_face_encodings.append(face_encodings[0])
#             known_face_names.append(filename)

# cap = cv2.VideoCapture(0)

# def iniciar_sesion(face_encoding_in_frame):
#     results = face_recognition.compare_faces(known_face_encodings, face_encoding_in_frame)
#     if True in results:
#         return known_face_names[results.index(True)]
#     else:
#         return None

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame = cv2.flip(frame, 1)

#     face_locations_in_frame = face_recognition.face_locations(frame)

#     for face_location in face_locations_in_frame:

#         face_encoding_in_frame = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]
#         usuario = iniciar_sesion(face_encoding_in_frame)

#         if usuario is not None:
#             print(f"Inició sesión como: {usuario}")
#             color = (0, 255, 0)  # Verde para usuarios reconocidos
#         else:
#             color = (0, 0, 255)  # Rojo para usuarios desconocidos

#         cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), color, 2)
#         cv2.rectangle(frame, (face_location[3], face_location[2]), (face_location[1], face_location[2] + 30), color, -1)
#         cv2.putText(frame, "Unknown" if usuario is None else usuario, (face_location[3], face_location[2] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

#     cv2.imshow("Frame", frame)

#     k = cv2.waitKey(1)
#     if k == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()








import os
import cv2
import face_recognition
import tkinter as tk

# Obtén la resolución de la pantalla usando tkinter
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

# Calcula el 80% de la resolución de la pantalla
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)

image_folder = "image/"
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
            known_face_names.append(filename)

cap = cv2.VideoCapture(0)

def iniciar_sesion(face_encoding_in_frame):
    results = face_recognition.compare_faces(known_face_encodings, face_encoding_in_frame)
    if True in results:
        return known_face_names[results.index(True)]
    else:
        return None

cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Frame", window_width, window_height)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    face_locations_in_frame = face_recognition.face_locations(frame)

    for face_location in face_locations_in_frame:
        face_encoding_in_frame = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]
        usuario = iniciar_sesion(face_encoding_in_frame)

        if usuario is not None:
            print(f"Inició sesión como: {usuario}")
            color = (0, 255, 0)  # Verde para usuarios reconocidos
        else:
            color = (0, 0, 255)  # Rojo para usuarios desconocidos

        cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), color, 2)
        cv2.rectangle(frame, (face_location[3], face_location[2]), (face_location[1], face_location[2] + 30), color, -1)
        cv2.putText(frame, "Unknown" if usuario is None else usuario, (face_location[3], face_location[2] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

    cv2.imshow("Frame", frame)

    k = cv2.waitKey(1)
    if k == 27:  # Presiona 'Esc' para salir
        break

cap.release()
cv2.destroyAllWindows()


