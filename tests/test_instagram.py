import os

import pytest
from dotenv import load_dotenv

from utils.instagram import get_last_post

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


@pytest.mark.xfail
def test_get_last_post():
    username = os.environ.get('IG_USERNAME')
    password = os.environ.get('IG_PASSWORD')
    post_url, post = get_last_post(username, password, 'rocketscienze')
    assert isinstance(post, str)
    assert isinstance(post_url, str)
    assert post_url.startswith('https://')
    assert 1 <= len(post.split('\n\n')) <= 2
