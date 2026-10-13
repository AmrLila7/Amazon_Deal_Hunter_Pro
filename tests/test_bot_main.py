
import pytest
from unittest.mock import MagicMock, patch
import os

# Import the run function from the bot's main module
# Since it's in __main__.py, we might need to handle the import carefully
import sys
import importlib.util

# Dynamically load the __main__.py module as 'bot_main'
spec = importlib.util.spec_from_file_location("bot_main", "C:/Users/amrli/Desktop/Extra Work/Amazon_Deal_Hunter_Pro/amazon-deals-telegram-bot/__main__.py")
bot_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bot_main)

@patch('bot_main.telegram.Bot')
@patch('bot_main.retrieve_deals')
@patch('bot_main.get_random_product_info')
def test_run_handles_no_products_found(mock_get_product, mock_retrieve, mock_bot):
    """
    RED: Verify that if get_random_product_info returns None, 
    the run() function handles it without raising a TypeError.
    """
    # Setup
    mock_retrieve.return_value = {
        "collection_time": 123456789,
        "deals_ids": ["id1", "id2"],
        "already_sent_product_ids": []
    }
    # Simulate the failure: get_random_product_info returns None
    mock_get_product.return_value = None
    
    # This should NOT raise TypeError: cannot unpack non-iterable NoneType object
    bot_main.run()

@patch('bot_main.telegram.Bot')
@patch('bot_main.retrieve_deals')
@patch('bot_main.get_random_product_info')
@patch('bot_main.send_deal')
def test_run_handles_missing_chat_id(mock_send, mock_get_product, mock_retrieve, mock_bot):
    """
    RED: Verify that if AMAZON_DEALS_TG_CHANNEL_ID is missing,
    the bot doesn't crash and handles it gracefully.
    """
    # Setup
    mock_retrieve.return_value = {
        "collection_time": 123456789,
        "deals_ids": ["id1"],
        "already_sent_product_ids": []
    }
    mock_get_product.return_value = ({"product_id": "id1"}, [])
    
    # Clear the chat id from environment
    with patch.dict(os.environ, {}, clear=True):
        bot_main.run()
        # send_deal should not be called if chat_id is missing
        mock_send.assert_not_called()
