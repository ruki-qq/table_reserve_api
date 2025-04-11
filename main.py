from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from api import router_v1
from core.config import settings

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_v1, prefix=settings.api_prefix)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
    )
