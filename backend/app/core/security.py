import os
from fastapi import Header, HTTPException

def require_api_key(x_api_key: str = Header(None)):
    expected = os.getenv("APP_API_KEY")
    if not expected:
        raise HTTPException(status_code=500, detail="APP_API_KEY not set in environment")

    if x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
