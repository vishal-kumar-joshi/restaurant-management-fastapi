from fastapi import FastAPI
from sqlalchemy import text
from app.database import engine
from app.routers import customer, menu , category, restorenttable, admin,order,websocket
from utils import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Restaurant Management System",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(customer.router)
app.include_router(menu.router)
app.include_router(category.router)
app.include_router(restorenttable.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(order.router)
app.include_router(websocket.router)



@app.get("/test-db")
def test_db():
    with engine.connect() as connection:
        connection.execute(text("select 1"))
        return {"message" : "database connected"}

