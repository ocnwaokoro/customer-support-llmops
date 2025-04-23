"""
Implements API key authentication for securing FastAPI endpoints.

This module defines a reusable dependency that verifies incoming requests
include a valid API key in the header. Unauthorized requests are rejected
with a 403 Forbidden response.
"""

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
import os
API_KEY_NAME = 'X-API-Key'
API_KEY = os.getenv('API_KEY', 'your-secure-api-key')
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str=Security(api_key_header)):
    """Validate API key."""
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Invalid API Key')

@router.post('/', response_model=ChatResponse, dependencies=[Depends(get_api_key)])
async def chat(request: ChatRequest):
    """chat - Provides API key validation and secure access controls."""
    pass