from fastapi import FastAPI
from routers import services, users, auths

app = FastAPI()

app.include_router(services.router)
app.include_router(users.router)
app.include_router(auths.router)

# from sql.database import engine, Base
# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

#####################
import uvicorn
if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True, host="127.0.0.1")
