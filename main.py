from fastapi import FastAPI
from database import engine
import models
from routers import products,categorey

app = FastAPI()

models.Base.metadata.create_all(bind = engine)
app.include_router(products.router)
app.include_router(categorey.router)

