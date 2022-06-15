В этом уроке мы научились ограничивать доступ, давайте продолжим отрабатывать знания на практике.

Шаг 1. Клонируйте репозиторий
Вам предоставлен репозиторий. Склонируйте его.

Если в прошлом уроке вы использовали простую архитектуру, клонируйте этот (https://github.com/skypro-008/lesson19_project_easy_source).

Если в прошлом уроке вы использовали сложную архитектуру, клонируйте этот (https://github.com/skypro-008/lesson19_project_hard_source).

БД с данными уже должна быть в репозитории (файл movies.db).

Шаг 2. Создайте пользователя
Создайте модель и схему пользователя и добавьте к ней CRUD (views с методами GET/POST/PUT).

Описание модели пользователя:

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String)
	password = db.Column(db.String)
	role = db.Column(db.String)
Создайте пользователей в БД — двух обычных и одного администратора.

Добавьте в app.py этот кусок кода и вызовите функцию create_data в register_extensions.

def create_data(app, db):
    with app.app_context():
        db.create_all()

        u1 = User(username="vasya", password="my_little_pony", role="user")
        u2 = User(username="oleg", password="qwerty", role="user")
        u3 = User(username="oleg", password="P@ssw0rd", role="admin")

        with db.session.begin():
            db.session.add_all([u1, u2, u3])
Шаг 2.1. Добавьте методы генерации хеша пароля пользователя
Для сложной архитектуры — в слой с бизнес-логикой.

Для простой архитектуры — в модель пользователя (class User).

Для сложной архитектуры хешируем пароли с помощью pbkdf2_hmac.

config.py

# Добавляем константы в файл constants.py
PWD_HASH_SALT = b'secret here'
PWD_HASH_ITERATIONS = 100_000

# services/user.py, class UserService для сложной архитектуры
# models.py, class User для простой архитектуры

# Метод хеширование пароля
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS

def get_hash(password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")
Для простой архитектуры хешируем пароли с помощью md5.

def get_hash(self):
	return hashlib.md5(self.password.encode('utf-8')).hexdigest()
Шаг 3. Добавьте недостающие методы
У моделей Director и Genre отсутствуют методы POST, PUT, DELETE. Добавьте их.

[ ЕСЛИ ВЫ ДЕЛАЕТЕ СЛОЖНУЮ АРХИТЕКТУРУ ] Добавьте методы в сервис и в DAO.

Шаг 4. Добавьте эндпоинты аутентификации
Эндпоинт

Доступ

POST /auth/ — возвращает access_token и refresh_token или 401

PUT /auth/ — возвращает access_token и refresh_token или 401

Anonymous (кто угодно)

Anonymous (кто угодно)

POST /auth — получает логин и пароль из Body запроса в виде JSON, далее проверяет соотвествие с данными в БД (есть ли такой пользователь, такой ли у него пароль) и если всё оk — генерит пару access_token и refresh_token и отдает их в виде JSON.

PUT /auth — получает refresh_token из Body запроса в виде JSON, далее проверяет refresh_token и если он не истек и валиден — генерит пару access_token и refresh_token и отдает их в виде JSON.

Шаг 5. Ограничьте доступ на чтение
Защитите (ограничьте доступ) так, чтобы к некоторым эндпоинтам был ограничен доступ для запросов без токена. Для этого создайте декоратор auth_required и декорируйте им методы, которые нужно защитить.

Эндпоинт

Доступ

GET /directors/ + /directors/id

GET /movies/ + /movies/id

GET /genres/ + /genres/id

Authorized Required

Authorized Required

Authorized Required

Шаг 6. Ограничьте доступ на редактирование
Защитите (ограничьте доступ) так, чтобы к некоторым эндпоинтам был доступ только у администраторов ( user.role == admin ) Для этого создайте декоратор admin_required и декорируйте им методы, которые нужно защитить.

POST/PUT/DELETE /movies/ + /movies/id

POST/PUT/DELETE /genres/ + /genres/id

POST/PUT/DELETE /directors/ + /directors/id

Authorized Required + Role admin Required

Authorized Required + Role admin Required

Authorized Required + Role admin Required

Шаг 7. Добавьте регистрацию пользователя
Эндпоинт

Доступ

POST /users/ — создает пользователя

Anonymous (кто угодно)

Пример запроса:

POST /users/

{
	"username": "ivan",
	"password": "qwerty",
	"role": "admin"
}
Критерии приема домашнего задания:
 Используется декоратор ограничения доступа.
 Модель пользователя создана и используется.
 Для пароля применяется шифрование.
 Общедоступные эндпоинты общедоступны.
 Пользовательские эндпоинты доступны пользователям и администраторам.
 Администраторские эндпоинты доступны только администраторам.
Как сдавать задание
Загрузить программу на гитхаб и приложить в дз на платформе Skypro ссылку на файл на гитхабе.