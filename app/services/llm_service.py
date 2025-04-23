"""
Handles LLM interactions with prompt formatting, OpenAI API integration, and monitoring.

This module defines a service layer responsible for generating language model responses
based on prompt templates. It includes session tracking, latency measurement, token usage
logging, and automatic feedback submission to a monitoring backend.
"""

import os
import time
import uuid
import logging
from typing import Dict, List, Optional, Any
import openai
from openai import OpenAI
from app.prompts.templates import PromptRepository
from app.utils.monitoring import LLMMonitor
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', ''))
monitor = LLMMonitor()

class LLMService:
    """Service for handling LLM requests with monitoring and metrics."""

    @staticmethod
    def generate_response(prompt_name: str, prompt_params: Dict[str, Any], session_id: Optional[str]=None, model: str='gpt-3.5-turbo', temperature: float=0.7, max_tokens: int=500, metadata: Optional[Dict[str, Any]]=None) -> Dict[str, Any]:
        """Generate a response from the LLM using the specified prompt template."""
        if not session_id:
            session_id = str(uuid.uuid4())
        prompt_template = PromptRepository.get(prompt_name)
        if not prompt_template:
            logger.error(f'Prompt template not found: {prompt_name}')
            return {'error': 'Prompt template not found', 'session_id': session_id}
        formatted_prompt = prompt_template.format(**prompt_params)
        start_time = time.time()
        try:
            response = client.chat.completions.create(model=model, messages=[{'role': 'system', 'content': 'You are a helpful assistant.'}, {'role': 'user', 'content': formatted_prompt}], temperature=temperature, max_tokens=max_tokens)
            response_text = response.choices[0].message.content
            tokens_input = response.usage.prompt_tokens
            tokens_output = response.usage.completion_tokens
        except Exception as e:
            logger.error(f'LLM request failed: {str(e)}')
            return {'error': str(e), 'session_id': session_id}
        latency_ms = int((time.time() - start_time) * 1000)
        interaction_id = monitor.log_interaction(session_id=session_id, prompt_name=prompt_name, prompt_version=prompt_template.version, prompt_text=formatted_prompt, response_text=response_text, tokens_input=tokens_input, tokens_output=tokens_output, latency_ms=latency_ms, model=model, temperature=temperature, metadata=metadata or {})
        return {'response': response_text, 'interaction_id': interaction_id, 'session_id': session_id, 'latency_ms': latency_ms, 'tokens_input': tokens_input, 'tokens_output': tokens_output, 'prompt_version': prompt_template.version}