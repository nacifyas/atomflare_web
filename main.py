import uvicorn
from routers import images, services
from fastapi import FastAPI
from sql.database import engine, Base

app = FastAPI()

app.include_router(images.router)
app.include_router(services.router)

@app.on_event("startup")
async def startup():
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@app.get('/')
async def root():
    return 'Hello world'

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True, host="127.0.0.1")