from pydantic import BaseModel, ConfigDict, UUID4


class ShopIn(BaseModel):
    name: str
    value: int
    quiz_id: int

class Shop(ShopIn):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")