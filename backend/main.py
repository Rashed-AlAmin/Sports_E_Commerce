from fastapi import FastAPI
from backend.db.session import engine
from backend.routes import (
    test,
    auth,
    product,
    cart,order)
from backend.db.base import Base


app = FastAPI()

async def init_db():
    async with engine.begin() as conn:
        # run_sync allows you to run synchronous functions (like create_all) 
        # using the underlying synchronous connection of the async engine
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(auth.router)
app.include_router(test.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(order.router)