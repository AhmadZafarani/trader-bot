from fastapi import FastAPI
from enum import Enum
import subprocess
import os
from starlette.responses import FileResponse

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from fastapi.security import OAuth2PasswordBearer


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "ali": {
        "username": "ali",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Strategy(str, Enum):
    ichi = "ichi"
    ma = "ma"


app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    user = authenticate_user(
        fake_users_db, form_data.username, form_data.password)

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


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/single_month")
async def month(strtgg: Strategy, month: str, profit_loss_period_step: int = 48, periodical_profit_loss_limit_enable: int = 1, periodical_profit_limit: float = 18, periodical_loss_limit: float = -1.8,
                buy_method_line_to_line_enable: int = 1, buy_method_line_to_line_cross: int = 1, volume_buy_ma: int = 80, sell_method_line_to_line_enable: int = 0,
                global_limit: int = 0, global_loss_limit: float = 0, global_profit_limit: float = 0, token: str = Depends(oauth2_scheme)):
    sed_str = f'sed -i "s/\\(month = \\).*/\\1\\"{month}\\"/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(strtgg = \\).*/\\1\\"{strtgg}\\"/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(profit_loss_period_step = \\).*/\\1{profit_loss_period_step}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(periodical_profit_loss_limit_enable = \\).*/\\1{periodical_profit_loss_limit_enable}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(periodical_profit_limit = \\).*/\\1{periodical_profit_limit}/" scenario.py'

    sed_str = f'{sed_str};sed -i "s/\\(periodical_loss_limit = \\).*/\\1{periodical_loss_limit}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(global_limit = \\).*/\\1{global_limit}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(global_profit_limit = \\).*/\\1{global_profit_limit}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(global_loss_limit = \\).*/\\1{global_loss_limit}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(buy_method_line_to_line_enable = \\).*/\\1{int(buy_method_line_to_line_enable)}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(buy_method_line_to_line_cross = \\).*/\\1{int(buy_method_line_to_line_cross)}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(volume_buy_ma = \\).*/\\1{volume_buy_ma}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(sell_method_line_to_line_enable = \\).*/\\1{int(sell_method_line_to_line_enable)}/" scenario.py'
    os.system(sed_str)
    subprocess.run(["python", "main.py"], stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE, text=True)
    result = subprocess.run(["python", "analyze_output/analyze.py", "only-print-profit"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return {"profit": result.stdout}


@app.get("/all_month")
async def all_month(profit_loss_period_step: int = 48, periodical_profit_loss_limit_enable: int = 1, periodical_profit_limit: float = 18, periodical_loss_limit: float = -1.8,
                    buy_method_line_to_line_enable: int = 1, buy_method_line_to_line_cross: int = 1, volume_buy_ma: int = 80, sell_method_line_to_line_enable: int = 0,
                    global_limit: int = 0, global_loss_limit: float = 0, global_profit_limit: float = 0, token: str = Depends(oauth2_scheme)):
    sed_str = f'sed -i "s/\\(profit_loss_period_step = \\).*/\\1{profit_loss_period_step}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(periodical_profit_loss_limit_enable = \\).*/\\1{periodical_profit_loss_limit_enable}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(periodical_profit_limit = \\).*/\\1{periodical_profit_limit}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(periodical_loss_limit = \\).*/\\1{periodical_loss_limit}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(global_limit = \\).*/\\1{global_limit}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(global_profit_limit = \\).*/\\1{global_profit_limit}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(global_loss_limit = \\).*/\\1{global_loss_limit}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(buy_method_line_to_line_enable = \\).*/\\1{int(buy_method_line_to_line_enable)}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(buy_method_line_to_line_cross = \\).*/\\1{int(buy_method_line_to_line_cross)}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(volume_buy_ma = \\).*/\\1{volume_buy_ma}/" scenario.py'
    sed_str = f'{sed_str};sed -i "s/\\(sell_method_line_to_line_enable = \\).*/\\1{int(sell_method_line_to_line_enable)}/" scenario.py'
    os.system(sed_str)
    subprocess.run(["python", "main.py"], stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE, text=True)
    subprocess.run(["python", "analyze_output/analyze.py", "only-print-profit"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    subprocess.run(["bash", "all-parameters-test/all-parameters-test.sh", "1"])
    subprocess.run(["python", "all-parameters-test/join.py"])

    return FileResponse('all-parameters-test/final.csv', media_type='application/octet-stream', filename='final.csv')
