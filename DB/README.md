# DB
## Общие сведенья
файл config.py содержит реализацию развертывания векторной базы данных chromedb. Для ее установки используется код, приведенный ниже:
```
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
файл run.py запускает тестирование функционала для работы с базой данных

## Основные функции
### init
Функция init создает клиента и формирует коллекцию. По умолчанию создание происходит в директории "./chroma_db". Коллекция по умолчанию называется "my_collection"

### select_query
Функция select_query делает запрос к коллекции, принимая текст для поиска, и возвращает наиболее близкую запись. (не реализовано, но к сведению) Существует возможность настроить фильтры по метаданным, вывод метаданных, количество выводимых записей

### insert_query


### delete_query


## Интересные ссылки
https://github.com/FSerg/mcp-1c-v1?ysclid=mm2gat7hhi942297636
https://infostart.ru/1c/tools/2407674/?ysclid=mm2gddwt7v971145245

https://github.com/1C-Migration-Lab/1c-analyzer-wiki-rag
https://habr.com/ru/articles/896314/

https://github.com/hasura/business-data-benchmark
https://github.com/fdabench/FDAbench
https://github.com/ServiceNow/drbench
https://github.com/SalesforceAIResearch/HERB
https://github.com/kapilsprinklr/cxmarena
https://huggingface.co/datasets/ibm-research/watsonxDocsQA
https://huggingface.co/datasets/ibm-research/WatsonxDocsQARetrieval