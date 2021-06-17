import uvicorn
from fastapi import FastAPI
import httpx
import time
from circuit_breaker import circuit_breaker

fraud_base_url = 'http://127.0.0.1:8000'

app = FastAPI()


@app.get("/order/hello")
async def hello():
    try:
        return await get_hello()
    except Exception:
        return await get_hello_fallback()


@circuit_breaker(__pybreaker_call_async=True)
async def get_hello():
    async with httpx.AsyncClient(base_url=fraud_base_url) as client:
        response = await client.get('/fraud/hello', timeout=3)
        response.raise_for_status()
        return response.text


async def get_hello_fallback():
    return "Hello Order fallback {}:{}".format(time.localtime().tm_min,
                                               time.localtime().tm_sec)


@app.get("/circuit")
def get_circuit():
    return {
        "current_state": circuit_breaker.current_state,
        "fail_counter": circuit_breaker.fail_counter
    }


if __name__ == '__main__':
    uvicorn.run('order_service:app', port=8001, reload=True)
