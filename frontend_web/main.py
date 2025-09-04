from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

BACKEND_URL = "http://127.0.0.1:8000"  # URL de ton backend

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # Récupère tous les restaurants depuis ton backend
    resp = requests.get(f"{BACKEND_URL}/restaurants")
    restaurants = resp.json()
    return templates.TemplateResponse("index.html", {"request": request, "restaurants": restaurants})

@app.get("/restaurant/{id}", response_class=HTMLResponse)
def restaurant_detail(request: Request, id: int):
    resp = requests.get(f"{BACKEND_URL}/restaurants/{id}")
    restaurant = resp.json()
    return templates.TemplateResponse("restaurant_detail.html", {"request": request, "restaurant": restaurant})
