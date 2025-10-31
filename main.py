from fastapi import FastAPI,Depends
from database import engine
import models
from routers import products,categorey,auth

app = FastAPI()

models.Base.metadata.create_all(bind = engine)
app.include_router(products.router)
app.include_router(categorey.router)
app.include_router(auth.router)

