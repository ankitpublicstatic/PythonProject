# uv add fastapi uvicorn sqlalchemy psycopg2-binary
from requests import Session
# postgres root
# spring.datasource.username = root mysql
# spring.datasource.password = abcA1@2016

# run this app: uvicorn main:app --reload


from sqlalchemy import create_engine, text, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session


from  sqlalchemy.ext.declarative import declarative_base
from datetime import date, timedelta
from fastapi import FastAPI, Query, HTTPException, status,Depends
from fastapi.middleware.cors import CORSMiddleware

DATABASE_URL = "postgresql://postgres:root@localhost:5432/python"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

def get_date_range(duration: str):
    end_date = date.today()

    if duration == "1M":
        start_date = end_date - timedelta(days=30)
    elif duration == "6M":
        start_date = end_date - timedelta(days=180)
    elif duration == "1Y":
        start_date = end_date - timedelta(days=365)
    else:
        raise ValueError(f"Invalid duration: {duration}")
    return start_date, end_date

app = FastAPI(title="Leave Compensation API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"] )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def read_user(userId: int, db: Session = Depends(get_db)):
@app.get("/api/users/{userId}")
def read_user(userId: int):
    return {"userId": userId,"name":"Ram"}

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
        response.append({"emp_id": row.emp_id, "emp_name": row.emp_name, "email": row.email, "leave_count":0 # explicitly zero
                         })
    db.close()
    return response


@app.get("/leave-compensation")
def fetch_employee_for_compensation(duration: str = Query( examples=["6M"]), db: Session = Depends(get_db)):
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
        response.append({"emp_id": row.emp_id, "emp_name": row.emp_name, "email": row.email, "leave_count":0 # explicitly zero
                         })
    db.close()
    return response

