from datetime import datetime, timedelta
from typing import Annotated
from fastapi import FastAPI, HTTPException, status, Depends
import logging as log
import uuid
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from model import (
    Token,
    TokenPublic,
    UserLogin,
    UserRead,
    engine,
    Link,
    LinkCreate,
    User,
    UserCreate,
    create_db_and_tables,
    get_db_session,
)
from pwdlib import PasswordHash

app = FastAPI()
create_db_and_tables()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="./token")

@app.get("/")
async def root():
    return {"message": "Welcome to LinkHub"}

async def get_curent_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db_session)) -> User:
    return await token_to_user(token, session)

async def token_to_user(token: str, session: Session) -> User:
        statement = select(Token).where(Token.token_value == token)
        db_token = session.exec(statement).first()

        # Verify token exists
        if db_token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
        
        expiration_time = db_token.expires_at
        if datetime.now() > expiration_time:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

        user = session.exec(select(User).where(User.id == db_token.user_id)).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user
        
    

@app.post("/links", status_code=status.HTTP_201_CREATED)
async def create_link(link: LinkCreate, user: Annotated[User, Depends(get_curent_user)], session: Session = Depends(get_db_session)) -> Link:
    link_db = Link(
        title=link.title, url=str(link.url), description=link.description
    )
    session.add(link_db)
    session.commit()
    session.refresh(link_db)
    return link_db


@app.get("/links", status_code=status.HTTP_200_OK)
async def get_all_links():
    links = []
    with Session(engine) as session:
        links = session.exec(statement=select(Link)).all()
        return {"links": links}


@app.get("/links/{link_id}", status_code=status.HTTP_200_OK)
async def get_link(link_id: int):
    log.debug(f"Fetching link with link id: {link_id}")
    with Session(engine) as session:
        statement = select(Link).where(Link.id == link_id)
        result = session.exec(statement).first()
        if not result:
            return {"message": "Link not found"}
        return {"link": result}


@app.get("/users", status_code=status.HTTP_200_OK, response_model=list[UserRead])
async def get_all_users(session: Session = Depends(get_db_session)):
    users = session.exec(select(User)).all()
    return users


pwd_context = PasswordHash.recommended()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def create_user(user: UserCreate, session: Session = Depends(get_db_session)):
    log.info("creating user")

    created_user = User(
        username=user.username,
        email=user.email,
        hashed_password=pwd_context.hash(user.password),
    )
    session.add(created_user)
    session.commit()
    session.refresh(created_user)
    return created_user


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UserRead)
async def get_user(user_id: int, session: Session = Depends(get_db_session)):
    log.debug(f"Fetching user with id: {user_id}")
    statement = select(User).where(User.id == user_id)
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result


# ==== AUTH ===
@app.post("/login", status_code=status.HTTP_201_CREATED, response_model=TokenPublic)
async def create_token(user_login: UserLogin, session: Session = Depends(get_db_session)):
    # Find user by username only
    statement = select(User).where(User.username == user_login.username)
    user: User | None = session.exec(statement).first()

    # Verify user exists and password is correct
    if user is None or user.id is None or not pwd_context.verify(user_login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # refresh token if it exist

    token = session.exec(select(Token).where(Token.user_id == user.id)).first()

    # create token
    if token:
       log.info("token already exists reseting expiration time")
       token.expires_in_seconds = 300
       token.created_at = datetime.now()
       session.add(token)
       session.commit()
       session.refresh(token)
       return token
    else:
        log.info("Creating token")

    token = Token(
        user_id=user.id,  # Now guaranteed to be int after the check above
        token_value=str(uuid.uuid4()),
        expires_at=datetime.now() + timedelta(seconds=300)
    )
    
    session.add(token)
    session.commit()
    session.refresh(token)

    return token


