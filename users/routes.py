from fastapi import APIRouter, Depends, UploadFile, HTTPException, status, File
from sqlalchemy.orm import Session
from auth.dependencies import get_db, get_authorized_user, get_all_users, verify_user_auth, get_users_by_query, delete_existing_user
from .schemas import User
from .models import User as UserModel, UserFiles
from typing import List
import os
from .defs import get_file_by_id, get_file_by_name, delete_file
import zipfile
from fastapi.responses import StreamingResponse, FileResponse
import io



router = APIRouter(dependencies=[Depends(verify_user_auth)])

@router.get("/me", response_model=User)
def read_my_user_details(current_user: UserModel = Depends(get_authorized_user)):
    return current_user

@router.get("/list", response_model=list[User])
def fetch_all_user_list(user_list: list[User] = Depends(get_all_users)):
    return user_list

@router.get("/search", response_model=list[User])
def fetch_user_by_query(user_list: list[User] = Depends(get_users_by_query)):
    return user_list

@router.delete("/remove/{id}")
def remove_existing_user(resp: str = Depends(delete_existing_user)):
    return resp

@router.post("/files/upload")
def upload_files(files: List[UploadFile] = File(...),  db: Session = Depends(get_db), auth_user: User = Depends(get_authorized_user)):
    added_files = []
    for file in files:
        try:
            fileDir = os.getcwd()+"\\users\\uploads\\"+str(auth_user.id)+"\\"
            filePath = fileDir+file.filename.replace(" ", "-")
            if not os.path.exists(fileDir):
                os.makedirs(fileDir)
            
            if os.path.exists(filePath):
                existingFile = get_file_by_name(db, file.filename)
                temp_info = {'file_name': existingFile.filename, 'id': existingFile.id}
                added_files.append(temp_info)
                continue
            else:
                contents = file.file.read()
                with open(filePath, 'wb') as f:
                    f.write(contents)
                    #insert file data into db
                    fileDetails = UserFiles()
                    fileDetails.filename = file.filename
                    fileDetails.user_id = auth_user.id
                    fileDetails.file_path = filePath
                    fileDetails.file_size = file.size
                    fileDetails.mime_type = file.content_type
                    print("filename: ", fileDetails.filename, " size: ", fileDetails.file_size, " mime: ", fileDetails.mime_type, ' path: ', fileDetails.file_path)
                    db.add(fileDetails)
                    db.commit()
                    db.refresh(fileDetails)
                    temp_info = {'file_name': fileDetails.filename, 'id': fileDetails.id}
                    added_files.append(temp_info)
        except Exception:
            raise HTTPException(status_code=500, detail='Something went wrong')
        finally:
            file.file.close()

    return {"Success": added_files} 


@router.post("/files/download/by-list")
def download_files_by_list(idList: List[int],  db: Session = Depends(get_db), auth_user: User = Depends(get_authorized_user)):
    zip_subdir = os.getcwd()+"\\users\\uploads\\"

    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as temp_zip:
        for file_id in idList:
            existingFile = get_file_by_id(db, file_id)
            if existingFile is not None:
                # Calculate path for file in zip
                # Add file, at correct path
                temp_zip.write(existingFile.file_path)
            else:
                pass
    return StreamingResponse(
        iter([zip_io.getvalue()]), 
        media_type="application/x-zip-compressed", 
        headers = { "Content-Disposition": f"attachment; filename=my_files.zip"}
    )

@router.get("/files/{file_id}")
def get_file(file_id: int, db: Session = Depends(get_db), auth_user: User = Depends(get_authorized_user)):
    existingFile = get_file_by_id(db, file_id)
    if existingFile is None:
        raise HTTPException(status_code=400, detail="incorrect file")
    return FileResponse(path=existingFile.file_path)

@router.get("/files/download/{file_id}")
def download_file_by_id(file_id: int, db: Session = Depends(get_db), auth_user: User = Depends(get_authorized_user)):
    existingFile = get_file_by_id(db, file_id)
    if existingFile is None:
        raise HTTPException(status_code=400, detail="incorrect file")
    return FileResponse(path=existingFile.file_path, media_type='application/octet-stream', filename=existingFile.filename)

@router.post("/files/remove")
def remove_files_by_ids(idList: List[int],  db: Session = Depends(get_db), auth_user: User = Depends(get_authorized_user)):
    removedFiles = []
    for file_id in idList:
        
        existingFile = get_file_by_id(db, file_id)
        if (existingFile is not None) and existingFile.user_id == auth_user.id:
            #only owners are allowed to delete the files
            os.remove(existingFile.file_path)
            delete_file(db, existingFile )
            temp_info = {'file_id':  existingFile.id, 'status': 'success'}
            removedFiles.append(temp_info)
        else:
            temp_info = {'file_id':  file_id, 'status': 'failed : incorrect file or user details submitted'}
            removedFiles.append(temp_info)

    return removedFiles
