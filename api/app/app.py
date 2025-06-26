from asyncio import sleep
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
#import logger
from utils.logs import get_logger
logger = get_logger()

# Start fastAPI
app = FastAPI()

prefix_api_v1 = ''

origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Default route
@app.get(f"{prefix_api_v1}/", tags=["Root"], 
            response_description="Get message from root path")
async def read_root():
    return {
        "status_code": status.HTTP_200_OK,
        "response_type": "success",
        "detail": "Welcome to Demo API."
    }


# Default test endpoint
@app.get(f"{prefix_api_v1}/demo", 
            response_description="Demo endpoint",)
async def read_root():
    return {
        "status_code": status.HTTP_200_OK,
        "response_type": "success",
        "detail": "Demo endpoint"
    }

