from flask import Flask, request, jsonify
import joblib  # Para cargar el modelo entrenado

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
