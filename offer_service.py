import uvicorn
from fastapi import FastAPI
import httpx
import time
from circuit_breaker import circuit_breaker

fraud_base_url = 'http://127.0.0.1:8000'

app = FastAPI()


@app.get("/offers")
async def offers():
    try:
        return await get_offers()
    except Exception:
        return await get_cold_offers_fallback()


@circuit_breaker(__pybreaker_call_async=True)
async def get_offers():
    async with httpx.AsyncClient(base_url=fraud_base_url) as client:
        response = await client.get('/offers/hot', timeout=2)
        response.raise_for_status()
        return response.text


async def get_cold_offers_fallback():
    return "Cold offers fallback {}:{}".format(time.localtime().tm_min,
                                               time.localtime().tm_sec)


@app.get("/offers/circuit")
def get_circuit():
    return {
        "current_state": circuit_breaker.current_state,
        "fail_counter": circuit_breaker.fail_counter
    }


if __name__ == '__main__':
    uvicorn.run('offer_service:app', port=8001, reload=True)
