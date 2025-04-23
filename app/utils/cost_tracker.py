"""
Tracks and analyzes token usage and cost metrics for LLM queries.

This module records token counts and associated costs per interaction using model-specific
pricing. It stores cost data in a local SQLite database and provides aggregated reports
grouped by day, week, or month, as well as breakdowns by LLM model.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class CostTracker:
    """Track and manage LLM API costs."""

    def __init__(self, db_path: str='monitoring.db'):
        """__init__ - Tracks token usage and cost estimation for LLM queries."""
        self.db_path = db_path

    def track_interaction_cost(self, interaction_id: int, tokens_input: int, tokens_output: int, model: str) -> float:
        """Calculate and track cost for an interaction."""
        input_cost_per_1k = {'gpt-3.5-turbo': 0.0015, 'gpt-4': 0.03, 'gpt-4-32k': 0.06}
        output_cost_per_1k = {'gpt-3.5-turbo': 0.002, 'gpt-4': 0.06, 'gpt-4-32k': 0.12}
        input_cost = tokens_input / 1000 * input_cost_per_1k.get(model, 0.002)
        output_cost = tokens_output / 1000 * output_cost_per_1k.get(model, 0.002)
        total_cost = input_cost + output_cost
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('\n            CREATE TABLE IF NOT EXISTS cost_tracking (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                interaction_id INTEGER,\n                model TEXT,\n                tokens_input INTEGER,\n                tokens_output INTEGER,\n                input_cost REAL,\n                output_cost REAL,\n                total_cost REAL,\n                timestamp TEXT,\n                FOREIGN KEY (interaction_id) REFERENCES interactions (id)\n            )\n            ')
        cursor.execute('\n            INSERT INTO cost_tracking\n            (interaction_id, model, tokens_input, tokens_output, input_cost, output_cost, total_cost, timestamp)\n            VALUES (?, ?, ?, ?, ?, ?, ?, ?)\n            ', (interaction_id, model, tokens_input, tokens_output, input_cost, output_cost, total_cost, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return total_cost

    def get_cost_report(self, start_date: Optional[datetime]=None, end_date: Optional[datetime]=None, group_by: str='day') -> Dict[str, Any]:
        """Get a cost report for a date range."""
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if group_by == 'day':
            group_clause = "strftime('%Y-%m-%d', timestamp)"
        elif group_by == 'week':
            group_clause = "strftime('%Y-%W', timestamp)"
        elif group_by == 'month':
            group_clause = "strftime('%Y-%m', timestamp)"
        else:
            group_clause = "strftime('%Y-%m-%d', timestamp)"
        cursor.execute(f'\n            SELECT \n                {group_clause} as period,\n                SUM(total_cost) as cost,\n                SUM(tokens_input) as tokens_input,\n                SUM(tokens_output) as tokens_output,\n                COUNT(*) as interactions_count\n            FROM cost_tracking\n            WHERE timestamp BETWEEN ? AND ?\n            GROUP BY period\n            ORDER BY period ASC\n            ', (start_date.isoformat(), end_date.isoformat()))
        results = cursor.fetchall()
        cursor.execute('\n            SELECT \n                model,\n                SUM(total_cost) as cost,\n                SUM(tokens_input) as tokens_input,\n                SUM(tokens_output) as tokens_output,\n                COUNT(*) as interactions_count\n            FROM cost_tracking\n            WHERE timestamp BETWEEN ? AND ?\n            GROUP BY model\n            ORDER BY cost DESC\n            ', (start_date.isoformat(), end_date.isoformat()))
        model_results = cursor.fetchall()
        conn.close()
        time_series = []
        for row in results:
            time_series.append({'period': row[0], 'cost': row[1], 'tokens_input': row[2], 'tokens_output': row[3], 'interactions_count': row[4]})
        by_model = []
        for row in model_results:
            by_model.append({'model': row[0], 'cost': row[1], 'tokens_input': row[2], 'tokens_output': row[3], 'interactions_count': row[4]})
        return {'start_date': start_date.isoformat(), 'end_date': end_date.isoformat(), 'group_by': group_by, 'total_cost': sum((item['cost'] for item in time_series)), 'total_interactions': sum((item['interactions_count'] for item in time_series)), 'time_series': time_series, 'by_model': by_model}