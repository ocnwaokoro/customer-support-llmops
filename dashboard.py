"""
Interactive dashboard for real-time LLMOps metrics using Streamlit.

This module visualizes system health, token usage, feedback ratings, and interaction
performance. It communicates with the backend API to fetch metrics and presents them
through an interactive UI for operations monitoring and model evaluation.
"""

import streamlit as st
import pandas as pd
import requests
import altair as alt
import json
from datetime import datetime, timedelta
st.set_page_config(page_title='LLMOps Dashboard', page_icon='📊', layout='wide')
BASE_URL = 'http://localhost:8000'
st.title('Customer Support LLMOps Dashboard')
st.sidebar.header('Settings')
date_range = st.sidebar.selectbox('Date range', ['Last 7 days', 'Last 30 days', 'Last 90 days'])
if date_range == 'Last 7 days':
    days = 7
elif date_range == 'Last 30 days':
    days = 30
else:
    days = 90

@st.cache_data(ttl=300)
def fetch_metrics(days):
    """fetch_metrics - Dashboard for real-time metrics visualization and system status."""
    response = requests.get(f'{BASE_URL}/feedback/metrics?days={days}')
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Error fetching metrics: {response.status_code}')
        return None
metrics = fetch_metrics(days)
if metrics:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total Interactions', metrics['total_count'])
    with col2:
        st.metric('Avg Latency', f"{metrics['avg_latency_ms']:.2f} ms")
    with col3:
        avg_rating = metrics.get('avg_rating')
        if avg_rating:
            st.metric('Avg Rating', f'{avg_rating:.1f} / 5')
        else:
            st.metric('Avg Rating', 'No ratings')
    with col4:
        st.metric('Flagged Interactions', metrics['flag_count'])
    st.subheader('Token Usage')
    token_data = {'Type': ['Input', 'Output'], 'Tokens': [metrics['avg_tokens_input'], metrics['avg_tokens_output']]}
    token_df = pd.DataFrame(token_data)
    token_chart = alt.Chart(token_df).mark_bar().encode(x='Type', y='Tokens', color='Type').properties(height=300)
    st.altair_chart(token_chart, use_container_width=True)

    @st.cache_data(ttl=300)
    def fetch_recent_interactions(limit=10):
        """fetch_recent_interactions - Dashboard for real-time metrics visualization and system status."""
        response = requests.get(f'{BASE_URL}/chat/recent?limit={limit}')
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f'Error fetching interactions: {response.status_code}')
            return []
    st.subheader('Recent Interactions')
    recent_interactions = [{'id': 1, 'question': 'How do I reset my password?', 'response': "To reset your password, go to the login page and click on 'Forgot Password'. Enter your email address and follow the instructions sent to your inbox.", 'latency_ms': 1250, 'timestamp': '2025-04-22T15:30:45', 'rating': 5}, {'id': 2, 'question': 'What are your subscription plans?', 'response': 'We offer three subscription plans: Basic ($9.99/month), Pro ($19.99/month), and Enterprise ($49.99/month).', 'latency_ms': 980, 'timestamp': '2025-04-22T14:45:12', 'rating': 4}]
    for interaction in recent_interactions:
        with st.expander(f"Q: {interaction['question']}"):
            st.write(f"**Response:**\n{interaction['response']}")
            st.write(f"**Latency:** {interaction['latency_ms']} ms")
            st.write(f"**Time:** {interaction['timestamp']}")
            if 'rating' in interaction:
                st.write(f"**Rating:** {'⭐' * interaction['rating']}")
else:
    st.warning('No metrics data available')