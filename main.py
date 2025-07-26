from fastapi import FastAPI, Query
import keepa
from fastapi.responses import JSONResponse
import os
import time

app = FastAPI()

API_KEY = os.environ.get("KEEPA_API_KEY")

@app.get("/price")
def get_product_price(asin: str = Query(...)):
    try:
        api = keepa.Keepa(API_KEY)

        # Шаг 1: форсируем обновление
        api.query([asin], domain='US', update=True)
        time.sleep(15)

        # Шаг 2: получаем свежие данные
        result = api.query([asin], domain='US')
        if not result or not isinstance(result, list) or len(result) == 0:
            return JSONResponse(status_code=404, content={"error": "Товар не найден"})

        product = result[0]

        if not product:
            return JSONResponse(status_code=404, content={"error": "Данные по ASIN отсутствуют"})

        title = product.get("title") or "Без названия"
        price_cents = product.get("stats", {}).get("current", [])
        price = price_cents[0] / 100 if price_cents and price_cents[0] != -1 else None

        return {
            "asin": asin,
            "title": title,
            "price": price
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})