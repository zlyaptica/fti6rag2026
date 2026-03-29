# ПЕТРГУ ФТИ 6 КУРС | РАЗРАБОТКА RAG

## Запуск

### Подготовка переменных окружения
На основе .env создайте файл .env.local и поместите заполните его по примеру.
Для регистрации URL вебхука в Телеграмме необходимо выполнить GET запрос:
```
https://api.telegram.org/bot<TOKEN>/setWebhook?url=path

# Пример запроса на данных из .env:
https://api.telegram.org/bottoken/setWebhook?url=https://example.com/telegram
```

### Команда запуска
Windows
``` bash
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
py run.py
```

Linux
``` bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```
