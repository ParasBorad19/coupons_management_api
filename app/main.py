from fastapi import FastAPI
from .routes import coupons

app = FastAPI(title="Coupons API")
app.include_router(coupons.router)

@app.get("/")
def root():
    return {"status": "ok"}
