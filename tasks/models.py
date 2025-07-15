from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class ToDoList(Base):
    __tablename__ = "to_do_list"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    task_name = Column(String, index=True)
    is_task_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)      