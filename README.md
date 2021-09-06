# api_yamdb
### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/kkkyifut/api_yamdb
```
```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение (windows):
```
python3 -m venv venv
```
```
venv\scripts\activate
```

Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

Выполнить миграции:
```
python3 manage.py migrate
```

Запустить проект:
```
python3 manage.py runserver
```

### Документация API
/redoc/

/swagger/

/api/v1/
