import asyncio
import re
from playwright.async_api import async_playwright
from config import DealConfig
from agents.notifier.notifier_agent import TelegramNotifier

class ScoutAgent:
    def __init__(self):
        self.config = DealConfig()
        self.min_discount = self.config.current_config.get('min_discount', 60)
        self.smart_threshold = self.config.current_config.get('smart_discount_threshold', 40)
        self.notifier = TelegramNotifier()

    async def scan_amazon_deals(self):
        print(f'🔎 [Scout] Scanning for deals with {self.min_discount}%+ discount...')
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = await context.new_page()
            found_deals = []
            try:
                await page.goto('https://www.amazon.eg/gp/goldbox', timeout=60000)
                await page.wait_for_timeout(5000)
                deal_elements = await page.query_selector_all('[data-testid="grid-deal"], .s-result-item')
                for element in deal_elements:
                    try:
                        name_el = await element.query_selector('.s-line-clamp-1, .a-text-normal')
                        name = await name_el.inner_text() if name_el else 'Unknown Product'
                        text_content = await element.inner_text()
                        discount_match = re.search(r'(\d+)%', text_content)
                        discount = int(discount_match.group(1)) if discount_match else 0
                        price_el = await element.query_selector('.a-price-whole')
                        price = await price_el.inner_text() if price_el else 'N/A'
                        link_el = await element.query_selector('a')
                        link = 'https://www.amazon.eg' + await link_el.get_attribute('href') if link_el else 'N/A'
                        if discount >= self.min_discount:
                            found_deals.append({'product_name': name, 'new_price': price, 'old_price': 'Check Link', 'discount': discount, 'link': link, 'type': '🔥 MEGA DEAL'})
                        elif discount >= self.smart_threshold:
                            found_deals.append({'product_name': name, 'new_price': price, 'old_price': 'Check Link', 'discount': discount, 'link': link, 'type': '✨ SMART DEAL'})
                    except Exception: continue
            except Exception as e:
                print(f'❌ Scanning Error: {e}')
            finally:
                await browser.close()
        return found_deals

    async def process_and_notify(self):
        deals = await self.scan_amazon_deals()
        if not deals:
            return "😴 No interesting deals found."
        
        results = []
        for deal in deals:
            res = await self.notifier.send_deal_alert(
                f"{deal['type']} | {deal['product_name']}", 
                deal['old_price'], 
                deal['new_price'], 
                deal['discount'], 
                deal['link']
            )
            results.append(res)
        return f"✅ Found {len(deals)} deals and notified Telegram."

if __name__ == '__main__':
    scout = ScoutAgent()
    asyncio.run(scout.process_and_notify())
