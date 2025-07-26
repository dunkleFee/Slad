from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import keepa
import time

app = FastAPI()

API_KEY = "9s53td5fjae0t5sr7rp5tfeq4ton69ng5eocg77e3a66t00gef3gaqdmcjsis7ec"

@app.get("/test-title")
def test_title(asin: str = Query(..., description="ASIN товара")):
    try:
        api = keepa.Keepa(API_KEY)

        # Простой запрос без обновления товара
        result = api.query([asin], domain='US')

        if not result or result[0] is None:
            return JSONResponse(status_code=404, content={"error": "Товар не найден"})

        product = result[0]
        title = product.get("title") or "Нет названия"

        return {"asin": asin, "title": title}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
