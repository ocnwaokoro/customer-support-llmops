"""
Manages prompt templates and versioned prompt sets for LLM execution.

This module defines a simple file-based system for creating, saving, and retrieving prompt
templates used in a customer support LLM. Each template is versioned automatically using
a hash of its content and stored both as the latest version and in historical archives.
"""

import json
import os
from datetime import datetime
from pathlib import Path
import hashlib
PROMPTS_DIR = Path('prompts_repository')
PROMPTS_DIR.mkdir(exist_ok=True)
HISTORY_DIR = PROMPTS_DIR / 'history'
HISTORY_DIR.mkdir(exist_ok=True)

class PromptTemplate:
    """A versioned prompt template with metadata."""

    def __init__(self, name, template, description=None, version=None, metadata=None):
        """__init__ - Manages prompt templates and versioned prompt sets for LLM execution."""
        self.name = name
        self.template = template
        self.description = description or ''
        self.metadata = metadata or {}
        self.created_at = datetime.now().isoformat()
        if not version:
            content_hash = hashlib.md5(template.encode()).hexdigest()
            self.version = content_hash[:8]
        else:
            self.version = version

    def format(self, **kwargs):
        """Fill in the template with provided variables."""
        return self.template.format(**kwargs)

    def to_dict(self):
        """Convert template to dictionary representation."""
        return {'name': self.name, 'template': self.template, 'description': self.description, 'version': self.version, 'created_at': self.created_at, 'metadata': self.metadata}

    @classmethod
    def from_dict(cls, data):
        """Create a template from dictionary representation."""
        return cls(name=data['name'], template=data['template'], description=data.get('description', ''), version=data.get('version'), metadata=data.get('metadata', {}))

class PromptRepository:
    """Repository for managing and versioning prompt templates."""

    @staticmethod
    def save(prompt_template):
        """Save a prompt template with version control."""
        prompt_path = PROMPTS_DIR / f'{prompt_template.name}.json'
        with open(prompt_path, 'w') as f:
            json.dump(prompt_template.to_dict(), f, indent=2)
        history_path = HISTORY_DIR / f'{prompt_template.name}_{prompt_template.version}.json'
        with open(history_path, 'w') as f:
            json.dump(prompt_template.to_dict(), f, indent=2)
        return prompt_template.version

    @staticmethod
    def get(name, version=None):
        """Get a prompt template by name and optional version."""
        if version:
            path = HISTORY_DIR / f'{name}_{version}.json'
        else:
            path = PROMPTS_DIR / f'{name}.json'
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                return PromptTemplate.from_dict(data)
        except FileNotFoundError:
            return None

    @staticmethod
    def list_versions(name):
        """List all versions of a prompt template."""
        versions = []
        for path in HISTORY_DIR.glob(f'{name}_*.json'):
            version = path.stem.split('_', 1)[1]
            with open(path, 'r') as f:
                data = json.load(f)
                versions.append({'version': version, 'created_at': data.get('created_at'), 'description': data.get('description', '')})
        return sorted(versions, key=lambda x: x['created_at'], reverse=True)

    @staticmethod
    def list_all():
        """List all prompt templates."""
        templates = []
        for path in PROMPTS_DIR.glob('*.json'):
            name = path.stem
            template = PromptRepository.get(name)
            if template:
                templates.append({'name': name, 'version': template.version, 'description': template.description, 'created_at': template.created_at})
        return templates
CUSTOMER_SUPPORT_TEMPLATE = "\nYou are a helpful customer support assistant for Acme Inc.\nYour goal is to provide clear, concise, and accurate information to help customers with their inquiries.\n\nCONTEXT INFORMATION:\n{context}\n\nUSER QUESTION:\n{question}\n\nProvide a friendly and helpful response based on the context information.\nIf you don't know the answer based on the context, say so politely and suggest the customer contact support for more help.\n"

def initialize_default_templates():
    """initialize_default_templates - Manages prompt templates and versioned prompt sets for LLM execution."""
    customer_support = PromptTemplate(name='customer_support', template=CUSTOMER_SUPPORT_TEMPLATE, description='Customer support assistant prompt', metadata={'category': 'support', 'model': 'gpt-3.5-turbo'})
    PromptRepository.save(customer_support)
if not (PROMPTS_DIR / 'customer_support.json').exists():
    initialize_default_templates()