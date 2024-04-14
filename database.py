from pymongo import MongoClient
import certifi

MONGO_URI = 'mongodb+srv://mariano:1234@clasificadordelibrosdb.lzeohrp.mongodb.net/?retryWrites=true&w=majority&appName=ClasificadorDeLibrosDB'
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["Cloud"]
    except ConnectionError: 
        print('Error de conexión con la Base de Datos')
    return db