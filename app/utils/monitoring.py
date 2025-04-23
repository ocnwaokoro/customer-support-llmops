"""
Logs and analyzes LLM interactions, user feedback, and flags for operational monitoring.

This module sets up and manages a local SQLite database to track LLM usage metrics,
user feedback ratings, and flagged responses. It supports detailed logging of interactions,
feedback comments, and performance metrics for observability and system improvement.
"""

import json
import sqlite3
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DB_PATH = 'monitoring.db'

class LLMMonitor:
    """Monitor and log LLM interactions and metrics."""

    def __init__(self, db_path: str=DB_PATH):
        """__init__ - Handles monitoring and metrics logging for LLM interactions."""
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        """Set up the monitoring database tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('\n        CREATE TABLE IF NOT EXISTS interactions (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            timestamp TEXT,\n            session_id TEXT,\n            prompt_name TEXT,\n            prompt_version TEXT,\n            prompt_text TEXT,\n            response_text TEXT,\n            tokens_input INTEGER,\n            tokens_output INTEGER,\n            latency_ms INTEGER,\n            model TEXT,\n            temperature REAL,\n            flagged BOOLEAN DEFAULT 0,\n            metadata TEXT\n        )\n        ')
        cursor.execute('\n        CREATE TABLE IF NOT EXISTS feedback (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            interaction_id INTEGER,\n            rating INTEGER,\n            comment TEXT,\n            categories TEXT,\n            timestamp TEXT,\n            FOREIGN KEY (interaction_id) REFERENCES interactions (id)\n        )\n        ')
        cursor.execute('\n        CREATE TABLE IF NOT EXISTS flags (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            interaction_id INTEGER,\n            flag_type TEXT,\n            flag_reason TEXT,\n            timestamp TEXT,\n            FOREIGN KEY (interaction_id) REFERENCES interactions (id)\n        )\n        ')
        conn.commit()
        conn.close()

    def log_interaction(self, session_id: str, prompt_name: str, prompt_version: str, prompt_text: str, response_text: str, tokens_input: int, tokens_output: int, latency_ms: int, model: str, temperature: float=0.7, metadata: Optional[Dict[str, Any]]=None) -> int:
        """Log an LLM interaction to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('\n            INSERT INTO interactions \n            (timestamp, session_id, prompt_name, prompt_version, prompt_text, \n             response_text, tokens_input, tokens_output, latency_ms, \n             model, temperature, metadata)\n            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)\n            ', (datetime.now().isoformat(), session_id, prompt_name, prompt_version, prompt_text, response_text, tokens_input, tokens_output, latency_ms, model, temperature, json.dumps(metadata or {})))
        interaction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        logger.info(f'Logged interaction {interaction_id} for session {session_id}')
        return interaction_id

    def log_feedback(self, interaction_id: int, rating: int, comment: Optional[str]=None, categories: Optional[List[str]]=None) -> int:
        """Log user feedback for an interaction."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('\n            INSERT INTO feedback\n            (interaction_id, rating, comment, categories, timestamp)\n            VALUES (?, ?, ?, ?, ?)\n            ', (interaction_id, rating, comment, json.dumps(categories or []), datetime.now().isoformat()))
        feedback_id = cursor.lastrowid
        conn.commit()
        conn.close()
        logger.info(f'Logged feedback {feedback_id} for interaction {interaction_id}')
        return feedback_id

    def flag_interaction(self, interaction_id: int, flag_type: str, flag_reason: str) -> int:
        """Flag an interaction for review."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE interactions SET flagged = 1 WHERE id = ?', (interaction_id,))
        cursor.execute('\n            INSERT INTO flags\n            (interaction_id, flag_type, flag_reason, timestamp)\n            VALUES (?, ?, ?, ?)\n            ', (interaction_id, flag_type, flag_reason, datetime.now().isoformat()))
        flag_id = cursor.lastrowid
        conn.commit()
        conn.close()
        logger.warning(f'Flagged interaction {interaction_id}: {flag_type} - {flag_reason}')
        return flag_id

    def get_metrics(self, days: int=7) -> Dict[str, Any]:
        """Get summary metrics for recent interactions."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM interactions WHERE timestamp >= datetime('now', ?)", (f'-{days} days',))
        total_count = cursor.fetchone()[0]
        cursor.execute("SELECT AVG(latency_ms) FROM interactions WHERE timestamp >= datetime('now', ?)", (f'-{days} days',))
        avg_latency = cursor.fetchone()[0] or 0
        cursor.execute("SELECT AVG(tokens_input), AVG(tokens_output) FROM interactions WHERE timestamp >= datetime('now', ?)", (f'-{days} days',))
        avg_tokens_input, avg_tokens_output = cursor.fetchone()
        avg_tokens_input = avg_tokens_input or 0
        avg_tokens_output = avg_tokens_output or 0
        cursor.execute("\n            SELECT AVG(f.rating) \n            FROM feedback f\n            JOIN interactions i ON f.interaction_id = i.id\n            WHERE i.timestamp >= datetime('now', ?)\n            ", (f'-{days} days',))
        avg_rating = cursor.fetchone()[0] or 0
        cursor.execute("\n            SELECT COUNT(*) \n            FROM flags f\n            JOIN interactions i ON f.interaction_id = i.id\n            WHERE i.timestamp >= datetime('now', ?)\n            ", (f'-{days} days',))
        flag_count = cursor.fetchone()[0]
        conn.close()
        return {'total_count': total_count, 'avg_latency_ms': round(avg_latency, 2), 'avg_tokens_input': round(avg_tokens_input, 2), 'avg_tokens_output': round(avg_tokens_output, 2), 'avg_rating': round(avg_rating, 2) if avg_rating else None, 'flag_count': flag_count, 'days': days}