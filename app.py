import streamlit as st
import asyncio
import pandas as pd
from config import DealConfig
from agents.scout.scout_agent_pro import ScoutAgent

st.set_page_config(page_title="Amazon Deal Hunter Pro", page_icon="🛍️", layout="wide")

st.markdown('''
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #FF9900; color: white; font-weight: bold; }
    </style>
    ''', unsafe_allow_html=True)

config = DealConfig()

st.sidebar.header("⚙️ Pro Hunter Settings")
st.sidebar.markdown("---")

min_discount = st.sidebar.slider("Min Discount (%)", 10, 99, config.current_config.get("min_discount", 60))
if st.sidebar.button("Update Discount"):
    config.update_config("min_discount", min_discount)
    st.sidebar.success("Updated!")

categories_str = ",".join(config.current_config.get("target_categories", []))
new_categories = st.sidebar.text_input("Categories", categories_str)
if st.sidebar.button("Update Categories"):
    config.update_config("target_categories", [c.strip() for c in new_categories.split(",")])
    st.sidebar.success("Updated!")

st.title("🛍️ Amazon Deal Hunter Pro Dashboard")
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎯 Current Scan Results")
    if st.button("🚀 Start Professional Scan"):
        with st.spinner("The Ultimate Scout is hunting..."):
            scout = ScoutAgent()
            scout.min_discount = min_discount
            scout.smart_threshold = min_discount - 20
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            deals = loop.run_until_complete(scout.scan_amazon_deals())
            
            if deals:
                st.success(f"Found {len(deals)} high-value deals!")
                st.table(pd.DataFrame(deals)[['product_name', 'new_price', 'discount', 'type']])
                loop.run_until_complete(scout.process_and_notify())
            else:
                st.info("No deals found in this run. 😴")

with col2:
    st.subheader("📡 System Status")
    st.write(f"**Chat ID:** `{config.current_config['chat_id']}`")
    st.info("Auto-Pilot active via .bat file.")

st.markdown("---")
st.caption("Hybrid Engine: Playwright Power + Pro-Bot Architecture")
