import requests

url = 'http://127.0.0.1:5000/recomendar-libros'

# Datos del usuario para la recomendación
usuario_data = {
    'Name': "Philosopher's Stone",
    'Author': 'J. K. Rowling',
    'User Rating': 4.8,
    'Reviews': 15000,
    'Price': 20,
    'Year': 2015
}

# Realizar la solicitud POST
response = requests.post(url, json=usuario_data)

# Verificar si la respuesta es exitosa (código 200) y si contiene datos JSON
if response.status_code == 200 and response.headers['content-type'] == 'application/json':
    print(response.json())
else:
    print(f"Error en la solicitud. Código de estado: {response.status_code}")
