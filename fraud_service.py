import uvicorn
from fastapi import FastAPI
import time

app = FastAPI()


@app.get("/hello")
async def hello():
    return "Hello Fraud {}:{}".format(time.localtime().tm_min,
                                      time.localtime().tm_sec)

if __name__ == '__main__':
    uvicorn.run('fraud_service:app', port=8000, reload=True)
