from logging import debug
import uvicorn
from fastapi import FastAPI, Response
import time

app = FastAPI()


@app.get("/fraud/hello")
async def hello():
    time.sleep(1)
    body = "Hello Fraud {}:{}".format(time.localtime().tm_min,
                                      time.localtime().tm_sec)
    return Response(content=body, status_code=200)


if __name__ == '__main__':
    uvicorn.run('fraud_service:app', port=8000, reload=True)
