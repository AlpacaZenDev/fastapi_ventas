from fastapi import FastAPI
from fastapi import Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from data_db import ventas


# Crea una instancia de FastAPI
app = FastAPI()
app.title = "APLICACIÓN DE VENTAS"
app.version = "2025.1.0"

# Punto de entrada o endpoint
@app.get("/", tags=['Bienvenida'])
def mensaje():
    return HTMLResponse("<h2>Hola, bienvenido</h2>")

@app.get('/ventas', tags=['Ventas'])
def obtener_ventas():
    return ventas

# Parámetro de ruta
@app.get('/ventas/{id}', tags=['Ventas'])
def obtener_venta_por_id(id: int):
    for item in ventas:
        if item['id'] == id:
            return item
    return []

# Parámetro de consulta
@app.get('/ventas/', tags=['Ventas'])
def obtener_venta_por_tienda(tienda: str):
    consulta = [item for item in ventas if item['tienda'] == tienda]        
    return consulta

# Otros métodos HTTP:
# Método POST
@app.post('/ventas', tags=['Ventas'])
def crear_una_venta(id: int = Body(), fecha: str = Body(), tienda: str = Body(), importe: float = Body()):
    ventas.append(
        {
            "id": id,
            "fecha": fecha,
            "importe": importe,
            "tienda": tienda
        }
    )
    return ventas

# Método PUT
@app.put('/ventas/{id}', tags=['Ventas'])
def actualizar_un_item(id: int, fecha: str = Body(), tienda: str = Body(), importe: float = Body()):
    for item in ventas:
        if item['id'] == id:
            item['fecha'] = fecha
            item['tienda'] = tienda
            item['importe'] = importe
    return ventas

# Método DELETE
@app.delete('/ventas/{id}', tags=['Ventas'])
def borrar_una_venta(id: int):
    for item in ventas:
        if item['id'] == id:
            ventas.remove(item)
    return ventas

