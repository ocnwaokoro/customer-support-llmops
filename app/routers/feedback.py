"""
Handles collection, routing, and monitoring of user feedback on LLM-generated responses.

This module defines FastAPI endpoints to collect structured feedback from users,
log it via the monitoring system, and compute evaluation metrics such as average
ratings, latency, and token usage over time.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from app.utils.monitoring import LLMMonitor
router = APIRouter(prefix='/feedback', tags=['feedback'])
monitor = LLMMonitor()

class FeedbackRequest(BaseModel):
    """FeedbackRequest - Handles collection and routing of user feedback on LLM responses."""
    interaction_id: int
    rating: int
    comment: Optional[str] = None
    categories: Optional[List[str]] = None

class FeedbackResponse(BaseModel):
    """FeedbackResponse - Handles collection and routing of user feedback on LLM responses."""
    feedback_id: int
    message: str = 'Feedback recorded successfully'

class MetricsResponse(BaseModel):
    """MetricsResponse - Handles collection and routing of user feedback on LLM responses."""
    total_count: int
    avg_latency_ms: float
    avg_tokens_input: float
    avg_tokens_output: float
    avg_rating: Optional[float]
    flag_count: int
    days: int

@router.post('/', response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """Submit feedback for a specific interaction."""
    if request.rating < 1 or request.rating > 5:
        raise HTTPException(status_code=400, detail='Rating must be between 1 and 5')
    feedback_id = monitor.log_feedback(interaction_id=request.interaction_id, rating=request.rating, comment=request.comment, categories=request.categories)
    if request.rating <= 2:
        monitor.flag_interaction(interaction_id=request.interaction_id, flag_type='low_rating', flag_reason=f'Low rating ({request.rating}/5)')
    return FeedbackResponse(feedback_id=feedback_id)

@router.get('/metrics', response_model=MetricsResponse)
async def get_metrics(days: int=7):
    """Get summary metrics for recent interactions."""
    if days < 1 or days > 30:
        raise HTTPException(status_code=400, detail='Days must be between 1 and 30')
    metrics = monitor.get_metrics(days=days)
    return metrics