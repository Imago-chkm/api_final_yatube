# Проект «API для Yatube»

Учебный проект для ознакомления и изучения работы API для Django REST Framework.

### В проекте используются:

- [Python](https://www.python.org/) - язык программирования.
- [Django](https://www.djangoproject.com/) - фреймворк для веб-приложений на языке Python.
- [Django REST Framework](https://www.django-rest-framework.org/) - набор инструментов для создания веб-API.
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) - плагин аутентификации JSON Web Token для Django REST Framework.

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Imago-chkm/api_yatube.git
```
```
cd api_yatube
```
Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py migrate
```
Запустить проект:
```
python manage.py runserver
```
### Примеры запросов:
Пример №1:
```
http://127.0.0.1:8000/api/v1/posts/{{post_with_group}}/
```
Ответ:
```
{
    "id": 7,
    "text": "Пост с группой",
    "pub_date": "2025-02-17T15:55:37.189561Z",
    "author": "regular_user",
    "image": null,
    "group": 1
}
```
Пример № 2:
```
http://127.0.0.1:8000/api/v1/posts/?limit=1&offset=1
```
Ответ:
```
{
    "count": 1,
    "next": null,
    "previous": "http://127.0.0.1:8000/api/v1/posts/?limit=1",
    "results": []
}
```

