from fastapi import FastAPI
from app.routes.issues import router as issues_router
from app.middleware.timer import timing_middleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.middleware("http")(timing_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_orgins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_header=["*"],
)

app.include_router(issues_router)



