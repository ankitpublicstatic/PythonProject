# run this app, uvicorn users_api:app --reload


from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from db import SessionLocal
from models import User
from request_dto_schemas import UserCreate
from security import get_password_hash
from utils import get_date_range

app = FastAPI(title="Users API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exits
    errors = {}
    user_details = db.query(User)
    existing_email = user_details.filter(User.email == user.email).first()
    if existing_email:
        # raise HTTPException(
        #     status_code=status.HTTP_409_CONFLICT,
        #     detail=f"User with email {user.email} already exists",
        # )
        errors["email"] = "Email already registered"
    existing_username = user_details.filter(User.username == user.username).first()
    if existing_username:
        errors["username"] = "Username already registered"

    if errors:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"errors": errors})
        # raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"errors": errors})

    # {
    #     "errors": {
    #         "email": "Already exists",
    #         "username": "Taken"
    #     }
    # }

    # {"detail": "User with email ankitpm01@gmail.com already exists"}
    hashed_password = get_password_hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        agree_to_terms=user.agreeToTerms,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "username": new_user.username,
        "message": "User registered successfully",
    }


# def read_user(userId: int, db: Session = Depends(get_db)):
@app.get("/api/users/{userId}")
def read_user(userId: int):
    return {"userId": userId, "name": "Ram"}


@app.get("/api/users")
def read_users(db: Session = Depends(get_db)):
    query = text("""
                    SELECT
                        e.emp_id,
                        e.emp_name,
                        e.email
                    FROM employee e
                    """)
    result = db.execute(query)
    response = []
    for row in result:
        response.append(
            {"emp_id": row.emp_id, "emp_name": row.emp_name, "email": row.email, "leave_count": 0  # explicitly zero
             })
    db.close()
    return response


@app.get("/leave-compensation")
def fetch_employee_for_compensation(duration: str = Query(examples=["6M"]), db: Session = Depends(get_db)):
    """
     Fetch employees who have taken ZERO leaves in the given duration.
    :param db:
    :param duration:
    :return:
    """
    try:
        start_date, end_date = get_date_range(duration)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid duration. Use 1M, 6M, or 1Y")
    # db = SessionLocal()
    query = text("""
    SELECT
        e.emp_id,
        e.emp_name,
        e.email
    FROM employee e
    WHERE e.is_active = true
    AND NOT EXISTS (
        SELECT 1
        FROM emp_leave_info l
        WHERE l.emp_id = e.emp_id
        AND l.leave_date BETWEEN :start_date AND :end_date )
    """)
    result = db.execute(query, {"start_date": start_date, "end_date": end_date})

    response = []
    for row in result:
        response.append(
            {"emp_id": row.emp_id, "emp_name": row.emp_name, "email": row.email, "leave_count": 0  # explicitly zero
             })
    db.close()
    return response

