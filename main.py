from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import keepa
import time

app = FastAPI()

# 🔐 ВСТРОЕННЫЙ КЛЮЧ (небезопасно для публичного репозитория!)
API_KEY = "9s53td5fjae0t5sr7rp5tfeq4ton69ng5eocg77e3a66t00gef3gaqdmcjsis7ec"

class PriceResponse(BaseModel):
    asin: str
    title: str
    price: float | None

@app.get("/")
def root():
    return {"message": "Keepa API работает. Используйте /price?asin=..."}

@app.get("/price", response_model=PriceResponse)
def get_product_price(asin: str = Query(..., description="ASIN товара с Amazon")):
    try:
        api = keepa.Keepa(API_KEY)

        # 🔁 Обновляем товар, ждём 15 секунд
        api.query([asin], domain='US', update=True)
        time.sleep(15)

        result = api.query([asin], domain='US')
        if not result or len(result) == 0 or result[0] is None:
            raise ValueError("Товар не найден")

        product = result[0]
        title = product.get("title") or "Нет названия"
        stats = product.get("stats", {})
        price_data = stats.get("current", [])

        price = None
        if isinstance(price_data, list) and len(price_data) > 0 and price_data[0]:
            price = round(price_data[0] / 100, 2)

        return {
            "asin": asin,
            "title": title,
            "price": price
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
