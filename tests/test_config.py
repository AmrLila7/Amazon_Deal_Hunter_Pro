import pytest
import os
import json
from config import DealConfig

def test_config_defaults():
    config = DealConfig()
    assert config.current_config['min_discount'] == 60
    assert 'telegram_token' in config.current_config

def test_config_update():
    config = DealConfig()
    config.update_config('min_discount', 50)
    assert config.current_config['min_discount'] == 50
    
    # Verify it's saved to disk
    with open(config.config_path, 'r') as f:
        saved_config = json.load(f)
        assert saved_config['min_discount'] == 50
