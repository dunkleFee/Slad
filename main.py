from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import keepa

app = FastAPI()

API_KEY = "YOUR_KEEPA_API_KEY"

@app.get("/")
def root():
    return {"message": "Keepa API is running. Use /price?asin=..."}

@app.get("/price")
def get_price(asin: str = Query(..., description="ASIN from Amazon")):
    try:
        api = keepa.Keepa(API_KEY)
        result = api.query([asin], domain='US')

        product = result[0]
        title = product.get("title", "Unknown")
        return {"asin": asin, "title": title}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})