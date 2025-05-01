"""
config.py · Model Name Configuration

This utility module provides a centralized way to retrieve
the LLM model name (e.g., "gpt-3.5-turbo") from environment variables.

This ensures consistency across all modules that invoke OpenAI APIs,
and allows for easy switching between models without changing multiple files.

Main Use Case:
--------------
Imported by:
- formatter_llm.py
- highlight_llm.py
- planner_llm.py
- feedback_learner.py
- style_classifier.py

Key Features:
-------------
✅ Avoids hardcoded model strings  
✅ Defaults to "gpt-3.5-turbo" if env var is missing  
✅ Compatible with deployment configuration

Author: Tripllery AI Backend
"""

import os

# ✅ Main model configuration used by all OpenAI LLM calls
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
