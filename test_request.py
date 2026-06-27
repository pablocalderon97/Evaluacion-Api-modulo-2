import requests
from datetime import datetime, date

url = "http://127.0.0.1:8000/tasks/"

datos_tarea = {
    "titulo": "Compra Supermercado",
    "contenido": "Patatas,fruta,filetes,huevos",
    "deadline":date(2025,3,2),
    "creada": date(2026,3,1).isoformat()
}

def exec_post_request(tarea_data, url, expected_code):

    response = requests.post(url, json=tarea_data, timeout=5)

    print(f"Código de respuesta: {response.status_code}")
    print(f"Respuesta: {response.json()}")
    assert response.status_code == expected_code
   
    if response.status_code == 200:
        print(f"Respuesta: {response.json()}")
    elif response.status_code != 500:
        print(f"Respuesta: {response.json()}")
    else:
        print("Internal Server Error")

def tarea_incorrecta():

    datos_tarea ={

        "titulo": "aaa", # Error pocos caracteres
        "contenido": "bbb",
        "deadline":date(2025,3,2),
        "creada": date(2026,3,1).isoformat()
    }

    response = requests.post(url, json=datos_tarea, timeout=5)
    print(f"Código: {response.status_code}")
    print(f"Respuesta: {response.json()}")
    assert response.status_code == 422, f"Esperado 422, obtenido {response.status_code}"

def id_incorrecta():

    response = requests.get(f"{url}/9999", timeout=5)
    print(f"Código: {response.status_code}")
    print(f"Respuesta: {response.json()}")
    assert response.status_code == 404, f"Esperado 404, obtenido {response.status_code}"

def tarea_fecha_incorrecta():

    datos_tarea = {
        
        "titulo": "Tarea futura",
        "contenido": "bbb",
        "creada": date(2030, 1, 1).isoformat()
    }
    response = requests.post(f"{url}/tasks/", json=datos_tarea, timeout=5)
    print(f"Código: {response.status_code}")
    print(f"Respuesta: {response.json()}")
    assert response.status_code == 400, f"Esperado 400, obtenido {response.status_code}"   


exec_post_request(datos_tarea,url,200)
tarea_incorrecta()
id_incorrecta()
tarea_fecha_incorrecta()