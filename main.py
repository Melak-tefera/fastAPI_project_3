from fastapi import FastAPI
import models
from router import register, login, posts, refresh

app= FastAPI()
app.include_router(register.router)

app.include_router(login.router)
app.include_router(posts.router)
app.include_router(refresh.router)