import uvicorn
from fastapi import FastAPI

from api_v1 import router as router_v1

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ScoreSpin"
)

app.include_router(router=router_v1, prefix="/api/v1")


origins = [
    "http://localhost",
    "http://localhost:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)
