import random
import vk_requests


owner_id = -121950041  # group or user id on VK.com


def get_random_photo(token):
    api = vk_requests.create_api(service_token=token)
    photos_wall_parkrun_kuzminki = api.photos.get(owner_id=owner_id, album_id='wall')
    random_photo = random.choice(photos_wall_parkrun_kuzminki['items'])
    return sorted(random_photo['sizes'], key=lambda x: -x['height'])[2]['url']
