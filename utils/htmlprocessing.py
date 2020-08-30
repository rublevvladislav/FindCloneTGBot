import requests
from lxml import html

def get_url_of_face_with_id(id: int) -> str:
    s = ''
    with open('associations.txt', 'r') as file_:
        for line in file_:
            w = str(id) + '|'
            if line.find(w) == 0:
                s = line.split('|')[1]
    s = 'https://vk.com/id' + s.split('_')[0]
    for bad_symbols in ['.txt', '.npy', '.jpg','\n']:
        s = s.replace(bad_symbols, '')
    return s

def get_name_for_url(url):
    tree = html.fromstring(requests.get(url).content)
    return str(tree.xpath('//title/text()')[0]).split('|')[0]