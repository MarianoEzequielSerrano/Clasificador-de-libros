from flask import Flask, request, jsonify
import joblib  # Para cargar el modelo entrenado
import json

app = Flask(__name__)

# Cargar el modelo entrenado
modelo_recomendacion = joblib.load('gbm_model.pkl')  

@app.route('/')
def index():
    return "¡Hola, esta es la página principal!"

@app.route('/save-data', methods=['POST'])
def persistir_data():
    try:
        data = request.get_json()
        usuario_data = [data['User Rating'], data['Reviews'], data['Price'], data['Year']]
        recomendacion = recomendar_libros(usuario_data)
        return "Data guardada exitosamente: " + data['Name'] + "," + data['Author'] + "," + str(data['User Rating']) + "," + str(data['Reviews']) + "," + str(data['Price']) + "," + str(data['Year']) + "," + str(recomendacion) #Mensaje de guardado exitoso + row formateada para insertar en archivo csv
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    
def recomendar_libros(usuario_data):
    try:
        recomendacion = modelo_recomendacion.predict([usuario_data])[0]
        return int(recomendacion)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)