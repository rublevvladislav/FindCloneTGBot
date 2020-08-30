import os
import numpy as np
import nmslib
import threading
import queue

from skimage import io
from utils.findface import get_face_descriptor

# Настройки nmslib
index = nmslib.init(method='hnsw',
                        space='l2',
                        data_type=nmslib.DataType.DENSE_VECTOR)

count_of_points_in_index = 0

def run(files: list, result_queue: queue) -> None:
    for file in files:
        try:
            global count_of_points_in_index
            face_descriptor = get_face_descriptor('users/' + file)
            embedding = np.array(face_descriptor)
            result_queue.put_nowait(str(count_of_points_in_index) + '|' + file + '\n')
            index.addDataPoint(count_of_points_in_index, embedding)
            count_of_points_in_index += 1
            print(count_of_points_in_index)
        except Exception as ex:
            print(ex)

if __name__ == '__main__':
    num_of_threads = 5
    result_queue = queue.Queue()
    threads = []
    files = np.array_split(os.listdir('users'), num_of_threads)

    for m_files in files:
        threads.append(threading.Thread(target=run, args = (m_files, result_queue)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # Запись связей (номер вектора и id в файл)
    with open('associations.txt', 'a') as embedding_file:
        while not result_queue.empty():
            embedding_file.write(result_queue.get())

        index_time_params = {
                'indexThreadQty': 4,
                'skip_optimized_index': 0,
                'post': 2,
                'delaunay_type': 1,
                'M': 100,
                'efConstruction': 2000
            }
        # Запись индекса с векторами лиц в файл
        index.createIndex(index_time_params, print_progress=True)
        index.saveIndex('embeddings.bin')