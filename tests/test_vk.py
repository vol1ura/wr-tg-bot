import os

from dotenv import load_dotenv
from utils.vk import get_random_photo

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def test_get_random_photo():
    photo_url = get_random_photo(os.getenv('VK_SERVICE_TOKEN'))
    print(photo_url)
    assert isinstance(photo_url, str)
    assert photo_url.startswith('https://')
