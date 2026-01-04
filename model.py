from datetime import datetime
from sqlmodel import UUID, Field, SQLModel, Session, create_engine
from pydantic import BaseModel, HttpUrl, EmailStr
import os
from pwdlib import PasswordHash
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class LinkBase(SQLModel):
    title: str
    description: str | None = None

class LinkCreate(LinkBase):
    url: HttpUrl

class Link(LinkBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str
    created_at: datetime = Field(default_factory=datetime.now)


class UserBase(SQLModel):   
    username: str = Field(unique=True)
    email: EmailStr

class UserLogin(SQLModel):
    username: str
    password:str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    updated_at: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)
    hashed_password: str = Field()

class TokenPublic(BaseModel):
    token_value: str
    expires_at: datetime

class Token(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    token_value: str
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)
    expires_at: datetime = Field(default_factory=lambda: datetime.now() + timedelta(seconds=300))


# configure db connection with Engine 
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Echo SQL queries in development, disable in production
echo_sql = os.getenv("SQL_ECHO", "true").lower() == "true"
engine = create_engine(sqlite_url, echo=echo_sql)

# Creates the database and creates the link table
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

async def get_db_session():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

