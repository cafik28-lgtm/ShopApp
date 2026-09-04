from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.utils.admin import create_default_admin

from app.database import Base, SessionLocal, engine
# Даш, импорты роутеров сюда / харашо
from app.routers.categories import router as categories_router
from app.routers.users import router as users_router

Base.metadata.create_all(
    bind=engine
)

db = SessionLocal()

try:
    create_default_admin(db)
finally:
    db.close()

app = FastAPI(
    title='Shop Online',
    version='1.0.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# и тут роутеры подключаем
app.include_router(categories_router)
app.include_router(users_router)

# для аватарок
app.mount("/avatars", StaticFiles(directory="avatars"), name="avatars")

@app.get('/')
def root():
    return {
        'message': '/docs to open Swagger UI'
    }

@app.get('/health')
def health():
    return {
        'status': 'OK'
    }
