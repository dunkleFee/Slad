from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import keepa
import os
import time

app = FastAPI()

# 🔑 Укажи свой API-ключ как переменную окружения KEEPA_API_KEY
API_KEY = os.environ.get("9s53td5fjae0t5sr7rp5tfeq4ton69ng5eocg77e3a66t00gef3gaqdmcjsis7ec")

# 🎯 Структура ответа
class PriceResponse(BaseModel):
    asin: str
    title: str
    price: float | None

@app.get("/price", response_model=PriceResponse)
def get_product_price(asin: str = Query(..., description="ASIN товара с Amazon")):
    try:
        api = keepa.Keepa(API_KEY)

        # 🔄 Форс-обновление
        api.query([asin], domain='US', update=True)
        time.sleep(15)  # ожидание обновления

        # 🧩 Получение свежих данных
        result = api.query([asin], domain='US')

        if not result or not isinstance(result, list) or len(result) == 0:
            return JSONResponse(status_code=404, content={"error": "Товар не найден (пустой результат)"})

        product = result[0]
        if not product or not isinstance(product, dict):
            return JSONResponse(status_code=404, content={"error": "Нет данных по товару (null product)"})

        title = product.get("title", "Нет названия")
        stats = product.get("stats", {})
        price_data = stats.get("current", [])

        # 💰 Извлечение цены
        if isinstance(price_data, list) and len(price_data) > 0:
            raw_price = price_data[0]
            price = round(raw_price / 100, 2) if raw_price and raw_price > 0 else None
        else:
            price = None

        return {
            "asin": asin,
            "title": title,
            "price": price
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})