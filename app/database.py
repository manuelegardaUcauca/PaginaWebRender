from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import requests

# Configuración de base de datos
DATABASE_URL = "sqlite:///./visitas.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Visita(Base):
    __tablename__ = "visitas"
    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String)
    pais = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

# Inicializar base de datos
init_db()

# Inicialización de FastAPI
app = FastAPI()

# Montar archivos estáticos y templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Obtener IP y país de visitante
def get_visitor_info(request: Request):
    ip = request.client.host
    try:
        # Utiliza ipapi.co para geolocalización rápida
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        data = response.json()
        country = data.get("country_name", "Desconocido")
    except:
        country = "Desconocido"
    return ip, country

def registrar_visita(request: Request):
    db = SessionLocal()
    ip, pais = get_visitor_info(request)
    visita = Visita(ip=ip, pais=pais)
    db.add(visita)
    db.commit()
    db.close()

# Rutas de la página (todas registran visita)
@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    registrar_visita(request)
    return templates.TemplateResponse("index.html", {"request": request, "titulo": "Inicio"})

@app.get("/objetivos", response_class=HTMLResponse)
async def objetivos(request: Request):
    registrar_visita(request)
    return templates.TemplateResponse("objetivos.html", {"request": request, "titulo": "Objetivos"})

@app.get("/metodologia", response_class=HTMLResponse)
async def metodologia(request: Request):
    registrar_visita(request)
    return templates.TemplateResponse("metodologia.html", {"request": request, "titulo": "Metodología"})

@app.get("/contribuciones", response_class=HTMLResponse)
async def contribuciones(request: Request):
    registrar_visita(request)
    return templates.TemplateResponse("contribuciones.html", {"request": request, "titulo": "Contribuciones"})

@app.get("/resultados", response_class=HTMLResponse)
async def resultados(request: Request):
    registrar_visita(request)
    return templates.TemplateResponse("resultados.html", {"request": request, "titulo": "Resultados"})

@app.get("/contacto", response_class=HTMLResponse)
async def contacto(request: Request):
    registrar_visita(request)
    return templates.TemplateResponse("contacto.html", {"request": request, "titulo": "Contacto"})
