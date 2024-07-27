import time


class UrTube:
    """
    users - список пользователей (dict( User.nickname: (password, age) ))
    videos - список видео (list(Video))
    current_user - текущий пользователь (User)
    """

    def __init__(self):
        self.users = {}
        self.videos = []
        self.current_user = None

    def log_in(self, nickname, password):
        """
        Ищет в users такие же логин и пароль.
        """
        if nickname in self.users:
            if hash(password) == self.users[nickname][0]:
                self.current_user = User(nickname, password, self.users[nickname][1])

    def register(self, nickname, password, age):
        """
        Добавляет пользователя в список, если такого пользователя еще нет.
        """
        if nickname not in self.users:
            self.users[nickname] = (hash(password), age)
            self.log_in(nickname, password)
        else:
            print(f"Пользователь {nickname} уже существует.")

    def log_out(self):
        """
        Сброс текущего пользователя на None.
        """
        self.current_user = None

    def add(self, *args):
        """
        Добавляет видео в videos, если такого видео еще нет.
        """
        for video in args:
            if video not in self.videos:
                self.videos.append(video)

    def get_videos(self, search_name):
        """
        Возвращает список видео, содержащих поисковое слово.
        """
        self.video_list = []

        for video in self.videos:  # поиск видео по запросу
            if search_name.lower() in video.title.lower():
                self.video_list.append(video.title)

        if len(self.video_list) != 0:  # возвращает список найденных видео, иначе возвращает None
            return self.video_list

    def watch_video(self, video_name):
        """
        Просмотр видео с проверкой ограничений.
        """
        if self.current_user == None:  # Проверка на вхождение в аккаунт
            print("Войдите в аккаунт, чтобы смотреть видео")
        else:
            for video in self.videos:
                if str(video) == video_name:  # поиск видео

                    if self.current_user.age < 18 and video.adult_mode:  # проверка на возраст
                        print("Вам нет 18 лет, пожалуйста покиньте страницу")
                    else:
                        self._play_video(video)

                    break  # если видео найдено, дальнейший поиск видео по имени не требуется

    def _play_video(self, video):
        """
        Проигрывание видео.
        """
        current_video_second = video.time_now  # запись переменной - до какой секунды было просмотрено видео до открытия

        # просмотр видео
        while current_video_second < video.duration:
            current_video_second += 1
            print(current_video_second, end=" ")
            time.sleep(1)  # пауза длительностью 1 секунда
        video.time_now = 0  # после просмотра сбросить записанное время
        print("Конец видео")


class Video:
    """
    title - заголовок (str)
    duration - продолжительность (int)
    time_now - секунда остановки (int)
    adult_mode - ограничение по возрасту (bool)
    """

    def __init__(self, title, duration, time_now=0, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = time_now
        self.adult_mode = adult_mode

    def __str__(self):  # возвращает название видео
        return self.title


class User:
    """
    nickname - имя пользователя (str)
    password - хэшированный пароль (int)
    age - возраст (int)
    """

    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = hash(password)
        self.age = age

    def __str__(self):  # возвращает имя пользователя
        return self.nickname


ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')
