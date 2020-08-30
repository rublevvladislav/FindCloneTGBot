import vk_api
import codecs
import time
import os

vk_session = vk_api.VkApi(token = os.getenv('VK_API_TOKEN'))
vk = vk_session.get_api()

# Код города (Бердск 1133, Новосибирск 99)
city_code = 1133
# Минимальный возраст, который ищем
min_age = 18
# Максимальный возраст, который ищем
max_age = 30
# 1-woman, 2-man
gender = 1

def find_peoples_and_write_to_file(city_code: int, min_age: int, max_age: int,
                                    gender: int, filepath = 'ids.txt') -> None:
    age = min_age
    ff = codecs.open(filepath, 'w', 'utf-8')
    while age <= max_age:
        # Месяц рождения
        b_month = 1
        # Качаем по очереди в зависимости от месяца рождения из-за ограничений апи
        while b_month <= 12:
            # Задержка, из-за ограничений апи
            time.sleep(4)
            z=vk.users.search(count=1000, 
            fields='id, photo_max_orig, first_name, last_name', 
            city=city_code, sex=gender, age_from=age, age_to=age, 
            birth_month=b_month, has_photo = 1)
            print('Count of users: ' + str(z['count']))
            b_month += 1
            for i in z['items']:
                s = str(i['id']) + '|' + str(i['photo_max_orig']) + \
                    '|' + str(i['first_name']) + '|' + \
                    str(i['last_name']) + '\n'
                ff.write(s)
        age += 1
    ff.close()
    print('Done')

if __name__ == '__main__':
    find_peoples_and_write_to_file(city_code, min_age, max_age, gender)