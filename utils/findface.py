import dlib
import numpy as np
import nmslib
from skimage import io
from typing import Optional

sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
face_rec = dlib.face_recognition_model_v1('dlib_face_recognition_'
'resnet_model_v1.dat')
detector = dlib.get_frontal_face_detector()

# Настройки nmslib
index = nmslib.init(method='hnsw', space='l2',
                        data_type=nmslib.DataType.DENSE_VECTOR)
index.loadIndex('embeddings.bin')
query_time_params = {'efSearch': 400}
index.setQueryTimeParams(query_time_params)

def get_face_descriptor(filename: str) -> Optional[list]:
    img = io.imread(filename)
    dets = detector(img, 1)
    face_descriptor = None
    for _, d in enumerate(dets):
        shape = sp(img, d)
        try:
            face_descriptor = face_rec.compute_face_descriptor(img, shape)
            face_descriptor = np.array(face_descriptor)
        except Exception as ex:
            print(ex)
    return face_descriptor

def get_count_of_faces(filename: str) -> int:
    img = io.imread(filename)
    dets = detector(img, 1)
    return np.size(dets)