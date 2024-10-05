from  pymongo import MongoClient
import certifi

#Cambiar dirección de conexión
MONGO_URI = 'mongodb+srv://agus75:agus1234@cluster0.tk9lqny.mongodb.net/ClasificadorDeLibrosDB?retryWrites=true&w=majority' 
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["ClasificadorDeLibrosDB"]
    except ConnectionError: 
        print('Error de conexión con la Base de Datos')
    return db