import pytest

from utils import content

sets_of_phrases_to_try = [
    content.instagram_profiles, content.instagram_profiles, content.greeting,
    content.phrases_grut, content.phrases_grechka, content.phrases_about_admin,
    content.phrases_about_myself, content.phrases_about_parkrun, content.phrases_about_running
]


@pytest.mark.parametrize('phrases', sets_of_phrases_to_try)
def test_content_with_lists(phrases):
    assert bool(phrases) and isinstance(phrases, list)
    assert all(isinstance(elem, str) for elem in phrases)


phrases_to_try = [
    content.about_training, content.about_message, content.start_message, content.about_social
]


@pytest.mark.parametrize('phrases', phrases_to_try)
def test_content_with_strings(phrases):
    assert isinstance(phrases, str)
