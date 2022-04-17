from datetime import timedelta
from auth.tokens import ACCESS_TOKEN_EXPIRE_MINUTES, Token, create_access_token
from routers import services, users
from routers.users import authenticate_user
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sql.database import engine, Base

app = FastAPI()

app.include_router(services.router)
app.include_router(users.router)

@app.on_event("startup")
async def startup():
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@app.get('/')
async def root():
    return 'Hello world'

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user("users_db", form_data.username, form_data.password)
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

#####################
import uvicorn
if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True, host="127.0.0.1")