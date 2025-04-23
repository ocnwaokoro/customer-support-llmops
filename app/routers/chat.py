"""
Manages chat-related endpoints for user interaction with the LLM.

This module provides API routes for generating customer support responses using
language models, as well as for retrieving available prompt templates and their
versions. It interfaces with LLMService and PromptRepository to dynamically construct
context-aware responses.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from app.services.llm_service import LLMService
from app.prompts.templates import PromptRepository
router = APIRouter(prefix='/chat', tags=['chat'])

class ChatRequest(BaseModel):
    """ChatRequest - Manages chat-related endpoints for user interaction with the LLM."""
    question: str
    context: Optional[str] = None
    session_id: Optional[str] = None
    prompt_name: str = 'customer_support'
    prompt_version: Optional[str] = None
    model: Optional[str] = 'gpt-3.5-turbo'
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    """ChatResponse - Manages chat-related endpoints for user interaction with the LLM."""
    response: str
    interaction_id: int
    session_id: str
    latency_ms: int
    tokens_input: int
    tokens_output: int
    prompt_version: str

@router.post('/', response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Generate a response to a customer question."""
    if request.prompt_version:
        prompt_template = PromptRepository.get(request.prompt_name, request.prompt_version)
        if not prompt_template:
            raise HTTPException(status_code=404, detail=f'Prompt version {request.prompt_version} not found')
    prompt_params = {'question': request.question, 'context': request.context or 'No specific context provided.'}
    result = LLMService.generate_response(prompt_name=request.prompt_name, prompt_params=prompt_params, session_id=request.session_id, model=request.model, temperature=request.temperature, metadata={'source': 'api', 'ip': '127.0.0.1'})
    if 'error' in result:
        raise HTTPException(status_code=500, detail=result['error'])
    return result

@router.get('/prompts', response_model=List[Dict[str, Any]])
async def list_prompts():
    """List all available prompt templates."""
    return PromptRepository.list_all()

@router.get('/prompts/{name}/versions', response_model=List[Dict[str, Any]])
async def list_prompt_versions(name: str):
    """List all versions of a specific prompt template."""
    versions = PromptRepository.list_versions(name)
    if not versions:
        raise HTTPException(status_code=404, detail=f'Prompt {name} not found')
    return versions