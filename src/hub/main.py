import uvicorn
from fastapi import FastAPI
from hub.routers import services, users, auths
from hub.sql.database import engine, Base

app = FastAPI()

app.include_router(services.router)
app.include_router(users.router)
app.include_router(auths.router)


@app.get("/initialize_db")
async def createdb() -> str:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        return "database recreated"

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True, host="127.0.0.1")
