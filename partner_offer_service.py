import uvicorn
from fastapi import FastAPI, Response
import time

app = FastAPI()


@app.get("/offer/hot")
async def get_offer():
    time.sleep(1)
    body = f"Hot offer {time.localtime().tm_min}:{time.localtime().tm_sec}"
    return Response(content=body, status_code=500)


if __name__ == '__main__':
    uvicorn.run('partner_offer_service:app', port=8000, reload=True)
