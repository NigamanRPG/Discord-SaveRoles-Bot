# Discord-SaveRoles-Bot
Требуется Python последней версии, mysql/mariadb (локально или на удаленном сервере)
# Вариант 1. Установка локально
```
git clone https://github.com/NigamanRPG/Discord-SaveRoles-Bot.git
cd Discord-SaveRoles-Bot
pip install -r requirements.txt
```
## Настройка
В файле config/example.json необходимо указать токен вашего бота, а также данные для подключение к базе данных mysql.
```json
{
    "TOKEN": "",
    "HOSTNAME": "",
    "PASSWD": "",
    "USERNAME": "",
    "DB": ""
}
```
## Запуск
```python bot.py``` или ```python3 bot.py```

После запуска, выполните команду для включения сохранения ролей на необходимой гильдии ```$save_role enable``` _(требуются права администратора)_. Для отключения функции воспользуйтесь командой ```$save_role disable```

# Вариант 2. Использование Docker
Требуется установить актуальную версию docker, mysql/mariadb (локально или на удаленном сервере).
Измените данные в файле config/example.json (см. раздел "Настройка").

Соберите и запустите контейнер.
```
docker build -t saveroles-bot .
docker run saveroles-bot
```
# Демонстрация
[demo.webm](https://user-images.githubusercontent.com/52179357/185404837-788d4a5c-d12f-44a1-b203-c800e2533ab2.webm)

