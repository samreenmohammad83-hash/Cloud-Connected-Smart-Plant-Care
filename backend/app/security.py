from fastapi import Header, HTTPException
from .config import DEVICE_API_KEY

def verify_device_key(x_device_key: str | None = Header(default=None)):
    if x_device_key != DEVICE_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid device API key")
    return True
