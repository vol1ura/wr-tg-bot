import pytest
from flask import url_for

from app import app as site
from wakeandrunbot import bot


@pytest.fixture
def app():
    return site


def test_bot_page(client):
    # GIVEN a Flask application configured for testing
    # WHEN the '/bot' page is requested (GET)
    response = client.get(url_for('bot_page'))
    # THEN check that the response is valid
    assert response.status_code == 200


def test_index_page(client):
    # GIVEN a Flask application configured for testing
    # WHEN the '/' page is requested (GET)
    response = client.get(url_for('index'))
    # THEN check that the response is valid
    assert response.status_code == 200


def test_webhook_page(client, monkeypatch):
    # GIVEN a Flask application configured for testing
    monkeypatch.setenv('WEBHOOK', 'test_webhook')
    monkeypatch.setattr(bot, 'remove_webhook', lambda: None)
    monkeypatch.setattr(bot, 'set_webhook', lambda url: None)
    # WHEN the '/' page is requested (GET)
    response = client.get(url_for('webhook'))
    # THEN check that the response is valid
    assert response.status_code == 200


@pytest.mark.skip
def test_get_message_page(monkeypatch, client, app):
    # GIVEN a Flask application configured for testing
    monkeypatch.setenv('API_BOT_TOKEN', 'test_token_bot')
    monkeypatch.setattr(bot, 'process_new_updates', lambda arg: None)
    monkeypatch.setattr('telebot.types.Update.de_json', lambda arg: None)
    # WHEN the '/TOKEN_BOT' page is requested (POST)
    with app.test_request_context('/'):
        response = client.post(url_for('getMessage'))
    # THEN check that the response is valid
    assert response.status_code == 200
