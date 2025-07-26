from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import keepa
import time

app = FastAPI()

API_KEY = "9s53td5fjae0t5sr7rp5tfeq4ton69ng5eocg77e3a66t00gef3gaqdmcjsis7ec"

class ProductResponse(BaseModel):
    asin: str
    title: str
    price: float | None

@app.get("/")
def root():
    return {"message": "Keepa API работает. Используйте /price?asin=..."}

@app.get("/price", response_model=ProductResponse)
def get_price(asin: str = Query(...)):
    try:
        api = keepa.Keepa(API_KEY)

        # Форс-обновление + ожидание
        api.query([asin], domain='US', update=True)
        time.sleep(15)

        product = api.query([asin], domain='US')[0]
        title = product.get("title") or "Без названия"

        # Получение текущей цены (в центах → /100)
        price = None
        stats = product.get("stats")
        if stats and "current" in stats:
            price_list = stats["current"]
            amazon_price = price_list[0]
            if amazon_price and isinstance(amazon_price, int):
                price = round(amazon_price / 100, 2)

        return {"asin": asin, "title": title, "price": price}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})