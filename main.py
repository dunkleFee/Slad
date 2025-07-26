from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import keepa

app = FastAPI()

API_KEY = "9s53td5fjae0t5sr7rp5tfeq4ton69ng5eocg77e3a66t00gef3gaqdmcjsis7ec"

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