import os
import json
from dotenv import load_dotenv

load_dotenv()

class DealConfig:
    def __init__(self):
        self.config_path = 'C:/Users/amrli/Desktop/Extra Work/Amazon_Deal_Hunter_Pro/config.json'
        self.defaults = {
            'telegram_token': os.getenv('TELEGRAM_TOKEN', ''),
            'chat_id': os.getenv('TELEGRAM_CHAT_ID', ''),
            'min_discount': 60,
            'smart_discount_threshold': 40,
            'target_categories': ['Electronics', 'Home Appliances', 'Kitchen'],
            'scan_interval_minutes': 15,
            'email_user': os.getenv('EMAIL_USER', ''),
            'email_pass': os.getenv('EMAIL_PASS', ''),
            'email_receiver': os.getenv('EMAIL_RECEIVER', ''),
            'dynamic_thresholds': [
                {'min_price': 1000, 'discount': 20},  # High value: 20% is enough
                {'min_price': 500, 'discount': 30},   # Mid value: 30%
                {'min_price': 0, 'discount': 60}      # Low value: 60%
            ]
        }
        self.load_or_create_config()

    def load_or_create_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.current_config = json.load(f)
        else:
            self.current_config = self.defaults
            self.save_config()

    def save_config(self):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.current_config, f, indent=4)

    def update_config(self, key, value):
        self.current_config[key] = value
        self.save_config()

if __name__ == '__main__':
    conf = DealConfig()
    print('Config initialized.')
