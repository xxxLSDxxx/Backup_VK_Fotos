import requests
import os
import time
from datetime import datetime, date
from tqdm import tqdm


def vk_fotos(user_id, count_fotos, version=5.199):
    photos_info = {}
    url = 'https://api.vk.com/method/photos.get'
    params = {'owner_id': user_id, 'access_token': 'введите токен',
              'rev': 0, 'count': count_fotos, 'extended': 1, 'album_id': 'profile', 'photo_sizes': True, 'v': version}
    response = requests.get(url, params=params)
    for el in response.json()['response']['items']:
        for size in el['sizes']:
            if size['type'] == 'm' and el['likes']['count']not in photos_info:
                url_image = size['url']
                like = el['likes']['count']
                file_name = f'{like}.jpg'
                photos_info[like] = {"url": url_image, "size": size['type']}
                response = requests.get(url_image)
                with open(f'image//{file_name}', 'wb') as f:
                    f.write(response.content)
                    time.sleep(0.5)
            elif size['type'] == 'm' and like in photos_info:
                url_image = size['url']
                file_name = f'{like}_{
                    datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.jpg'
                photos_info[like] = {"url": url_image, "size": size['type']}
                response = requests.get(url_image)
                with open(f'Image//{file_name}', 'wb') as f:
                    f.write(response.content)
                    time.sleep(0.5)


def unload_ya(file):

    headers = {
        'Authorization': 'введите токен'}
    response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                            headers=headers,
                            params={'path': f'Image/{file}', 'overwrite': True})
    url_upload = response.json()['href']
    with open(f'image/{file}', 'rb') as image:
        response = requests.put(url_upload, files={'file': image})


def backup():
    vk_fotos(user_id, count_fotos)
    total = len(os.listdir('Image'))
    count = 0
    with tqdm(total=len(os.listdir('Image')), desc="Загрузка файлов...") as pbar:
        for file in os.listdir('Image'):
            count += 1
            pbar.set_description(f"Загружено {count} из {total}")
            unload_ya(file)
            pbar.update(100/total)


if __name__ == '__main__':
    user_id = '101405428'
    count_fotos = 5
    backup()
