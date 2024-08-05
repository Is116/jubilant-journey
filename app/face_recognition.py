import dlib
import numpy as np

predictor = dlib.shape_predictor('app/models/shape_predictor_68_face_landmarks.dat')
face_rec = dlib.face_recognition_model_v1('app/models/dlib_face_recognition_resnet_model_v1.dat')

def recognize_faces(frame, faces):
    recognized_faces = []
    for face in faces:
        shape = predictor(frame, face)
        face_descriptor = face_rec.compute_face_descriptor(frame, shape)
        recognized_faces.append(np.array(face_descriptor))
    return recognized_faces
