import httpx
import asyncio
from config import DealConfig

class TelegramNotifier:
    def __init__(self):
        self.config = DealConfig()
        self.token = self.config.current_config["telegram_token"]
        self.chat_id = self.config.current_config["chat_id"]
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    async def send_deal_alert(self, product_name, old_price, new_price, discount, link):
        if not self.chat_id:
            return "❌ Error: chat_id not set."
        
        message = (
            f"🚨 *لقطة جديدة من أمازون!* 🚨\n\n"
            f"📦 *المنتج:* {product_name}\n"
            f"💰 *السعر الحالي:* {new_price}\n"
            f"📉 *السعر القديم:* {old_price}\n"
            f"🔥 *نسبة الخصم:* {discount}%\n\n"
            f"🔗 [اضغط هنا للشراء مباشرة]({link})"
        )
        
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, json=payload)
                return "✅ Alert sent!" if response.status_code == 200 else f"❌ Error: {response.text}"
        except Exception as e:
            return f"❌ Connection Error: {e}"
