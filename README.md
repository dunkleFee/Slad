# Keepa Price API

FastAPI-приложение для получения информации о товаре с Amazon через Keepa API.

## Эндпоинт

`GET /price?asin=ASIN_HERE`

## Пример ответа
```json
{
  "asin": "B01EGKOH4E",
  "title": "Название товара"
}