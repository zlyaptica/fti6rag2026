import chromadb

client = None
collection = None

def init(dir: str = "./chroma_db", collection_name:str = "my_collection"):
    global client, collection
    try:
        client = chromadb.Client(chromadb.config.Settings(
            persist_directory=dir,
            anonymized_telemetry=False
        ))

        try:
            collection = client.get_collection(collection_name)
        except:
            collection = client.create_collection(collection_name)

        print("init successfully")
    except:
        print("init fail")

def select_query(text: str) -> str:
    #Поиск в БД
    print("Ищу")

def insert_query(text: str):
    #Вставить в бд
    print("Вставляю")

def delete_query(text: str):
    #Удалить из бд
    print("Удаляю")