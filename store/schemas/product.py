from pydantic import Field

from store.schemas.base import BaseSchemaMixin


class ProductIn(BaseSchemaMixin):
    name: str = Field(description="Product name", example="Iphone 17 Pro Max")
    quantity: int = Field(description="Product quantity", example=10)
    price: float = Field(description="Product price", example=999.99)
    status: bool = Field(description="Product status", example=True)
