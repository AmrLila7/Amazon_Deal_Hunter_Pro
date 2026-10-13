import httpx
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import DealConfig

class TelegramNotifier:
    def __init__(self):
        self.config = DealConfig()
        self.token = self.config.current_config.get("telegram_token")
        self.chat_id = self.config.current_config.get("chat_id")
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage" if self.token else None

    async def send_deal_alert(self, product_name, old_price, new_price, discount, link):
        if not self.token or not self.chat_id:
            return "❌ Telegram not configured."
        
        message = (
            f"🚨 *لقطة جديدة من أمازون!* 🚨\n\n"
            f"📦 *المنتج:* {product_name}\n"
            f"💰 *السعر الحالي:* {new_price}\n"
            f"📉 *السعر القديم:* {old_price}\n"
            f"🔥 *نسبة الخصم:* {discount}%\n\n"
            f"🔗 [اضغط هنا للشراء مباشرة]({link})"
        )
        
        payload = {"chat_id": self.chat_id, "text": message, "parse_mode": "Markdown"}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, json=payload)
                return "✅ Telegram Alert sent!" if response.status_code == 200 else f"❌ Telegram Error: {response.text}"
        except Exception as e:
            return f"❌ Telegram Connection Error: {e}"

class EmailNotifier:
    def __init__(self):
        self.config = DealConfig()
        self.user = self.config.current_config.get("email_user")
        self.password = self.config.current_config.get("email_pass")
        self.receiver = self.config.current_//config.get("email_receiver")

    async def send_deal_alert(self, product_name, old_price, new_price, discount, link):
        if not self.user or not self.password or not self.receiver:
            return "❌ Email not configured."
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.user
            msg['To'] = self.receiver
            msg['Subject'] = f"🔥 Mega Deal: {product_name} ({discount}%)"
            
            body = f"لقد وجد البوت صفقة رائعة!\n\nالمنتج: {product_name}\nالسعر الحالي: {new_price}\nالخصم: {discount}%\n\nرابط الشراء: {link}"
            msg.attach(MIMEText(body, 'plain'))
            
            def send():
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login(self.user, self.password)
                    server.send_message(msg)
            
            await asyncio.to_thread(send)
            return "✅ Email Alert sent!"
        except Exception as e:
            return f"❌ Email Error: {e}"

class NotificationManager:
    def __init__(self):
        self.telegram = TelegramNotifier()
        self.email = EmailNotifier()

    async def notify_all(self, product_name, old_price, new_price, discount, link):
        t_res = await self.telegram.send_deal_alert(product_name, old_//price, new_price, discount, link)
        e_res = await self.email.send_//deal_alert(product_name, old_//price, new_price, discount, link)
        return f"Telegram: {t_res} | Email: {e_res}"
