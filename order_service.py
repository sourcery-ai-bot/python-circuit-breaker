import uvicorn
from fastapi import FastAPI
import httpx
import time

fraud_base_url = 'http://127.0.0.1:8000'

app = FastAPI()


@app.get("/order/hello")
async def hello():
    try:
        return await get_hello()
    except Exception:
        return await get_hello_fallback()


async def get_hello():
    async with httpx.AsyncClient(base_url=fraud_base_url) as client:
        response = await client.get('/fraud/hello', timeout=3)
        response.raise_for_status()
        return response.text


async def get_hello_fallback():
    return "Hello Order fallback {}:{}".format(time.localtime().tm_min,
                                               time.localtime().tm_sec)


if __name__ == '__main__':
    uvicorn.run('order_service:app', port=8001, reload=True)
