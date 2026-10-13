
import unittest
import asyncio
import os
import sys

# Add project root to sys.path to import project modules
sys.path.append('C:/Users/amrli/Desktop/Extra Work/Amazon_Deal_Hunter_Pro')

from tests.test_config import test_config_defaults, test_config_update

async def run_tests():
    print("🚀 Running Internal Production Tests...")
    
    # Test Config Defaults
    try:
        test_config_defaults()
        print("✅ test_config_defaults: PASSED")
    except Exception as e:
        print(f"❌ test_config_defaults: FAILED ({e})")
        
    # Test Config Update
    try:
        test_config_update()
        print("✅ test_config_update: PASSED")
    except Exception as e:
        print(f"❌ test_config_update: FAILED ({e})")

if __name__ == '__main__':
    asyncio.run(run_tests())
