from fastapi import FastAPI

from src.core.database import lifespan
from src.api.routes import users, auth, advertisements

app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(advertisements.router)