from pydantic import BaseModel
import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime                   

    class Config:
        orm_mode = True


class FileBase(BaseModel):
    filename: str

class UserFiles(FileBase):
    id: int
    user_id: int
    file_path: str
    file_size: int
    mime_type: str
    created_at: datetime.datetime
    updated_at: datetime.datetime                   

    class Config:
        orm_mode = True