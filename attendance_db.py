from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import date
from pydantic import BaseModel
from typing import List


# Database Configuration
username = "root"
password = "Mysql%400195"
DATABASE_URL = "mysql+pymysql://{0}:{1}@127.0.0.1:3306/attendance_db".format(username, password)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI App Initialization
app = FastAPI()

# Database Model
class StudentAttendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    registration_number = Column(String(255), nullable=False, unique=True)
    branch = Column(String(255), nullable=False)
    section = Column(String(255), nullable=False)
    date = Column(Date, nullable=False, default=date.today)
    present = Column(Boolean, nullable=False)

# Create Tables
Base.metadata.create_all(bind=engine)


class StudentAttendanceResponse(BaseModel):
    id: int
    name: str
    registration_number: str
    branch: str
    section: str
    date: date
    present: bool

    class Config:
        orm_mode = True

# Pydantic Models
class AttendanceCreate(BaseModel):
    name: str
    registration_number: str
    branch: str
    section: str
    date: date
    present: bool

class AttendanceUpdate(BaseModel):
    date: date
    present: bool
    section: str

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.post("/attendance/", response_model=dict)
def create_attendance_record(record: AttendanceCreate, db: Session = Depends(get_db)):
    # Check if student record exists
    db_student = db.query(StudentAttendance).filter(
        StudentAttendance.registration_number == record.registration_number,
        StudentAttendance.date == record.date
    ).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Attendance record already exists for this date.")

    new_record = StudentAttendance(
        name=record.name,
        registration_number=record.registration_number,
        branch=record.branch,
        section=record.section,
        date=record.date,
        present=record.present
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return {"message": "Attendance record created successfully."}

@app.get("/attendance/{registration_number}", response_model=List[StudentAttendanceResponse])
def get_attendance(registration_number: str, db: Session = Depends(get_db)):
    records = db.query(StudentAttendance).filter(
        StudentAttendance.registration_number == registration_number
    ).all()
    if not records:
        raise HTTPException(status_code=404, detail="No attendance records found for this student.")
    return records

@app.put("/attendance/{registration_number}", response_model=dict)
def update_attendance(
    registration_number: str,
    update: AttendanceUpdate,
    db: Session = Depends(get_db)
):
    record = db.query(StudentAttendance).filter(
        StudentAttendance.registration_number == registration_number,
        StudentAttendance.date == update.date
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found.")

    record.present = update.present
    record.section = update.section
    db.commit()
    return {"message": "Attendance record updated successfully."}

@app.delete("/attendance/{registration_number}/{date}", response_model=dict)
def delete_attendance(
    registration_number: str,
    date: date,
    db: Session = Depends(get_db)
):
    record = db.query(StudentAttendance).filter(
        StudentAttendance.registration_number == registration_number,
        StudentAttendance.date == date
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found.")

    db.delete(record)
    db.commit()
    return {"message": "Attendance record deleted successfully."}
