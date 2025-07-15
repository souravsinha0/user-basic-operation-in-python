import fastapi
from auth.dependencies import get_db
from sqlalchemy.orm import Session
from .models import UserFiles


def get_file_by_id(db: Session, id: int):
    return db.query(UserFiles).filter(UserFiles.id == id).first()

def get_file_by_name(db: Session, name: str):
    return db.query(UserFiles).filter(UserFiles.filename == name).first()

def delete_file(db: Session, delFile: UserFiles):
    db.delete(delFile)
    db.commit()
    return