from fastapi import FastAPI
from app.api.endpoints import router
import uvicorn

app = FastAPI(
    title="Financial Document Intelligence API",
    description="Automated Underwriting & Fraud Detection System",
    version="1.0"
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"status": "System is Online", "docs": "/docs"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
