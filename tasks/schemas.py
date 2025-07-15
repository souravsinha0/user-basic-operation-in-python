from pydantic import BaseModel
import datetime

class ToDoBase(BaseModel):
    task_name: str

class ToDoResp(ToDoBase):
    id: int
    user_id: int
    is_task_completed: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True   
"""
class ToDoList(ToDoBase):
    id: int
    user_id: int
    is_task_completed: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True  

  """      