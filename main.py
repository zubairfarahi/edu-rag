import uvicorn
from api.v1 import route
from fastapi import FastAPI

from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI(
    title="edu-chat-rag",
    description="testing",
    contact={
        "name": "zubair",
        "email": "farahi.zubair121@gmail.com"
    }
)


app.include_router(route)
if __name__ == '__main__':
    uvicorn.run(app, host=os.getenv('HOST'), port=os.getenv('PORT'), log_level="info")
