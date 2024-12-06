from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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

