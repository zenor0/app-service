from pydantic import BaseModel
from typing import Optional

class UpdateUserForm(BaseModel):
    username: Optional[str]
    email: Optional[str]
    nickname: Optional[str]
    password: Optional[str]
    realname: Optional[str]
    id_number: Optional[str]
    blocked: Optional[bool]
    