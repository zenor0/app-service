from pydantic import BaseModel

class BaseResponse(BaseModel):
    code: int = 200
    message: str = 'success'
    data: dict = {}


