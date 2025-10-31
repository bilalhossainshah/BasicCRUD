from sqlalchemy import String,Column,Integer,ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


class Products(Base):
    __tablename__ = "Products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    description = Column(String)
    cat_id = Column(Integer, ForeignKey("Categorey.id"))
    
    categories = relationship("Categorey",back_populates="product")


class Categorey(Base):
    __tablename__ = "Categorey"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)


    product = relationship("Products", back_populates="categories")