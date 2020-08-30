import os
import threading, requests, shutil, codecs
import numpy as np

from utils.findface import get_count_of_faces

count_of_downloads = 0
count_of_threads = 10
urls_for_download = []
threads = []

def download_photo(name: str, url: str) -> None:
    if not(os.path.exists('users/'+str(name)+'.jpg')):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open('users/' + str(name) + '.jpg', 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

def download_photo_only_with_solo_face_on_it(name: str, url: str) -> bool:
    file_path = 'users/' + str(name) + '.jpg'
    face_found = False
    if not(os.path.exists(file_path)):
        download_photo(name, url)
        try:
            if get_count_of_faces(file_path) == 1:
                face_found = True
        except Exception as ex:
            print(ex)
        # Если не удалось найти единственное лицо на фотографии, 
        # то удаляем скачанную фотографию
        if not face_found:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
        global count_of_downloads
        count_of_downloads += 1
        #print(count_of_downloads)
    return face_found

def run(part: list) -> None:
    for s in part:
        s = s.split('|')
        # Получаем из строки идентификатор пользователя
        user_id = s[0]
        # И ссылку на фотографию 
        photo_url = s[1]
        download_photo_only_with_solo_face_on_it(name=user_id, url=photo_url)

if __name__ == '__main__':
    ff = codecs.open('ids.txt', 'r', encoding='utf8')
    for s in ff:
        urls_for_download.append(s)
    ff.close()
    print('Количество ссылок для скачивания: ', np.size(urls_for_download))
    parts = np.array_split(urls_for_download, count_of_threads)

    for part in parts:
        threads.append(threading.Thread(target=run, args=(part,)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()