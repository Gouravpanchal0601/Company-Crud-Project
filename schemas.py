from pydantic import BaseModel
from typing import Optional

class EmployeeBase(BaseModel):
    name:str
    age:int
    department:str

class EmployeeResponse(EmployeeBase):
    id: int
    class Config:
        orm_mode = True

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id:int
    owner_id:Optional[int]=None

    class config:
        orm_mode=True

class UserCreate(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str