from flask import Flask, request, jsonify
import joblib  # Para cargar el modelo entrenado
import pandas as pd

app = Flask(__name__)

# Cargar el modelo entrenado
modelo_recomendacion = joblib.load('gbm_model.pkl')  

@app.route('/')
def index():
    return "¡Hola, esta es la página principal!"

@app.route('/recomendar-libros', methods=['POST'])
def recomendar_libros():
    try:
        data = request.get_json()

        # Obtener los datos del usuario de la solicitud
        usuario_data = [data['User Rating'], data['Reviews'], data['Price'], data['Year']]

        # Realizar la predicción con el modelo de recomendación
        recomendacion = modelo_recomendacion.predict([usuario_data])[0]

        # Convertir el resultado a un tipo serializable
        recomendacion_serializable = int(recomendacion)

        return jsonify({'libro_recomendado': recomendacion_serializable})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500  # Devuelve el error 500 con detalles

if __name__ == '__main__':
    app.run(debug=True)

#Definicion de la ruta para manejar solicitudes GET para obtener la clasificacion del libro por su ID

def obtener_clasificacion_libro(libro_index):
    #Cargar el csv
    df = pd.read_csv('books_df_final.csv')

    #Verificar si el indice está dentro del rango de indice del DataFrame
    if libro_index < len(df):
        #Obtener la fila que corresponde al indice dado
        libro = df.iloc[libro_index]

        #Obtener la clasificacion del libro
        clasificacion_fiction = libro['Genre_Fiction']
        clasificacion_non_fiction = libro['Genre_Non Fiction']

    #Verificar la clasificacion del libro y devolverla como resultado
        if clasificacion_fiction == 1:
            return 'Fiction'
        elif clasificacion_non_fiction == 0:
            return 'Non Fiction'
        else:
            return 'Clasificacion Desconocida'
    else:
        return 'Indice fuera de rango'
    
@app.route('/libro/<int:libro_id>', methods=['GET'])    
def obtener_clasificacion(libro_id):
    try:
        # Llamo a la funcion para obtener la clasificacion del libro
        clasificacion = obtener_clasificacion_libro(libro_id)

        #Devolver la clasificacion del libro como parte de la respuesta
        return jsonify({'ID': libro_id, 'Clasificacion': clasificacion})
    
    except Exception as e:
        return jsonify ({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)