"""
Integration test suite for key customer support LLM endpoints.

This script validates the behavior of the `/chat`, `/feedback`, and `/feedback/metrics` endpoints
to ensure the customer support system is functioning as expected. It simulates user interaction,
submits feedback, and retrieves performance metrics.
"""

import requests
import json
BASE_URL = 'http://localhost:8000'

def test_chat():
    """test_chat - TODO: Add description."""
    print('Testing chat endpoint...')
    response = requests.post(f'{BASE_URL}/chat/', json={'question': 'How do I reset my password?', 'context': 'I forgot my password and need to log in.', 'session_id': 'test-session-001'})
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data['response']}")
        print(f"Interaction ID: {data['interaction_id']}")
        print(f"Latency: {data['latency_ms']}ms")
        return data
    else:
        print(f'Error: {response.status_code} - {response.text}')
        return None

def test_feedback(interaction_id):
    """test_feedback - TODO: Add description."""
    print('\nTesting feedback endpoint...')
    response = requests.post(f'{BASE_URL}/feedback/', json={'interaction_id': interaction_id, 'rating': 5, 'comment': 'Very helpful response!', 'categories': ['password', 'account']})
    if response.status_code == 200:
        data = response.json()
        print(f"Feedback ID: {data['feedback_id']}")
        print(f"Message: {data['message']}")
    else:
        print(f'Error: {response.status_code} - {response.text}')

def test_metrics():
    """test_metrics - TODO: Add description."""
    print('\nTesting metrics endpoint...')
    response = requests.get(f'{BASE_URL}/feedback/metrics')
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f'Error: {response.status_code} - {response.text}')
if __name__ == '__main__':
    chat_result = test_chat()
    if chat_result:
        test_feedback(chat_result['interaction_id'])
    test_metrics()