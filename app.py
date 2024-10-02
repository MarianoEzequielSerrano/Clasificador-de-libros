import json
from flask import Flask, request, jsonify, render_template #type: ignore
import joblib  # Para cargar el modelo entrenado

app = Flask(__name__)

# Cargar el modelo entrenado
modelo_recomendacion = joblib.load('gbm_model.pkl')  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recomendar-libros', methods=['POST'])
def recomendar_libros():
    try:
        data = request.form

        # Obtener los datos del usuario de la solicitud

        usuario_data = [float(data['rating']), float(data['review']), float(data['price']), int(data['year'])]

        # Realizar la predicción con el modelo de recomendación
        recomendacion = modelo_recomendacion.predict([usuario_data])[0]

        # Convertir el resultado a un tipo serializable
        recomendacion_serializable = int(recomendacion) 

        return render_template ('new.html', recomendado=recomendacion_serializable, data=data)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500  # Devuelve el error 500 con detalles

@app.route('/Recomendacion')
def predict():
    return render_template('new.html')

if __name__ == '__main__':
    app.run(debug=True)
