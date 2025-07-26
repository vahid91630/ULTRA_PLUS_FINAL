
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULTRA_PLUS_BOT - Persian Dashboard
مدیریت کامل سیستم معاملاتی خودکار
"""

import streamlit as st
import sqlite3
import requests
import time
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# تنظیمات صفحه
st.set_page_config(
    page_title="🤖 ULTRA_PLUS_BOT - داشبورد معاملاتی",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS سفارشی برای ظاهر بهتر
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1f4037, #99f2c8);
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 2rem;
}
.metric-box {
    background: #f0f2f6;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #00ff88;
}
</style>
""", unsafe_allow_html=True)

# هدر اصلی
st.markdown("""
<div class="main-header">
    <h1 style="color: white; text-align: center; margin: 0;">
        🤖 ULTRA_PLUS_BOT - داشبورد معاملاتی خودکار
    </h1>
    <p style="color: white; text-align: center; margin: 0;">
        سیستم معاملاتی هوشمند با AI • 24/7 فعال
    </p>
</div>
""", unsafe_allow_html=True)

# دریافت وضعیت سیستم
@st.cache_data(ttl=30)
def get_system_status():
    """دریافت وضعیت سیستم از health reporter"""
    try:
        response = requests.get("http://localhost:8090/health", timeout=5)
        return response.json() if response.status_code == 200 else None
    except:
        return None

@st.cache_data(ttl=60)
def get_trading_data():
    """دریافت داده‌های معاملاتی"""
    try:
        conn = sqlite3.connect('autonomous_trading.db')
        cursor = conn.cursor()
        
        # آخرین معاملات
        cursor.execute('''
            SELECT symbol, action, confidence, reasoning, timestamp
            FROM trading_decisions 
            ORDER BY timestamp DESC LIMIT 5
        ''')
        recent_trades = cursor.fetchall()
        
        # آمار عملکرد
        cursor.execute('''
            SELECT COUNT(*) as total, 
                   SUM(CASE WHEN profit_loss > 0 THEN 1 ELSE 0 END) as wins
            FROM trading_decisions 
            WHERE DATE(timestamp) = DATE('now')
        ''')
        daily_stats = cursor.fetchone()
        
        conn.close()
        return recent_trades, daily_stats
        
    except Exception as e:
        st.error(f"خطا در دریافت داده‌های معاملاتی: {e}")
        return [], (0, 0)

# نمایش وضعیت سیستم
col1, col2, col3, col4 = st.columns(4)

system_status = get_system_status()

with col1:
    if system_status:
        st.metric("🤖 وضعیت کلی", "فعال", "✅")
    else:
        st.metric("🤖 وضعیت کلی", "خطا", "❌")

with col2:
    if system_status and system_status.get('workflows', {}).get('AUTONOMOUS_AI_TRADER', {}).get('status') == 'RUNNING':
        st.metric("💰 معاملگر خودکار", "فعال", "🚀")
    else:
        st.metric("💰 معاملگر خودکار", "غیرفعال", "⏸️")

with col3:
    if system_status:
        portfolio_service = system_status.get('workflows', {}).get('SMART_PORTFOLIO_SERVICE', {})
        if portfolio_service.get('status') == 'RUNNING':
            st.metric("📊 مدیر پورتفولیو", "فعال", "✅")
        else:
            st.metric("📊 مدیر پورتفولیو", "خطا", "❌")
    else:
        st.metric("📊 مدیر پورتفولیو", "نامشخص", "❓")

with col4:
    # محاسبه uptime
    if system_status:
        uptime = system_status.get('uptime_hours', 0)
        st.metric("⏰ مدت فعالیت", f"{uptime:.1f} ساعت", "🕒")
    else:
        st.metric("⏰ مدت فعالیت", "نامشخص", "❓")

# داده‌های معاملاتی
st.subheader("📈 عملکرد معاملاتی امروز")

recent_trades, daily_stats = get_trading_data()
total_trades, wins = daily_stats

col5, col6, col7 = st.columns(3)

with col5:
    st.metric("🎯 تعداد معاملات", total_trades)

with col6:
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    st.metric("🏆 نرخ موفقیت", f"{win_rate:.1f}%")

with col7:
    st.metric("💵 موجودی", "$103.84", "💰")

# آخرین معاملات
if recent_trades:
    st.subheader("📋 آخرین تحلیل‌های AI")
    
    for trade in recent_trades:
        symbol, action, confidence, reasoning, timestamp = trade
        
        # رنگ بر اساس نوع عمل
        color = "🟢" if action == "BUY" else "🔴" if action == "SELL" else "🟡"
        
        with st.expander(f"{color} {symbol} - {action} ({confidence}% اطمینان)"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**زمان:** {timestamp}")
                st.write(f"**اطمینان:** {confidence}%")
            with col_b:
                st.write(f"**تحلیل AI:** {reasoning}")

# نمایش لاگ‌های زنده
st.subheader("📊 فعالیت زنده سیستم")

if st.button("🔄 به‌روزرسانی وضعیت"):
    st.cache_data.clear()
    st.rerun()

# نمایش آمار سیستم تعمیرگاهی
try:
    repair_stats = requests.get("http://localhost:8090/system_stats", timeout=3).json()
    
    st.subheader("🔧 سیستم تعمیرگاهی")
    col8, col9, col10 = st.columns(3)
    
    with col8:
        st.metric("🚨 خطاهای گزارش شده", repair_stats.get('total_errors_reported', 0))
    
    with col9:
        st.metric("✅ چک‌های سلامت", repair_stats.get('total_health_checks', 0))
    
    with col10:
        uptime_repair = repair_stats.get('uptime_hours', 0)
        st.metric("⏰ زمان فعالیت تعمیرگاه", f"{uptime_repair:.2f}h")

except:
    st.info("🔧 سیستم تعمیرگاهی در حال بارگذاری...")

# راهنمای Always On
st.subheader("🚀 راه‌حل Always On")

st.info("""
**برای اینکه سیستم 24/7 کار کند:**

1. **UptimeRobot (رایگان):** 
   - ثبت‌نام در uptimerobot.com
   - Monitor URL: https://[پروژه-شما].replit.app:8080/ping
   - Interval: 5 minutes

2. **Replit Always On ($20/ماه):**
   - به Settings پروژه برید
   - "Always On" را فعال کنید
   - ۱۰۰٪ گارانتی بدون وقفه

3. **وضعیت فعلی:** Keep-Alive فعال - نیاز به UptimeRobot ping
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 12px;">
🤖 ULTRA_PLUS_BOT v2.0 - Autonomous AI Trading System<br>
آخرین به‌روزرسانی: {} | Made with ❤️ in Persian
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)
        