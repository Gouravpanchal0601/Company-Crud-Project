# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from database import SessionLocal, engine, Base
from model import User, Employee
from schemas import UserRegister, UserVerifyOTP, Token, UserCreate
import auth
from schemas import EmployeeResponse, EmployeeBase, UserCreate, Token

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Role + OTP Auth System")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

@app.post("/register")
def register(data: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    otp = auth.generate_otp()
    otp_expiry = datetime.utcnow() + timedelta(minutes=auth.OTP_EXPIRY_MINUTES)

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=auth.hash_password(data.password),
        role=data.role,
        otp_code=otp,
        otp_expiry=otp_expiry,
        is_verified=False
    )

    db.add(user)
    db.commit()

    print("OTP SENT:", otp)

    return {"message": "OTP sent to email"}

@app.post("/verify-otp")
def verify_otp(data: UserVerifyOTP, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.otp_code != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if user.otp_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    user.is_verified = True
    user.otp_code = None
    user.otp_expiry = None

    db.commit()

    return {"message": "Account verified"}

@app.post("/token", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()

    if not user or not auth.verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Verify OTP first")

    token = auth.create_access_token(
        {"sub": user.username, "role": user.role}
    )

    return {"access_token": token, "token_type": "bearer"}

# @app.get("/admin-only", response_model=list[EmployeeResponse])
# def admin_only(db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
#     if current_user.role != "admin":
#         raise HTTPException(status_code=403, detail="Only Admins Allowed")

#     employees_detail = db.query(Employee).all()
#     return employees_detail

@app.get("/admin-only", response_model=list[EmployeeResponse])
def admin_only(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "admin":
        return db.query(Employee).all()

    return (
        db.query(Employee).filter(Employee.name == current_user.username).all()
    )

@app.post("/employees", response_model=EmployeeResponse)
def create_employee(employee: EmployeeBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    emp = Employee(name=employee.name, age=employee.age, department=employee.department)
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

@app.get("/employees", response_model=list[EmployeeResponse])
def read_employees(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Employee).all()

@app.get("/employees/{emp_id}", response_model=EmployeeResponse)
def read_employee(emp_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@app.put("/employees/{emp_id}", response_model=EmployeeResponse)
def update_employee(emp_id: int, employee: EmployeeBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    emp.name = employee.name
    emp.age = employee.age
    emp.department = employee.department
    db.commit()
    db.refresh(emp)
    return emp

@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(emp)
    db.commit()
    return {"message": "Employee deleted"}
