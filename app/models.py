from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float
    brand: str
    rating: float
    description: str


class ProductRequirements(BaseModel):
    category: Optional[str] = None
    max_price: Optional[float] = None
    min_price: Optional[float] = None
    min_rating: Optional[float] = None
    brand: Optional[str] = None
    search_query: Optional[str] = None


class ProductSearchResponse(BaseModel):
    products: list[Product]
    total: int


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    product: Optional[Product] = None