# Инструкция по запуску

Создайте копию файла .env с названием .env.local (не попадет в репозиторий!), укажите токен телеграм бота, созданного через бота @BotFather. Создайте виртуальное Python окружение следующими командами в зависимости от вашей операционной системы:

## Запуск через Windows:
``` bash
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
py run.py
```

## Запуск через Linux:
``` bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Бот запущен, можете писать в телеграмме в сообщения своему боту, в логах будет информация о событиях.
