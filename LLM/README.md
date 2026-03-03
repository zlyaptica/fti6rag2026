<div align="center">
  <h1 align="center">Запуск программы для работы с LLM</h1>
</div>
<br>

## Установка
> [!Note]
> Команды для установки и последующих манипуляций будут представлены для ОС Windows.

### 1. Клонирование репозитория
```shell
git clone https://github.com/vasilievi/fti6rag2026
cd fti6rag2026\LLM
```

### 2. Устанавление зависимостей
```shell
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Установка пакета PyTorch
Перед выполнением следующих действий желательно установить [CUDA](https://developer.nvidia.com/cuda/toolkit), а также библиотку torch под версию CUDA.<br>
Пример установки torch для CUDA 13.0:
```shell
pip install --pre torch --index-url https://download.pytorch.org/whl/nightly/cu130
```
Без использования CUDA LLM будет взаимодействовать только с CPU, что повлияет на время исполнения программы.<br>
Установка torch без поддержки CUDA:
```shell
pip install torch
```

### 4. Устанавка необходимых компонентов
Для последующего запуска нужно скачать LLM [Qwen3](https://huggingface.co/Qwen/Qwen3-0.6B). Модель должна находиться в одной папке с запускаемым далее py-файлом. Директория с моделью должна иметь название "Qwen3-0.6B". 

### 5. Запуск программы
```shell
py run.py
```