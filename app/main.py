"""
FastAPI entrypoint for the Customer Support LLMOps service.

This module configures middleware, registers routers for chat and feedback,
and exposes health and root endpoints. It serves as the primary interface
for launching and interacting with the LLM-powered API.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, feedback
app = FastAPI(title='Customer Support LLMOps', description='An LLMOps implementation for customer support with monitoring and feedback', version='0.1.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.include_router(chat.router)
app.include_router(feedback.router)

@app.get('/')
async def root():
    """root - FastAPI app entrypoint. Registers routes and launches the service."""
    return {'message': 'Customer Support LLMOps API'}

@app.get('/health')
async def health_check():
    """health_check - FastAPI app entrypoint. Registers routes and launches the service."""
    return {'status': 'healthy'}