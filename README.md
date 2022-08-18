# Discord-SaveRoles-Bot
Требуется Python последней версии, mysql/mariadb (локально или на удаленном сервере)
## Установка
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