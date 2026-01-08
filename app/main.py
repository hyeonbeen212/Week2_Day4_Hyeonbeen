from fastapi import FastAPI
from app.router import agent_router

app = FastAPI()

#라우터 등록
app.include_router(agent_router.router)

@app.get("/")
def health_check():
    return {"status": "Server is running"}