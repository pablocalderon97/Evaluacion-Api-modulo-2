import requests
from datetime import datetime, date

url = "https://127.0.0.1:8000/tasks/"

def exec_post_request(user_data, url, expected_code):

    response = requests.post(url, json=user_data, timeout=5)

    print(f"Código de respuesta: {response.status_code}")
    print(f"Respuesta: {response.json()}")
    assert response.status_code == expected_code
   
    if response.status_code == 200:
        print(f"Respuesta: {response.json()}")
    elif response.status_code != 500:
        print(f"Respuesta: {response.json()}")
    else:
        print("Internal Server Error")

datos_tarea = {
    "titulo": "Compra Supermercado",
    "Contenido": "Patatas,fruta,filetes,huevos",
    "Creada": date(2026,3,1).isoformat()
}

exec_post_request(datos_tarea,url,200)