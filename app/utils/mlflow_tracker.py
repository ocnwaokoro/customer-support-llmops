"""
Integrates MLflow to track experiments, prompt evaluations, and LLM interaction metrics.

This module logs prompt tests, model parameters, performance metrics, and artifacts to an MLflow server.
It supports both structured experiment logging and ad hoc tracking of live LLM interactions for
auditability, reproducibility, and performance analysis.
"""

import mlflow
import mlflow.pyfunc
import os

class MLflowTracker:
    """Integration with MLflow for experiment tracking."""

    def __init__(self, experiment_name='customer-support-llm'):
        """__init__ - Integrates MLflow for experiment tracking and model evaluation."""
        mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI', 'http://localhost:5000'))
        try:
            self.experiment_id = mlflow.create_experiment(experiment_name)
        except:
            self.experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id

    def log_prompt_test(self, prompt_name: str, prompt_version: str, metrics: Dict[str, float], params: Dict[str, Any], artifacts: Optional[Dict[str, str]]=None) -> str:
        """Log a prompt test to MLflow."""
        with mlflow.start_run(experiment_id=self.experiment_id) as run:
            for key, value in params.items():
                mlflow.log_param(key, value)
            for key, value in metrics.items():
                mlflow.log_metric(key, value)
            if artifacts:
                for name, path in artifacts.items():
                    mlflow.log_artifact(path, name)
            mlflow.set_tags({'prompt_name': prompt_name, 'prompt_version': prompt_version, 'model_type': 'llm'})
            return run.info.run_id

    def log_interaction(self, interaction_data: Dict[str, Any]) -> str:
        """Log an individual interaction to MLflow."""
        with mlflow.start_run(experiment_id=self.experiment_id) as run:
            mlflow.log_param('prompt_name', interaction_data.get('prompt_name'))
            mlflow.log_param('prompt_version', interaction_data.get('prompt_version'))
            mlflow.log_param('model', interaction_data.get('model'))
            mlflow.log_param('temperature', interaction_data.get('temperature'))
            mlflow.log_metric('latency_ms', interaction_data.get('latency_ms'))
            mlflow.log_metric('tokens_input', interaction_data.get('tokens_input'))
            mlflow.log_metric('tokens_output', interaction_data.get('tokens_output'))
            if 'rating' in interaction_data:
                mlflow.log_metric('rating', interaction_data.get('rating'))
            with open('prompt.txt', 'w') as f:
                f.write(interaction_data.get('prompt_text', ''))
            with open('response.txt', 'w') as f:
                f.write(interaction_data.get('response_text', ''))
            mlflow.log_artifact('prompt.txt')
            mlflow.log_artifact('response.txt')
            mlflow.set_tags({'interaction_id': str(interaction_data.get('id')), 'session_id': interaction_data.get('session_id'), 'type': 'interaction'})
            return run.info.run_id