import os
from utils.vk import get_random_photo


def test_get_random_photo():
    photo_url = get_random_photo(os.getenv('VK_SERVICE_TOKEN'))
    print(photo_url)
    assert isinstance(photo_url, str)
    assert photo_url.startswith('https://')
