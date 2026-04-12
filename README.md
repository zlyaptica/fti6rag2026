# ПЕТРГУ ФТИ 6 КУРС | РАЗРАБОТКА RAG

Используемая LLM - Qwen/Qwen3-0.6B.

## Запуск

### Подготовка переменных окружения
На основе .env создайте файл .env.local и поместите заполните его по примеру.
Для регистрации URL вебхука (в случае его использования) в Телеграмме необходимо выполнить GET запрос:
```
https://api.telegram.org/bot<TOKEN>/setWebhook?url=path

# Пример запроса на данных из .env:
https://api.telegram.org/bottoken/setWebhook?url=https://example.com/telegram
```

### Установка виртуальног окружения
Windows
``` bash
py -3 -m venv .venv
.venv\Scripts\activate
```

Linux
``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### Установка torch
Linux torch + cpu
``` bash
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

Linux torch + gpu
``` bash
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu126
```

Windows torch + cpu
``` bash
pip3 install torch torchvision
```

Windows torch + gpu
``` bash
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu126
```

### Команда запуска без вебхука:
Windows
``` bash
pip install -r requirements.txt
py run.py
```

Linux
``` bash
pip install -r requirements.txt
python run.py
```

### Команда запуска с вебхуком:
Windows
``` bash
pip install -r requirements.txt
py run.py --use-webhook
```

Linux
``` bash
pip install -r requirements.txt
python run.py --use-webhook
```
