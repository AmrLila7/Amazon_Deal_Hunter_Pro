import asyncio
import time
from config import DealConfig
from agents.scout.scout_agent_pro import ScoutAgent

async def main():
    config = DealConfig()
    scout = ScoutAgent()
    
    print("🚀 Amazon Deal Hunter Pro is now running in Background Mode...")
    print(f"⏱️ Scan Interval: {config.current_config.get('scan_interval_minutes', 15)} minutes")
    print("Press Ctrl+C to stop the bot.\n")

    while True:
        try:
            print(f"[{time.strftime('%H:%M:%S')}] Starting a new scan...")
            result = await scout.process_and_notify()
            print(f"Result: {result}")
        except Exception as e:
            print(f"❌ Critical Error in background loop: {e}")
        
        interval = config.current_config.get('scan_interval_minutes', 15) * 60
        await asyncio.sleep(interval)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user.")
