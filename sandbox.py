# import asyncio
# from motor.motor_asyncio import AsyncIOMotorClient
# from pymongo import MongoClient

# def create_one(client, title: str, author: str, year_of_release: int, description: str):
#     test_collection = client['books_base']['books_collection']
#     test_dict = {
#         "title": title,
#         "author": author,
#         "year_of_release": year_of_release,
#         "description": description
#     }
#     test_collection.insert_one(test_dict)

# async def list_all(client):
#     test_collection = client['books_base']['books_collection']
#     cursor = test_collection.find({})
#     async for document in cursor:
#         print(document)

# def clear_collection(client):
#     test_collection = client['books_base']['books_collection']
#     result = test_collection.delete_many({})
#     print(f"Deleted {result.deleted_count}")

# def create_index(client: MongoClient):
#     test_collection = client['books_base']['books_collection']
#     test_collection.create_index("title", unique = True)

# def list_indexes(client):
#     test_collection = client['books_base']['books_collection']
#     result = test_collection.list_indexes()
#     for index in result:
#         print(index)

# def main():
#     client = MongoClient(serverSelectionTimeoutMS=5000)
#     # await list_all(client)
#     # clear_collection(client)
#     # create_one(client, "Pan Tadeusz", "Adam Mickiewicz", 1990, "")
#     # create_one(client, "Ludzie Bezdomni", "Stefan Żeromski", 1991, "")
#     # create_one(client, "Wesele", "Stanisław Wyspiański", 1992, "")
#     # create_one(client, "Chłopi", "Władysław Reymont", 1993, "")
#     # await list_all(client)
#     # list_indexes(client)
#     # create_index(client)
#     # client.close()

# # asyncio.run(main())


# main()