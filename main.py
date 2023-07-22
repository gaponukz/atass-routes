from fastapi import FastAPI
from src.db.json_db import RouteRepository
from src.usecases.view_routes import ViewRoutesUseCase
from src.handlers.view_routes import ViewRoutesHandler

db = RouteRepository("routes.json")
view_usecase = ViewRoutesUseCase(db)
view_handler = ViewRoutesHandler(view_usecase)

app = FastAPI()
app.include_router(view_handler.router)