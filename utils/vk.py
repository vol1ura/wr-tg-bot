import random
import vk_requests


owner_id = -121950041  # group or user id on VK.com
albums_id = ['wall', 256663165, 244707630]  # id of best albums of this owner_id


def get_random_photo(token):
    api = vk_requests.create_api(service_token=token)
    album_id = random.choice(albums_id)
    photos_wall_parkrun_kuzminki = api.photos.get(owner_id=owner_id, album_id=album_id)
    random_photo = random.choice(photos_wall_parkrun_kuzminki['items'])
    return sorted(random_photo['sizes'], key=lambda x: -x['height'])[2]['url']
