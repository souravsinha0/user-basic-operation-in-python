from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from auth.dependencies import get_db, verify_user_auth, get_accessed_user_detail, get_authorized_user
from .schemas import ToDoBase, ToDoResp
from .models import ToDoList
from fastapi.security import OAuth2PasswordBearer
from users.models import User
import pandas as pd
from fastapi.responses import StreamingResponse
import io
import openpyxl
from IPython.display import display


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(dependencies=[Depends(verify_user_auth)])

@router.post("/add", response_model=ToDoResp)
def add_task_to_list(task: ToDoBase, db: Session = Depends(get_db), auth_user: User = Depends(get_authorized_user)):

    newTask = ToDoList(task_name=task.task_name, user_id=auth_user.id)
    db.add(newTask)
    db.commit()
    db.refresh(newTask)
    return newTask

@router.get("/get/all", response_model=list[ToDoResp])
def list_all_tasks(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, auth_user: User = Depends(get_authorized_user)):

    taskList = db.query(ToDoList).filter(ToDoList.user_id == auth_user.id).offset(skip).limit(limit).all()
    if taskList is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no tasks found for the user")
    else:
        return taskList
    
@router.delete("/remove/{id}")
def list_all_tasks(id: int, db: Session = Depends(get_db), auth_user: User = Depends(get_authorized_user)):

    task = db.query(ToDoList).get(id)
    if task.id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="requested task details not found")
    else:
        db.delete(task)
        db.commit()
        return "Success"

@router.post("/export")
def get_tasks_in_excel_file(db: Session = Depends(get_db), auth_user: User = Depends(get_authorized_user)):
    # get all tasks of the user
    taskList = db.query(ToDoList).filter(ToDoList.user_id == auth_user.id).all()
    if taskList is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no tasks found for the user")
    else:
        idList = []
        taskNames = []
        progressList = []
        createdTimeList = []
        for item in taskList:
            curId = item.id
            curTask = item.task_name
            progress = item.is_task_completed
            curCreatedTime = item.created_at
            idList.append(curId)
            taskNames.append(curTask)
            progressList.append(progress)
            createdTimeList.append(curCreatedTime)

        df = pd.DataFrame(list(zip(idList, taskNames, progressList, createdTimeList)),
               columns =['id', 'task_name', 'is_task_completed', 'created_at (utc)'])

    return StreamingResponse(
        iter([df.to_csv(index=False)]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=my_task_list_exported.csv"}
)


@router.post("/import/")
async def upload_task_file(file: UploadFile = File(...), db: Session = Depends(get_db), auth_user: User = Depends(get_authorized_user)):
    if file.filename.endswith('.xlsx'):
        # Read it, 'f' type is bytes
        f = await file.read()
        xlsx = io.BytesIO(f)
        sheet_name = 'Sheet1'
        # open the spreadsheet
        wb = openpyxl.load_workbook(xlsx)
        # get the sheet
        sheet = wb.get_sheet_by_name(sheet_name)

        excel_contents = []
        for row in range(2, sheet.max_row +1):
            task_name = sheet['A'+str(row)].value
            temp_dict = {'task_name': task_name}
            excel_contents.append(temp_dict)

        # put our excel contents into the database
        for t in excel_contents:
            task = ToDoList(task_name=t['task_name'], user_id=auth_user.id)
            db.add(task)
            # commit the changes to the database
            db.commit()
            db.refresh(task)
        return excel_contents
    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
