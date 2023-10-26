import requests
import os
from dotenv import load_dotenv
import random
import logging


def check_vk_error(response):
    if response.get('error'):
        raise requests.exceptions.HTTPError


def download_img(file_path, url):
    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def download_comic():
    file_path = 'comics.png'
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    number_of_comics = response.json()['num']
    random_number = random.randint(1, number_of_comics)
    comic_url = f'https://xkcd.com/{random_number}/info.0.json'
    comic_response = requests.get(comic_url)
    comic_response.raise_for_status()
    url_of_comic = comic_response.json()['img']
    download_img(file_path, url_of_comic)
    return comic_response.json()['alt']
    

def get_upload_url(access_token, group_id):
    payload = {
        'group_id': group_id,
        'access_token': access_token,
        'v': 5.131
    }
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params=payload)
    check_vk_error(response.json())
    response.raise_for_status()
    return response.json()['response']['upload_url']


def upload_photo(upload_url):
    with open('comics.png', 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
    check_vk_error(response.json())
    response.raise_for_status()
    return response.json()


def save_wall_photo(photo_server, photo, photo_hash, group_id, access_token):
        payload = {
            'server': photo_server,
            'photo': photo,
            'hash': photo_hash,
            'group_id': group_id,
            'access_token': access_token,
            'v': 5.131
        }
        url = 'https://api.vk.com/method/photos.saveWallPhoto'
        response = requests.post(url, params=payload)
        check_vk_error(response.json())
        response.raise_for_status()
        return response.json()


def post_photo(from_group, attachments, message, access_token, group_id):
    payload = {
        'owner_id': f'-{group_id}',
        'from_group': from_group,
        'attachments': attachments,
        'message': message,
        'access_token': access_token,
        'v': 5.131
        }
    url = 'https://api.vk.com/method/wall.post'
    response = requests.post(url, params=payload)
    check_vk_error(response.json())
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    load_dotenv()
    vk_access_token = os.environ['VK_ACCESS_TOKEN']
    vk_group_id = os.environ['VK_GROUP_ID']
    try:
        message = download_comic()
        upload_url = get_upload_url(vk_access_token, vk_group_id)
        response = upload_photo(upload_url)
        photo_server = response['server']
        photo = response['photo']
        photo_hash = response['hash']
        album_response = save_wall_photo(photo_server, photo, photo_hash, vk_group_id, vk_access_token)
        owner_id = album_response['response'][0]['owner_id']
        media_id = album_response['response'][0]['id']
        attachments = f'photo{owner_id}_{media_id}'
        from_group = 1
        post_photo(from_group, attachments, message, vk_access_token, vk_group_id)
    except requests.exceptions.HTTPError:
        logging.exception('Произошла ошибка при запросе к ВК или к xkcd')
    finally:
        os.remove('comics.png')
