# conftest.py
import pytest
import os
from dotenv import load_dotenv

def pytest_configure(config):
    """
    Custom pytest configuration
    """
    load_dotenv()  # Load environment variables from .env file

    # Register custom markers
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
