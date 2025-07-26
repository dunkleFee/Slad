from fastapi import FastAPI, Query
import keepa
from fastapi.responses import JSONResponse
import os

app = FastAPI()

API_KEY = os.environ.get("KEEPA_API_KEY")

@app.get("/price")
def get_product_price(asin: str = Query(...)):
    try:
        api = keepa.Keepa(API_KEY)

        # Форс-запрос
        api.query([asin], domain='US', update=True)
        
        import time
        time.sleep(15)  # ждать пока Keepa обновит данные

        product_data = api.query([asin], domain='US')
        product = product_data[0]
        title = product.get("title") or "Без названия"
        current_price = product.get("stats", {}).get("current", [])[0]

        return {
            "asin": asin,
            "title": title,
            "price": round(current_price / 100, 2) if current_price != -1 else None
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})