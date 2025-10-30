from fastapi import APIRouter,Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import HTTPException
import models,database

class ProductBase(BaseModel):
    name:str
    price:float
    description:str
    cat_id:float

router = APIRouter(prefix="/products",tags=["Products"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db

    finally:
        db.close()

@router.post("/products")
def create_product(product: ProductBase,db:Session = Depends(get_db)):
    categorey = db.query(models.Categorey).filter(models.Categorey.id == product.cat_id ).first()
    if not categorey:
        raise HTTPException(status_code=400,detail="Categorey Not Found")
    
    db_products = models.Products(
        name = product.name,
        price = product.price,
        description = product.description,
        cat_id = product.cat_id
    )

    db.add(db_products)
    db.commit()
    db.refresh(db_products)
    return db_products
    return {'message':"Items created successfully",'product':product}

@router.get("/products")
def get_products(db:Session = Depends(get_db)):
    products = db.query(models.Products).all()
    result = [] 
    for p in products:
        result.append({
            "id" : p.id,
            "price" : p.price,
            "description" : p.description,
            "ctegorey" : p.categorey.name if p.categorey else None
    })
    return result


@router.put("/products:{/product_id}")
def update_products(products_id: int, update_product: ProductBase, db:Session = Depends(get_db)):
    db_products = db.query(models.Products).filter(models.Products.id == products_id).first()
    if not db_products:
        raise HTTPException(status_code=404,detail="Product not found")
    
    categorey = db.query(models.Categorey).filter(models.Categorey.id == product.cat_id).first()
    if not categorey:
        raise HTTPException(status_code=404,detail="There is no Category ")
    
    db_products.name = update_product.name
    db_products.price = update_product.price
    db_products.description = update_product.description
    db_products.id = update_product.id
    
    db.commit()
    db.refresh(db_products)

    return{"message":"Product updated Successfully",'product':db_products}


@router.delete("/products:/{product_id}")
def delete_product(product_id:int , db:Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404,detail="Product not found")
    db.delete(product)
    db.commit()
    return{"message":f"Successfully deleted {product_id}"}