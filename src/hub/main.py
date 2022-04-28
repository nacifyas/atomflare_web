import uvicorn
from fastapi import FastAPI
from hub.routers import services, users, auths

app = FastAPI()

app.include_router(services.router)
app.include_router(users.router)
app.include_router(auths.router)

#####################

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True, host="127.0.0.1")
