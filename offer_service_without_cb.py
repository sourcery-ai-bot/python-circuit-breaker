import uvicorn
from fastapi import FastAPI
import httpx
import time

partner_offer_url = 'http://127.0.0.1:8000'

app = FastAPI()


@app.get("/offer")
def offer():
    try:
        return get_offer()
    except Exception:
        return get_cold_offer_fallback()


def get_offer():
    with httpx.Client(base_url=partner_offer_url) as client:
        response = client.get('/offer/hot', timeout=2)
        response.raise_for_status()
        return response.text


def get_cold_offer_fallback():
    return "Cold offer fallback {}:{}".format(time.localtime().tm_min,
                                              time.localtime().tm_sec)


if __name__ == '__main__':
    uvicorn.run('offer_service_without_cb:app', port=8001, reload=True)
