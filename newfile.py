import requests
import os
import time
from config import access_token, user_id, token_api
from datetime import datetime, date
from tqdm import tqdm


class VK:
    def __init__(self, access_token, api_token, version='5.199'):

        self.token = access_token
        self.token_api = api_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def vk_fotos(self):
        n = 0
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': user_id, 'access_token': self.token, 'rev': 0, 'count': 5,
                  'extended': 1, 'album_id': 'profile', 'photo_sizes': True, 'v': self.version}
        response = requests.get(url, params=params)
        for el in response.json()['response']['items']:
            for size in el['sizes']:
                if size['type'] == 'm' and el['likes']['count'] != 0:
                    url_image = size['url']
                    file_name = f'{el['likes']['count']}.jpg'
                    response = requests.get(url_image)
                    with open(f'image//{file_name}', 'wb') as f:
                        f.write(response.content)
                        time.sleep(0.5)
                elif size['type'] == 'z' and el['likes']['count'] == 0:
                    n += 1
                    url_image = size['url']
                    file_name = f'{el['likes']['count']}_{
                        datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.jpg'
                    response = requests.get(url_image)
                    with open(f'Image//{file_name}', 'wb') as f:
                        f.write(response.content)
                        time.sleep(0.5)

    def unload_ya(self, file):

        headers = {'Authorization': self.token_api}
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                headers=headers,
                                params={'path': f'Image/{file}', 'overwrite': True})
        url_upload = response.json()['href']
        with open(f'image/{file}', 'rb') as image:
            response = requests.put(url_upload, files={'file': image})

    def backup(self):
        vk.vk_fotos()
        total = len(os.listdir('Image'))
        count = 0
        with tqdm(total=len(os.listdir('Image')), desc="Загрузка файлов...") as pbar:
            for file in os.listdir('Image'):
                count += 1
                pbar.set_description(f"Загружено {count} из {total}")
                vk.unload_ya(file)
                pbar.update(100/total)


vk = VK(access_token, token_api)
vk.backup()
