from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
# from database import Base
from sqlalchemy.orm import Session, sessionmaker
# from database import get_db
from sqlalchemy.ext.declarative import declarative_base

# Database Configuration
username = "root"
password = "Mysql%400195"
DATABASE_URL = "mysql+pymysql://{0}:{1}@127.0.0.1:3306/attendance_db".format(username, password)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# App Initialization
app = FastAPI()

# Secret key, algorithm, and token expiration time
SECRET_KEY = "e8c59a3ecc50a63786c075ed2f3bf5536b514fdb8a34923e69ea44a42e9d0a50"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Interactive user input
# username = input("Enter username (email): ").strip()
# password = input("Enter password: ").strip()

# Mock user database with dynamic input
fake_users_db = {
    username: {
        "username": username,
        "hashed_password": pwd_context.hash(password),
        "disabled": False,
    }
}

# # Mock user database
# fake_users_db = {
#     "user2@example.com": {
#         "username": "user2@example.com",
#         "hashed_password": pwd_context.hash("password2"),
#         "disabled": False,
#     }
# }

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

# Create Tables
Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# def get_user(db, username: str):
#     if username in db:
#         user = db[username]
#         return user

def get_user(db: Session, username: str):
    """
    Fetch a user from the database by username.
    """
    user = db.query(User).filter(User.username == username).first()
    return user

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists.")
    
    # Hash the password and create a new user
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Refresh to get the auto-generated fields like ID

    return {"message": "User signed up successfully", "username": new_user.username}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print("form data--",form_data)
    print(form_data.username)
    print(form_data.password)
    user = authenticate_user(db, form_data.username, form_data.password)
    print("USER is -",user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
