from unit17.example.app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from unit17.example.app.models import *

class Product(Base):
    __tablename__ = "products"  # наименование таблицы данных
    __table_args__ = {"keep_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)  # имя продукта
    slug = Column(String, unique=True, index=True)
    description = Column(String)  # описание продукта
    price = Column(Integer)  # цена
    img_url = Column(String)  # путь к изображению продукта
    stock = Column(Integer)  # количество
    category_id = Column(Integer, ForeignKey("categories.id"))
    rating = Column(Float)  # рейтинг
    is_active = Column(Boolean, default=True)

    category = relationship("Category", back_populates="products")

from sqlalchemy.schema import CreateTable
print(CreateTable(Product.__table__))
