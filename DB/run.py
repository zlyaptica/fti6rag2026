from config import init, select_query, insert_query, delete_query

init()

insert_query("test", {"date": '09.12.2025'})
print(select_query("test"))
