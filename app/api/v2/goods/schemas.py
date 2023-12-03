from pydantic import BaseModel
from typing import Optional

# interface FormData {
#   uid?: string;
#   good_id?: string;
#   seller_id?: string;
#   game?: string;
#   title?: string;
#   detail?: string;
#   state?: string;
#   publish_time?: string;
#   price?: string;
# }

class UpdateGoodForm(BaseModel):
    seller_id: Optional[int]
    state: Optional[str]
    game: Optional[str]
    title: Optional[str]
    detail: Optional[str]
    price: Optional[float]
    publish_time: Optional[str]


class CreateGoodForm(BaseModel):
    seller_id: int
    state: str
    game: str
    title: str
    detail: str
    price: float
    publish_time: str