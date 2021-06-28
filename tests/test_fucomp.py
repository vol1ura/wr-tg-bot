import pytest

from utils import fucomp

test_phrases = ['бот, покажи статью о беге', 'Бот, позови администратора',
                'Бот, покажи ссылки на клуб', 'Бот кто такой Максим Петрищев?',
                'бот, когда откроют паркраны?', 'бот, когда клубная тренировка?']

phrases_to_try = [fucomp.phrases_parkrun, fucomp.phrases_social, fucomp.phrases_admin,
                  fucomp.phrases_instagram, fucomp.phrases_schedule, fucomp.petristchev]


@pytest.mark.parametrize('phrase_set', phrases_to_try)
def test_compare(phrase_set):
    compare = list(map(lambda p: fucomp.bot_compare(p, phrase_set), test_phrases))
    assert sum(1 for b in compare if b) == 1


def test_compare_no_accost():
    compare = fucomp.bot_compare('без обращения к боту', fucomp.phrases_social)
    assert not compare


def test_best_answer():
    answer = fucomp.best_answer('бот, знаешь девиз?', fucomp.message_base_wr)
    print(answer)
    assert isinstance(answer, str)
    assert 'девиз' in answer
    answer = fucomp.best_answer('Бот, какие кроссовки лучше для кроссов?', fucomp.message_base_m)
    print(answer)
    assert isinstance(answer, str)
    assert 'кроссовки' in answer
