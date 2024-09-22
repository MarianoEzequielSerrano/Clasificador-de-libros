from flask import Flask, request, Response, jsonify, redirect, url_for
import joblib  # Para cargar el modelo entrenado
import json
import database as dbase

db = dbase.dbConnection() # Genera una instancia de conexion a la base de datos

app = Flask(__name__)

# Cargar el modelo entrenado
modelo_recomendacion = joblib.load('gbm_model.pkl')  

@app.route('/')
def index():
    return "¡Hola, esta es la página principal!"

@app.route('/save-data', methods=['POST'])
def persistir_data():
    collect = db['books']
    try:
        data = request.get_json()
        name = data.get('Name', None)
        author = data.get('Author', None)
        userRating = data.get('User Rating', None)
        reviews = data.get('Reviews', None)
        price = data.get('Price', None)
        year = data.get('Year', None)
    
        if name and author and userRating and reviews and price and year:
           usuario_data = [userRating, reviews, price, year]
           genre_fiction = recomendar_libros(usuario_data)
           genre_non_fiction = 1
           if genre_fiction == 1:
               genre_non_fiction = 0      
           response = collect.insert_one({
               'Name': name,
               'Author' : author,
               'User Rating' : userRating,
               'Reviews' : reviews,
               'Price' : price,
               'Year' : year,
               'Genre Fiction' : genre_fiction,
               'Genre non Fiction' : genre_non_fiction
           })
           result = {
               'id' : str(response.inserted_id),
               'done' : True
           }
           return result
        else:
            return notFound() 
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    
def recomendar_libros(usuario_data):
    try:
        recomendacion = modelo_recomendacion.predict([usuario_data])[0]
        return int(recomendacion)

    except Exception as e:
        print(f"Error: {e}")

@app.errorhandler(404)
def notFound(error=None):
    message ={
        'message': 'No encontrado ' + request.url,
        'status' : '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response
    
if __name__ == '__main__':
    app.run(debug=True)