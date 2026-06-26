import requests
from datetime import datetime, date



url = "https://127.0.0.1:8000/tasks/"

datos_tarea = {
    "titulo": "Compra Supermercado",
    "Contenido": "Patatas,fruta,filetes,huevos",
    "Creada": date(2026,3,1).isoformat()
}

respuesta = requests.post(url,datos_tarea)
print(f"Codigo de respuesta: {respuesta.status_code}")
print(f"Respuesta:{respuesta.json}")