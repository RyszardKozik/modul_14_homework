import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from config import settings  # Adjust import according to your actual settings variable

def test_example_config():
    assert settings['secret_key'] == 'your_secret_key'
