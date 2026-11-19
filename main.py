from fastapi import FastAPI
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import models
from router import register, login, posts, refresh, role

load_dotenv
app= FastAPI()

origins= [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


app.include_router(register.router)

app.include_router(login.router)
app.include_router(posts.router)
app.include_router(refresh.router)
app.include_router(role.router)