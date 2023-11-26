import g4f


def ask(phrase: str):
    return g4f.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': phrase}],
        timeout=100,
    )
