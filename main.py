from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_config import generar_token, validar_token
from config.db import sesion, motor, base
# from data_db import ventas
from models.ventas import Ventas as VentasModels


# Crea una instancia de FastAPI
app = FastAPI()
app.title = "APLICACIÓN DE VENTAS"
app.version = "2025.1.0"
base.metadata.create_all(bind=motor)

class UsuarioModel(BaseModel):
    email: str
    password: str

# Creación del modelo (Para usar BaseModel y Optional)
class Ventas(BaseModel):
    # id: int = Field(ge=0, le=21)
    id: Optional[int]=None
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

# class Ventas(BaseModel):
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

@app.get('/ventas', tags=['Ventas'], response_model=List[Ventas], status_code=200, dependencies=[Depends(Portador())])
def obtener_ventas() -> List[Ventas]:
    db = sesion()
    resultado = db.query(VentasModels).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(resultado))

# Parámetro de ruta
@app.get('/ventas/{id}', tags=['Ventas'], response_model= Ventas)
def obtener_venta_por_id(id: int = Path(ge=1, le=1000)) -> Ventas:
    db = sesion()
    resultado = db.query(VentasModels).filter(VentasModels.id == id).first()
    if resultado:
        return JSONResponse(status_code=200, content=jsonable_encoder(resultado))
    return JSONResponse(status_code=404, content={'Mensaje':'Id no encontrado'})

# Parámetro de consulta
@app.get('/ventas/', tags=['Ventas'], response_model=List[Ventas])
def obtener_venta_por_tienda(tienda: str = Query(min_length=4, max_length=20)) -> List[Ventas]:
    db = sesion()
    resultado = db.query(VentasModels).filter(VentasModels.tienda == tienda).all()
    if resultado:
        return JSONResponse(content= jsonable_encoder(resultado))
    return JSONResponse(status_code=404, content={'Mensaje': 'Tienda no encontrada'})
        

# Otros métodos HTTP:
# Método POST
@app.post('/ventas', tags=['Ventas'], response_model=dict)
def crear_una_venta(venta: Ventas) -> dict:
    db = sesion()
    nueva_venta = VentasModels(**venta.model_dump())
    db.add(nueva_venta)
    db.commit()
    return JSONResponse(content={'Mensaje':'Venta registrada'})

# Método PUT
@app.put('/ventas/{id}', tags=['Ventas'], response_model=dict)
def actualizar_un_item(id: int, venta: Ventas) -> dict:
    db = sesion()
    resultado = db.query(VentasModels).filter(VentasModels.id == id).first()
    if resultado:
        resultado.fecha = venta.fecha
        resultado.tienda = venta.tienda
        resultado.importe= venta.importe
        db.commit()
        return JSONResponse(status_code=200, content={'Mensaje': 'Venta actualizada'})
    return JSONResponse(status_code=404, content={'Mensaje': 'No se actualizó'} )
        

# Método DELETE
@app.delete('/ventas/{id}', tags=['Ventas'], response_model=dict)
def borrar_una_venta(id: int) -> dict:
    db = sesion()
    resultado = db.query(VentasModels).filter(VentasModels.id == id).first()
    if resultado:
        db.delete(resultado)
        db.commit()
        return JSONResponse(status_code=200, content={'Mensaje':'Item eliminado satisfactoriamente'})
    return JSONResponse(status_code=404, content={'Mensaje': 'Id no encontrado'})


# Creación de la ruta para el login
@app.post('/login', tags=['Autenticación'])
def login(user: UsuarioModel):
    if user.email == 'alpacazen@hotmail.com' and user.password == '1234':
        token: str=generar_token(user.model_dump())
        return JSONResponse(content=token, status_code=200)
    return JSONResponse(content={"detail": "Credenciales inválidas"}, status_code=401)

    
    
    