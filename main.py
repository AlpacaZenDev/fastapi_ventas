from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from data_db import ventas
from jwt_config import generar_token, validar_token


# Crea una instancia de FastAPI
app = FastAPI()
app.title = "APLICACIÓN DE VENTAS"
app.version = "2025.1.0"

class UsuarioModel(BaseModel):
    email: str
    password: str

# Creación del modelo (Para usar BaseModel y Optional)
class VentasModel(BaseModel):
    id: int = Field(ge=0, le=21)
    fecha: str
    importe: float
    tienda: str = Field(min_length=4, max_length=10)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "fecha": "01/01/2001",
                "importe": 1234.56,
                "tienda": "Tienda9"
            }
        }
    }

# class VentasModel(BaseModel):
#     id: Optional[int] = Field(None, title="Id", description="Identificador único de la venta")
#     fecha: str = Field(..., title="Fecha", description="Fecha de la venta (YYYY-MM-DD)")
#     importe: float = Field(..., title="Importe", description="Monto total de la venta")
#     tienda: str = Field(..., title="Tienda", description="Nombre de la tienda")

class Portador(HTTPBearer):
    async def __call__(self, request: Request):
        authorization = await super(). __call__(request)
        data = validar_token(authorization.credentials)
        if data['email'] != 'alpacazen@hotmail.com':
            raise HTTPException(detail='No autorizado', status_code=403)
# Punto de entrada o endpoint
@app.get("/", tags=['Bienvenida'])
def mensaje():
    return HTMLResponse("<h2>Hola, bienvenido</h2>")

@app.get('/ventas', tags=['Ventas'], response_model=List[VentasModel], status_code=200, dependencies=[Depends(Portador())])
def obtener_ventas() -> List[VentasModel]:
    return JSONResponse(content=ventas)

# Parámetro de ruta
@app.get('/ventas/{id}', tags=['Ventas'], response_model= VentasModel)
def obtener_venta_por_id(id: int = Path(ge=1, le=1000)) -> VentasModel:
    for item in ventas:
        if item['id'] == id:
            return JSONResponse(content=item)
    return JSONResponse(content=[])

# Parámetro de consulta
@app.get('/ventas/', tags=['Ventas'], response_model=List[VentasModel])
def obtener_venta_por_tienda(tienda: str = Query(min_length=4, max_length=20)) -> List[VentasModel]:
    consulta = [item for item in ventas if item['tienda'] == tienda]        
    return JSONResponse(content=consulta)

# Otros métodos HTTP:
# Método POST
@app.post('/ventas', tags=['Ventas'], response_model=dict)
# def crear_una_venta(id: int = Body(), fecha: str = Body(), tienda: str = Body(), importe: float = Body()):
def crear_una_venta(venta: VentasModel) -> dict:
    ventas.append(
        dict(venta)
    )
    return JSONResponse(content={'Mensaje':'Venta registrada'})

# Método PUT
@app.put('/ventas/{id}', tags=['Ventas'], response_model=dict)
def actualizar_un_item(id: int, venta: VentasModel) -> dict:
    for item in ventas:
        if item['id'] == id:
            item['fecha'] = venta.fecha
            item['tienda'] = venta.tienda
            item['importe'] = venta.importe
    return JSONResponse(content={'Mensaje': 'Venta actualizada'})

# Método DELETE
@app.delete('/ventas/{id}', tags=['Ventas'], response_model=dict)
def borrar_una_venta(id: int) -> dict:
    for item in ventas:
        if item['id'] == id:
            ventas.remove(item)
    return JSONResponse(content={'Mensaje': 'Venta eliminada'})


# Creación de la ruta para el login
@app.post('/login', tags=['Autenticación'])
def login(user: UsuarioModel):
    if user.email == 'alpacazen@hotmail.com' and user.password == '1234':
        token: str=generar_token(user.model_dump())
        return JSONResponse(content=token, status_code=200)
    return JSONResponse(content={"detail": "Credenciales inválidas"}, status_code=401)

    
    
    