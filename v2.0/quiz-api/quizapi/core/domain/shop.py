"""Module containing shop-related domain models"""

from pydantic import BaseModel, ConfigDict, UUID4

class ShopIn(BaseModel):
    """Model representing shop's DTO attributes."""
    name: str
    value: int
    quiz_id: int

class Shop(ShopIn):
    """Model representing shop attributes in the database."""
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")