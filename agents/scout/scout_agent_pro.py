import asyncio
import re
import random
from playwright.async_api import async_playwright
from config import DealConfig
from agents.notifier.notifier_agent import TelegramNotifier

class ScoutAgent:
    def __init__(self):
        self.config = DealConfig()
        self.min_discount = self.config.current_config.get('min_discount', 60)
        self.smart_threshold = self.config.current_config.get('smart_discount_threshold', 40)
        self.notifier = TelegramNotifier()
        self.categories = self.config.current_config.get('target_categories', ['Electronics'])

    async def _get_random_delay(self, min_s=2, max_s=5):
        await asyncio.sleep(random.uniform(min_s, max_s))

    async def scan_amazon_deals(self):
        print(f'🔎 [Pro-Scout] Hunting in categories: {self.categories}...')
        found_deals = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            )
            page = await context.new_page()
            
            search_urls = ['https://www.amazon.eg/gp/goldbox']
            for cat in self.categories:
                search_urls.append(f'https://www.amazon.eg/s?k={cat}')

            for url in search_urls:
                try:
                    print(f'Scanning {url}...')
                    await page.goto(url, timeout=60000, wait_until='domcontentloaded')
                    await self._get_random_delay()
                    
                    deal_elements = await page.query_selector_all('[data-component-type="s-search-result"], [data-testid="grid-deal"], .s-result-item')
                    
                    for element in deal_elements:
                        try:
                            name_el = await element.query_selector('.s-line-clamp-1, .a-text-normal, h2 span')
                            name = await name_el.inner_text() if name_el else 'Unknown Product'
                            
                            price_whole_el = await element.query_selector('.a-price-whole')
                            price = await price_whole_el.inner_text() if price_whole_el else 'N/A'
                            
                            text_content = await element.inner_text()
                            discount_match = re.search(r'(\d+)%', text_content)
                            discount = int(discount_match.group(1)) if discount_match else 0
                            
                            link_el = await element.query_selector('a')
                            href = await link_el.get_attribute('href') if link_el else ''
                            link = 'https://www.amazon.eg' + href if href.startswith('/') else href
                            
                            if discount >= self.min_discount:
                                found_deals.append({
                                    'product_name': name, 'new_price': price, 
                                    'old_price': 'Check Link', 'discount': discount, 
                                    'link': link, 'type': '🔥 MEGA DEAL'
                                })
                            elif discount >= self.smart_threshold:
                                found_deals.append({
                                    'product_name': name, 'new_price': price, 
                                    'old_price': 'Check Link', 'discount': discount, 
                                    'link': link, 'type': '✨ SMART DEAL'
                                })
                            await self._get_random_delay(0.1, 0.5)
                        except Exception: continue
                except Exception as e:
                    print(f'❌ Error scanning {url}: {e}')
            
            await browser.close()
        return found_deals

    async def process_and_notify(self):
        deals = await self.scan_amazon_deals()
        if not deals:
            return "😴 No interesting deals found."
        
        seen_links = set()
        unique_deals = []
        for d in deals:
            if d['link'] not in seen_links:
                unique_deals.append(d)
                seen_links.add(d['link'])

        results = []
        for deal in unique_deals:
            res = await self.notifier.send_deal_alert(
                f"{deal['type']} | {deal['product_name']}", 
                deal['old_price'], 
                deal['new_//price'], 
                deal['discount'], 
                deal['link']
            )
            results.append(res)
        return f"✅ Found {len(unique_deals)} unique deals and notified Telegram."

if __name__ == '__main__':
    import asyncio
    scout = ScoutAgent()
    asyncio.run(scout.process_and_notify())
