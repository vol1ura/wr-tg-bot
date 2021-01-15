from collections import namedtuple

greeting = ['Приветствую, {}!', 'Здравствуй, {}', 'Привет, {}!', 'Привет, бродяга 😉', 'Здоровеньки булы!']

phrases_about_myself = [
    'Супер!', 'Спасибо, всё нормально.', 'Всё хорошо', 'Отлично!',
    'Нормально, но в последнее время некогда тренироваться', 'Хорошо, бегаю тут потихоньку'
]

phrases_about_running = [
'Если вы просто хотите бегать, пробегите паркран. Если вы хотите почувствовать другую жизнь - пробегите марафон.',
'Беги, если можешь, иди, если должен, ползи, если вынужден, но никогда не сдавайся.',
'Когда вы бежите марафон, вы соревнуетесь не с другими бегунами и не бежите наперегонки со временем. Вы соревнуетесь с дистанцией.',
'Есть одна интересная вещь в беге — ваши самые лучшие пробежки измеряются не успехом в гонке. Они измеряются моментами в потоке времени, когда бег позволяет увидеть, насколько прекрасна наша жизнь.',
'Не достаточно просто мечтать о победах. Для этого нужно тренироваться!',
'Вы можете продолжать бежать, и тогда ваши ноги будут болеть неделю. А можете сойти с дистанции, и тогда ваша душа будет болеть всю жизнь.',
'Бег — это величайшая метафора для жизни, потому что ты получаешь от него столько же, сколько в него вкладываешь.',
'Чем быстрее бежишь, тем больше кажется, что тебя в самом деле преследуют.',
'Если хочешь быть сильным — бегай, хочешь быть красивым — бегай, хочешь быть умным — бегай, хочешь быть здоровым — быстро бегай, хочешь быть живым — бегай тем более...',
'Если ты устаешь от ходьбы — беги.', 'Бег продлевает жизнь, а беготня укорачивает.',
'Я бы тебя обогнал, даже если бы бежал спиной вперёд.',
'Иногда нам не везёт в любви, и в таких случаях я начинаю пробежки.',
'Если не бегаешь, пока здоров, придется побегать, когда заболеешь',
'Если встречный ветер усиливается, значит, ...ты набираешь скорость.',
'Самое главное – это не скорость и не расстояние. Самое главное – постоянство: бегать ежедневно, без перерывов и выходных.',
'Великим бегуном я никогда не был и не буду.',
'Я бежал потому, что надо было бежать. Я не думал о том, куда это меня приведёт.'
]

phrases_about_parkrun = [
'К сожалению, паркран в Москве временно отменён. Узнать в каких городах он сейчас проводится можно тут http://parkrun.me/ruopen',
'Паркран - это круто, советую попробовать. Не забудь зарегистрироваться и получить штрихкод на https://www.parkrun.ru/register',
'Нет штрих-кода - нет результата!',
'Суббота. Утро. Парк.',
'parkrun - это бесплатные еженедельные мероприятия, которые проводятся сообществом волонтеров по всему миру каждую субботу в 9-00.'
]

instagram_profiles = [
"i.yadgarov", "marathonecjournal", "across_the_runiverse", "begvreden", "wakeandrun", "runcomrun", "moscowmarathon",
"goldenringultratrail", "begovoy.monastyr", "diehardrunning", "russiarunning", "stepan_kiselev_run"
]

phrases_about_admin = ['Сейчас придёт и разберётся.', 'Не буди лихо!', 'Всех в бан!', 'Модерирует и добавляет.']

start_message = 'Чат-бот Wake&Run подключен. Чтобы вызвать бота, вы должны обратиться к нему, непосредственно упомянув его словом "бот". Например, "Привет, Бот!". Также вы можете вызывать справку, набрав команду /help'

about_message = "Чат-бот Wake&Run, версия 0.1\nВопросы, предложения и замечания можно направлять разработчику @vol1ura"

about_social = """✨*Беговой клуб WAKE&RUN*✨

🔸 [Instagram](www.instagram.com/wakeandrun)
🔹 [Facebook](www.facebook.com/wakeandrun)
🔹️ [Вконтакте](www.vk.com/wakeandrun)
🔸 [Strava](www.strava.com/clubs/wakeandrun)"""

# TODO добавить ссылки на геопозицию и маркдаун
about_training = """📆 Тренировки проходят три раза в неделю:

🕖 вторник 19:00 🚦 [кафе Сок](https://yandex.ru/maps/-/CCUINOR2XB) \(напротив Третьяковки\)
🕗 четверг 20:00 🌲 [парк Кузьминки](https://yandex.ru/maps/-/CCUINOUylB)
🕗 четверг 20:00 🌳 [парк Олимпийская деревня](https://yandex.ru/maps/-/CCUINOas0A)
🕘 воскрeсенье 09:00 🌲 [парк Кузьминки](https://yandex.ru/maps/-/CCUINOUylB)

При нажатии на гиперссылку отроется карта с точкой встречи\.
"""

Coordinates = namedtuple('coordinates', 'lat lon')
places = {
    'Кузьминки': Coordinates('55.693191', '37.778019'),
    'Центр Москвы': Coordinates('55.738547', '37.611002'),
    'Олимпийская деревня': Coordinates('55.680273', '37.477918'),
    'Сочи': Coordinates('43.585472', '39.723089'),
    'Mad Fox': Coordinates('56.826610', '38.656237'),
    'Суздаль': Coordinates('56.430630', '40.426844'),
    'Кисловодск': Coordinates('43.899573', '42.717579'),
    'Питер': Coordinates('59.979591', '30.262323'),
    'Алушта': Coordinates('44.675153', '34.409127'),
}
