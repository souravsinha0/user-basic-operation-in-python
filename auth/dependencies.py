from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import or_
from .utils import verify_password, get_password_hash, create_access_token
from .models import TokenData
from users.models import User
from .database import SessionLocal, engine, Base
import constants

Base.metadata.create_all(bind=engine, checkfirst=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8000/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


""" User related functions are defined in the following section : """
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_authorized_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, constants.SECRET_KEY, algorithms=[constants.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def verify_user_auth(cur_user = Depends(get_authorized_user)):
    
        if cur_user.username is not None:
            return True
        else:
            print('UNAUTHORISED!')
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        
async def get_accessed_user_detail(cur_user = Depends(get_authorized_user)):
    
        if cur_user.username is not None:
            return cur_user
        else:
            print('UNAUTHORISED!')
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        
def get_users_list(db: Session, offset, limit):
    return db.query(User).offset(offset).limit(limit).all()

def search_users(query: str, db: Session):
    return db.query(User).filter(or_( User.id.like(query),User.username.like(query+"%")))

def delete_user(id: int, db: Session):
    deleting_user = db.query(User).get(id)
    if deleting_user.username is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="requested user details not found")
    else:
        db.delete(deleting_user)
        db.commit()

#get all users list:
async def get_all_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    user_list = get_users_list(db, skip, limit)
    if user_list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return user_list

#search user by id or username:
def get_users_by_query(query: str, db: Session = Depends(get_db)):
    if query == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="empty search query")
    else:
        return search_users(query, db)

#delete existing user by user's id   
def delete_existing_user(id: int, db: Session = Depends(get_db)):
    if id == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="empty search query")
    else:
        delete_user(id, db)
        return "Success"

