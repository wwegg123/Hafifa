from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.air_quality import router as air_quality_router
from routes.alerts import router as alerts_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=air_quality_router)
app.include_router(router=alerts_router)