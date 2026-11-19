import os
import secrets


from typing import Annotated
from fastapi import FastAPI, Header, HTTPException, status, Depends


LISTEN_API_KEY = os.environ.get("LISTEN_API_KEY")

app = FastAPI(title="Listen API", version="1.0.0", description="API for Listen service")

@app.get("/health")
def health():
    return {"status": "ok"}



def require_api_key(x_api_key: Annotated[str | None, Header()] = None):
    if not LISTEN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key is not configured"
        )
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing"
        )
    if secrets.compare_digest(x_api_key, LISTEN_API_KEY):
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
@app.post("/identify", dependencies=[Depends(require_api_key)])


def identify():
    return {"stub": True}