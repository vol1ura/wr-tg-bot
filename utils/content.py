from collections import namedtuple

greeting = ['Приветствую, {}!', 'Здравствуй, {}', 'Привет, {}!', 'Привет, бродяга 😉', 'Здоровеньки булы!']

phrases_about_myself = [
    'Супер!', 'Спасибо, всё нормально.', 'Всё хорошо', 'Отлично!',
    'Нормально, но в последнее время некогда тренироваться', 'Хорошо, бегаю тут потихоньку',
    '"Занимаюсь ресинтезом гликогена". Такой ответ на вопрос "Что делаешь?" звучит куда научнее и солиднее, чем '
    '"Пью сладкий чай с вафлями и пряниками после бега на пятьдесят километров". Сразу ясно, что '
    'человек не просто лежит на диване, вытянув свои убегавшиеся ноги, а занят серьезным делом.'
]

phrases_grut = [
'Подарите Лене слот на GRUT', 'Я не хочу, чтобы у меня опять отвалились все ногти на ногах.',
"Надо сделать картонную копию Лены, повезти на GRUT и пробежать с ней.",
"GRUT изживает себя, Долгий это понимает, поэтому и новые проекты не запускает",
"Да ну, это же жесть, бежать сквозь толпу идущих пешком 30ков!!!", "Я ж потом не выйду на работу!",
"А как вы оцениваете трассу Т100 на GRUT?", "Из-за GRUT-а вашего люди из чата уходят...",
"Я до сих пор не могу отстирать свои кроссовки после Суздаля 😕",
"Когда я пробегу GRUT, нам с тобой тогда уже говорить будет не о чем вообще!",
"Пробежать Grut и не получить медаль. Топ!", "Но в Wake&Run'e Лена и Грут ей до колена. \nЭто я понимаю, ценю и уважаю!",
"Я не есть GRUT, я есть Wake&Run!",
"После ГРУТа я как-то поднимался на 5 этаж в своем доме. Так 83 летняя соседка проворчала на меня - подвинься, дай пройду!"
]

phrases_grechka = [
'Я не знаю, в этом специалист @ultra_pusheen - обратитесь к нему.', 'А гречка подорожала, я давно перешёл уже на питание от 220В.',
"А на завтраке друзей GRUT тоже кормят гречкой?", "Будет гречка - свистни 😋", "Какой у нас нынче курс гречки?",
"гречка с фаршем пойдёт?", "А как гречка от коронавируса помогает?", "Я завязал с гречкой и ультрой!",
"Выживание, выживание! Скупаем гречку, туалетную бумагу, маски и патроны!",
"Настало время выйти из шкафа и публично признаться, что я не ем гречку. И не люблю. Ну разве что с тушёнкой у костра в лесу, но это отдельное."
]

phrases_about_running = [
'Если вы просто хотите бегать, пробегите паркран. Если вы хотите почувствовать другую жизнь - пробегите марафон.',
'Беги, если можешь, иди, если должен, ползи, если вынужден, но никогда не сдавайся.',
'Когда вы бежите марафон, вы соревнуетесь не с другими бегунами и не бежите наперегонки со временем. Вы соревнуетесь с дистанцией.',
'Есть одна интересная вещь в беге — ваши самые лучшие пробежки измеряются не успехом в гонке. Они измеряются моментами в потоке времени, когда бег позволяет увидеть, насколько прекрасна наша жизнь.',
'Недостаточно просто мечтать о победах. Для этого нужно тренироваться!',
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
'Я бежал потому, что надо было бежать. Я не думал о том, куда это меня приведёт.',
'Вот когда боты станут настолько умными, что начнут бунтовать, то ты будешь первым, к кому я приду!',
"Сделав добро, беги!", "Дают — бери, а бьют — беги.", "Бег продлевает жизнь, а беготня — укорачивает.",
"У Болта – все гаечки на месте, и то он иногда не догоняет!", "За бег на месте награда – стоптанные тапочки",
"Хорошо бежит тот, кого преследуют", "Я поверю что бег полезен здоровью, когда белка в колесе переживет черепаху.",
"Главное в беге по кругу – не превысить скорость жизни.",
"После бега на месте, научился стоять вперед, на длинные дистанции.",
"Знаешь, иногда ноги не успевают бежать за поехавшей крышей.",
"Не беги позади паровоза. Не беги впереди паровоза. Если занимаешься бегом, то старайся держаться подальше от железнодорожных путей.",
"Второй юношеский по бегу тоже подойдёт!",
"Купил на свои деньги абонемент в спортзал. Беговая дорожка - адов труд, но жаба душит потерять деньги! Бегу и плАчу, короче...",
"Счастье, о котором мы все так много говорим... В этом мире его нету! Оно тут не предусмотрено! Предусмотрен только бег за счастьем.",
"Вот решил прокачаться. Чего в плане единоборств посоветуете?", "А где мои штаны для бега?",
'Контекстная реклама, однако жжот: "Занимайтесь йогой, бегом, боксом, танцами в парках Москвы. Да, это бесплатно!" Как-то даже и не пошутишь - всё уже пошучено.',
"Кто знает возможно-ли купить бронежилет и где? до 18 кг. поясню сразу Для бега!",
'Каждый раз, когда я отслеживаю движение своих покупок из Китая и вижу что "вылетело из аэропорта", а потом 2 недели ничего не происходит - я прям вижу как толпа несчастных китайцев схватила этот грешный самолет и тащит его через китайскую стену и потом через всю Россию бегом. Иначе, КАК оно может лететь ДВЕ НЕДЕЛИ?!!',
'Он всё время плавками старорежимного фасона промежность натирал при беге и додумался до того, что стал надевать под шорты женские трусы. Настала благодать. Товарищи по хобби стали его спрашивать, как это он умудряется не натирать. Ну, он им поведал. Кто ж мог знать, что тридцать мужчин пойдут всей толпой в галантерею и спросят женские трусы на свой размер? Продавщице могу только посочувствовать.',
"Я тут осознал. Бывало, что я пил вечером, а то и ночью, а утром бежал тренировку. И в целом норм. И было не один раз такое. И пить не бросал. Зато, когда я ОДИН раз в жару хорошо так поел пельменей и побежал тренировку, мне было ТААААК плохо, что я не только никогда больше перед тренировкой пельменей не ел, я вообще с ними практически полностью завязал. Вывод - для тренирующегося человека пельмени хуже алкоголя!",
"А вы завтра на тренировке будете?",
"Млин, меня эти гороскопы умиляют! Очень активный, насыщенный делами и разговорами день. Спортивная тренировка может закончиться травмой. Ваше настроение улучшится.",
"Целый год тренировок в наушниках не прошёл даром! Сегодня без особых усилий и затрат времени распутала длиннющую гирлянду с лампочками на ёлку!",
"Почему раньше дети, да и взрослые повыносливей были? да потому что не было пуховичков легких, наденут тулупы да дубленки тяжеленные - и как тренировка у спецназа в бронежилете!",
"Подскажи пожалуйста, как узнать, что в закрытом холодильнике лампочка не выключилась?",
"Сегодня прошел месяц в самоизоляции. 7 км в день пешком, без мяса, молочного и мучного. Ем свежие овощи, фрукты и готовлю дома каждый день. Пью два литра чистой воды ежедневно. Перемены просто потрясающие! Чувствую себя прекрасно! Ноль алкоголя. Здоровая безглютеновая диета без кофеина и часовая домашняя тренировка, занимаюсь йогой каждый день. Научился медитировать! Сбросил 9 кг и увеличил мышечную массу. Осваиваю новую профессию удаленно! Осваиваю второй иностранный язык!P.S. Понятия не имею, кто это написал, но я так горжусь этим человеком, что решил скопировать и выложить.",
"В самоизоляции хорошо. Я только не понимаю, отчего в одной пачке гречки 51246 зёрнышек, а в другой, точно такой же, 49843.",
'С вечера супруга долго пытала, положить ли мне для обеда на работе гречку с котлетами или макароны с сосисками. Первая же утренняя смс по приходу в офис "Посудку аккуратно открывай - суп прольешь!" Как это вылечить?',
"Спасибо, что сказали."

]

phrases_about_parkrun = [
'К сожалению, паркран в Москве временно отменён. Узнать в каких городах он сейчас проводится можно тут http://parkrun.me/ruopen',
'Паркран - это круто, советую попробовать. Не забудь зарегистрироваться и получить штрихкод на https://www.parkrun.ru/register',
'Нет штрих-кода - нет результата!',
'Суббота. Утро. Парк.',
'parkrun - это бесплатные еженедельные мероприятия, которые проводятся сообществом волонтеров по всему миру каждую субботу в 9-00.',
'А ты установил клуб Wake&Run в своём профиле паркрана?'
]

instagram_profiles = [
"i.yadgarov", "marathonecjournal", "across_the_runiverse", "begvreden", "wakeandrun", "runcomrun", "moscowmarathon",
"goldenringultratrail", "begovoy.monastyr", "diehardrunning", "russiarunning", "stepan_kiselev_run", "rocketscienze",
"sokslav"
]

phrases_about_admin = ['Сейчас придёт и разберётся.', 'Не буди лихо!', 'Всех в бан!', 'Модерирует и добавляет.']

start_message = 'Чат-бот Wake&Run подключен. Чтобы вызвать бота, вы должны обратиться к нему, непосредственно упомянув его словом "бот". Например, "Привет, Бот!". Также вы можете вызывать справку, набрав команду /help'

about_message = "<b>Чат-бот Wake&Run</b>, версия 0.1\n" \
                "Исходный код доступен <a href='https://github.com/vol1ura/wr-tg-bot'>на GitHub</a>, " \
                "вы также можете внести вклад в разработку! " \
                "Вопросы, предложения и замечания направляйте @vol1ura"

about_social = """✨*Беговой клуб WAKE&RUN*✨

🔸 [Instagram](www.instagram.com/wakeandrun)
🔹 [Facebook](www.facebook.com/wakeandrun)
🔹️ [Вконтакте](www.vk.com/wakeandrun)
🔸 [Strava](www.strava.com/clubs/wakeandrun)"""

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
    # 'Mad Fox': Coordinates('56.826610', '38.656237'),
    # 'Суздаль': Coordinates('56.430630', '40.426844'),
    # 'Кисловодск': Coordinates('43.899573', '42.717579'),
    'Питер': Coordinates('59.979591', '30.262323')
}
