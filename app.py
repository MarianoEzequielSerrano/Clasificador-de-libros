from flask import Flask, request, jsonify, render_template
import joblib  # Para cargar el modelo entrenado
import database as dbase
import csv

db = dbase.dbConnection()  # Genera una instancia de conexión a la base de datos

app = Flask(__name__)

# Cargar el modelo entrenado
modelo_recomendacion = joblib.load('gbm_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recomendar-libros', methods=['POST'])
def recomendar_libros():
    collect = db['Libros'] #Cambiar por el nombre de la colección de MongoDB
    try:
        # Obtener datos del formulario
        name = request.form.get('title')
        author = request.form.get('author')
        userRating = float(request.form.get('rating'))
        reviews = int(request.form.get('review'))
        price = float(request.form.get('price'))
        year = int(request.form.get('year'))

        if name and author and userRating is not None and reviews is not None and price is not None and year is not None:
            usuario_data = [userRating, reviews, price, year]
            genre_fiction = modelo_recomendacion.predict([usuario_data])[0]
            genre_non_fiction = 0 if genre_fiction == 1 else 1

            # Insertar en la base de datos
            response = collect.insert_one({
                'title': name,
                'author': author,
                'rating': userRating,
                'review': reviews,
                'price': price,
                'year': year,
                'Genre Fiction': int(genre_fiction),
                'Genre non Fiction': int(genre_non_fiction)
            })

            # Guardar los datos en el archivo CSV
            with open('bestsellers with categories.csv', mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([name, author, userRating, reviews, price, year, 'Fiction' if genre_fiction == 1 else 'Non Fiction'])

            # Preparar los datos para la plantilla
            result_data = {
                'author': author,
                'title': name,
                'rating': userRating,
                'review': reviews,
                'price': price,
                'year': year,
                'recomendado': 'Ficción' if genre_fiction == 1 else 'No ficción'
            }

            return render_template('new.html', data=result_data)
        else:
            return jsonify({'error': 'Datos incompletos'}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
