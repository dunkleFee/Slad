from fastapi import FastAPI, Query
import keepa
import os
import time
from fastapi.responses import JSONResponse

app = FastAPI()

API_KEY = os.environ.get("KEEPA_API_KEY")

@app.get("/price")
def get_product_price(asin: str = Query(...)):
    try:
        api = keepa.Keepa(API_KEY)

        # Шаг 1: форс-обновление
        api.query([asin], domain='US', update=True)
        time.sleep(15)

        # Шаг 2: получить обновлённые данные
        result = api.query([asin], domain='US')
        if not result or not isinstance(result, list) or not result[0]:
            return JSONResponse(status_code=404, content={"error": "Товар не найден или данные недоступны"})

        product = result[0]
        title = product.get("title", "Нет названия")
        price_data = product.get("stats", {}).get("current", [])

        # Обработка пустого списка или -1
        if not price_data or price_data[0] in (-1, None):
            price = None
        else:
            price = round(price_data[0] / 100, 2)

        return {
            "asin": asin,
            "title": title,
            "price": price
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})