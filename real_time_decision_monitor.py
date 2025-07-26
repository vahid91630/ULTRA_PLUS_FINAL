"""
📊 Real-Time Decision Monitor - نظارت لحظه‌ای تصمیمات
نمایش زنده و نظارت بر تصمیمات هوشمند سیستم

Created for Vahid (وحید) - Advanced Decision Monitoring
"""

import asyncio
import logging
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

from advanced_decision_engine import AdvancedDecisionEngine, MarketDecision, get_smart_decisions
from enhanced_income_strategies import EnhancedIncomeStrategies
from advanced_risk_manager import AdvancedRiskManager

logger = logging.getLogger(__name__)

class RealTimeDecisionMonitor:
    """نظارت لحظه‌ای بر تصمیمات هوشمند"""
    
    def __init__(self):
        self.decision_engine = AdvancedDecisionEngine()
        self.income_strategies = EnhancedIncomeStrategies()
        self.risk_manager = AdvancedRiskManager()
        
        # ذخیره تصمیمات
        self.decision_history = []
        self.performance_metrics = {}
        self.live_decisions = []
        
        # تنظیمات نمایش
        self.max_history = 100
        self.refresh_interval = 10  # ثانیه
        
        logger.info("📊 Real-Time Decision Monitor initialized")
    
    async def get_live_decisions(self) -> Dict:
        """دریافت تصمیمات زنده"""
        try:
            # دریافت فرصت‌های جدید
            arbitrage_opps = await self.income_strategies.analyze_crypto_arbitrage()
            forex_signals = await self.income_strategies.analyze_forex_trends()
            
            # ترکیب فرصت‌ها
            all_opportunities = arbitrage_opps + forex_signals
            
            if not all_opportunities:
                return {
                    'decisions': [],
                    'summary': {'total_decisions': 0},
                    'timestamp': datetime.now()
                }
            
            # تحلیل و تصمیم‌گیری
            decisions, summary = await get_smart_decisions({}, all_opportunities)
            
            # ذخیره در تاریخچه
            self.decision_history.extend(decisions)
            if len(self.decision_history) > self.max_history:
                self.decision_history = self.decision_history[-self.max_history:]
            
            # به‌روزرسانی آمار عملکرد
            self._update_performance_metrics(decisions)
            
            return {
                'decisions': decisions,
                'summary': summary,
                'performance': self.performance_metrics,
                'opportunities': all_opportunities,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"❌ خطا در دریافت تصمیمات زنده: {e}")
            return {
                'decisions': [],
                'summary': {'total_decisions': 0},
                'error': str(e),
                'timestamp': datetime.now()
            }
    
    def _update_performance_metrics(self, decisions: List[MarketDecision]):
        """به‌روزرسانی آمار عملکرد"""
        if not decisions:
            return
        
        # آمار اعتماد
        confidences = [d.confidence for d in decisions]
        success_probs = [d.success_probability for d in decisions]
        
        # آمار اکشن‌ها
        actions = {}
        for decision in decisions:
            actions[decision.action] = actions.get(decision.action, 0) + 1
        
        # آمار ریسک
        risk_levels = {}
        for decision in decisions:
            risk_levels[decision.risk_level] = risk_levels.get(decision.risk_level, 0) + 1
        
        self.performance_metrics = {
            'avg_confidence': np.mean(confidences),
            'avg_success_probability': np.mean(success_probs),
            'max_confidence': max(confidences),
            'min_confidence': min(confidences),
            'high_confidence_ratio': len([c for c in confidences if c > 0.8]) / len(confidences),
            'actions_distribution': actions,
            'risk_distribution': risk_levels,
            'total_decisions_today': len(self.decision_history),
            'last_update': datetime.now().isoformat()
        }
    
    def create_confidence_chart(self, decisions: List[MarketDecision]) -> go.Figure:
        """نمودار اعتماد تصمیمات"""
        if not decisions:
            fig = go.Figure()
            fig.add_annotation(text="هیچ تصمیمی موجود نیست", 
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        # داده‌های نمودار
        assets = [d.asset for d in decisions]
        confidences = [d.confidence * 100 for d in decisions]  # تبدیل به درصد
        success_probs = [d.success_probability * 100 for d in decisions]
        actions = [d.action for d in decisions]
        
        # رنگ‌بندی بر اساس اکشن
        colors = {
            'BUY': '#00ff00',    # سبز
            'SELL': '#ff4444',   # قرمز
            'HOLD': '#ffa500',   # نارنجی
            'WAIT': '#888888'    # خاکستری
        }
        
        fig = go.Figure()
        
        # اضافه کردن نقاط
        for i, (asset, conf, prob, action) in enumerate(zip(assets, confidences, success_probs, actions)):
            fig.add_trace(go.Scatter(
                x=[conf],
                y=[prob],
                mode='markers+text',
                marker=dict(
                    size=15,
                    color=colors.get(action, '#888888'),
                    line=dict(width=2, color='black')
                ),
                text=[asset],
                textposition="top center",
                name=f"{action}: {asset}",
                hovertemplate=f"<b>{asset}</b><br>" +
                            f"اعتماد: {conf:.1f}%<br>" +
                            f"احتمال موفقیت: {prob:.1f}%<br>" +
                            f"اکشن: {action}<extra></extra>"
            ))
        
        fig.update_layout(
            title="نمودار اعتماد و احتمال موفقیت تصمیمات",
            xaxis_title="درصد اعتماد",
            yaxis_title="احتمال موفقیت (%)",
            showlegend=True,
            height=400,
            font=dict(size=12)
        )
        
        # اضافه کردن خطوط راهنما
        fig.add_hline(y=75, line_dash="dash", line_color="green", 
                     annotation_text="آستانه موفقیت بالا")
        fig.add_vline(x=80, line_dash="dash", line_color="blue", 
                     annotation_text="آستانه اعتماد بالا")
        
        return fig
    
    def create_performance_gauge(self, metrics: Dict) -> go.Figure:
        """گیج عملکرد کلی"""
        if not metrics:
            overall_score = 0
        else:
            # محاسبه امتیاز کلی
            conf_score = metrics.get('avg_confidence', 0) * 100
            success_score = metrics.get('avg_success_probability', 0) * 100
            high_conf_bonus = metrics.get('high_confidence_ratio', 0) * 20
            
            overall_score = (conf_score + success_score + high_conf_bonus) / 2.2
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = overall_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "امتیاز عملکرد کلی"},
            delta = {'reference': 75, 'position': "top"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 75], 'color': "yellow"},
                    {'range': [75, 90], 'color': "lightgreen"},
                    {'range': [90, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 85
                }
            }
        ))
        
        fig.update_layout(height=300, font=dict(size=14))
        return fig
    
    def create_decisions_timeline(self, decisions: List[MarketDecision]) -> go.Figure:
        """خط زمانی تصمیمات"""
        if not decisions:
            fig = go.Figure()
            fig.add_annotation(text="هیچ تصمیمی موجود نیست", 
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        # مرتب‌سازی بر اساس زمان
        sorted_decisions = sorted(decisions, key=lambda x: x.decision_timestamp)
        
        timestamps = [d.decision_timestamp for d in sorted_decisions]
        confidences = [d.confidence * 100 for d in sorted_decisions]
        assets = [d.asset for d in sorted_decisions]
        actions = [d.action for d in sorted_decisions]
        
        # رنگ‌بندی
        colors = ['green' if a == 'BUY' else 'red' if a == 'SELL' else 'orange' 
                 for a in actions]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=confidences,
            mode='lines+markers',
            marker=dict(size=10, color=colors),
            line=dict(width=2),
            text=[f"{asset}: {action}" for asset, action in zip(assets, actions)],
            hovertemplate="<b>%{text}</b><br>" +
                        "زمان: %{x}<br>" +
                        "اعتماد: %{y:.1f}%<extra></extra>"
        ))
        
        fig.update_layout(
            title="خط زمانی تصمیمات",
            xaxis_title="زمان",
            yaxis_title="درصد اعتماد",
            height=300,
            showlegend=False
        )
        
        return fig
    
    def create_risk_distribution(self, decisions: List[MarketDecision]) -> go.Figure:
        """توزیع سطوح ریسک"""
        if not decisions:
            fig = go.Figure()
            fig.add_annotation(text="هیچ تصمیمی موجود نیست", 
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        risk_counts = {}
        for decision in decisions:
            risk_counts[decision.risk_level] = risk_counts.get(decision.risk_level, 0) + 1
        
        colors = {'LOW': '#00ff00', 'MEDIUM': '#ffa500', 'HIGH': '#ff4444'}
        
        fig = go.Figure(data=[
            go.Pie(
                labels=list(risk_counts.keys()),
                values=list(risk_counts.values()),
                marker_colors=[colors.get(risk, '#888888') for risk in risk_counts.keys()],
                textinfo='label+percent',
                hovertemplate="<b>%{label}</b><br>" +
                            "تعداد: %{value}<br>" +
                            "درصد: %{percent}<extra></extra>"
            )
        ])
        
        fig.update_layout(
            title="توزیع سطوح ریسک",
            height=300
        )
        
        return fig

# تابع اصلی برای نمایش در Streamlit
def show_decision_monitor():
    """نمایش نظارت تصمیمات در Streamlit"""
    st.set_page_config(
        page_title="🧠 نظارت تصمیمات هوشمند",
        page_icon="🧠",
        layout="wide"
    )
    
    # عنوان اصلی
    st.title("🧠 نظارت لحظه‌ای تصمیمات هوشمند")
    st.markdown("### سیستم تحلیل و تصمیم‌گیری پیشرفته")
    
    # ایجاد monitor
    if 'decision_monitor' not in st.session_state:
        st.session_state.decision_monitor = RealTimeDecisionMonitor()
    
    monitor = st.session_state.decision_monitor
    
    # بخش کنترل
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("🔄 تازه‌سازی تصمیمات", type="primary"):
            with st.spinner("در حال تحلیل و تصمیم‌گیری..."):
                st.session_state.live_data = asyncio.run(monitor.get_live_decisions())
    
    with col2:
        auto_refresh = st.checkbox("تازه‌سازی خودکار", value=True)
    
    with col3:
        st.metric("آخرین بروزرسانی", 
                 datetime.now().strftime("%H:%M:%S"))
    
    # دریافت داده‌های زنده
    if 'live_data' not in st.session_state or auto_refresh:
        with st.spinner("در حال دریافت تصمیمات..."):
            st.session_state.live_data = asyncio.run(monitor.get_live_decisions())
    
    live_data = st.session_state.live_data
    
    # نمایش خطا در صورت وجود
    if 'error' in live_data:
        st.error(f"❌ خطا: {live_data['error']}")
        return
    
    decisions = live_data.get('decisions', [])
    summary = live_data.get('summary', {})
    performance = live_data.get('performance', {})
    
    # آمار کلی
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("تعداد تصمیمات", summary.get('total_decisions', 0))
    
    with col2:
        avg_conf = performance.get('avg_confidence', 0) * 100
        st.metric("میانگین اعتماد", f"{avg_conf:.1f}%")
    
    with col3:
        avg_success = performance.get('avg_success_probability', 0) * 100
        st.metric("میانگین احتمال موفقیت", f"{avg_success:.1f}%")
    
    with col4:
        high_conf_ratio = performance.get('high_confidence_ratio', 0) * 100
        st.metric("تصمیمات پراعتماد", f"{high_conf_ratio:.1f}%")
    
    # نمودارها
    if decisions:
        st.markdown("---")
        
        # ردیف اول نمودارها
        col1, col2 = st.columns(2)
        
        with col1:
            confidence_chart = monitor.create_confidence_chart(decisions)
            st.plotly_chart(confidence_chart, use_container_width=True)
        
        with col2:
            performance_gauge = monitor.create_performance_gauge(performance)
            st.plotly_chart(performance_gauge, use_container_width=True)
        
        # ردیف دوم نمودارها
        col1, col2 = st.columns(2)
        
        with col1:
            timeline_chart = monitor.create_decisions_timeline(decisions)
            st.plotly_chart(timeline_chart, use_container_width=True)
        
        with col2:
            risk_chart = monitor.create_risk_distribution(decisions)
            st.plotly_chart(risk_chart, use_container_width=True)
        
        # جدول تصمیمات
        st.markdown("---")
        st.subheader("📋 جزئیات تصمیمات")
        
        decisions_data = []
        for decision in decisions:
            decisions_data.append({
                'دارایی': decision.asset,
                'اکشن': decision.action,
                'اعتماد': f"{decision.confidence:.2%}",
                'احتمال موفقیت': f"{decision.success_probability:.2%}",
                'ریسک': decision.risk_level,
                'هدف سود': f"{decision.profit_target:.2f}%",
                'فوریت': decision.execution_urgency,
                'زمان': decision.decision_timestamp.strftime("%H:%M:%S")
            })
        
        if decisions_data:
            df = pd.DataFrame(decisions_data)
            st.dataframe(df, use_container_width=True)
        
        # جزئیات تصمیم برتر
        if decisions:
            st.markdown("---")
            st.subheader("⭐ تصمیم برتر")
            
            top_decision = decisions[0]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info(f"""
                **دارایی:** {top_decision.asset}  
                **اکشن:** {top_decision.action}  
                **اعتماد:** {top_decision.confidence:.2%}
                """)
            
            with col2:
                st.success(f"""
                **احتمال موفقیت:** {top_decision.success_probability:.2%}  
                **هدف سود:** {top_decision.profit_target:.2f}%  
                **ریسک:** {top_decision.risk_level}
                """)
            
            with col3:
                st.warning(f"""
                **سایز پوزیشن:** {top_decision.position_size:.2%}  
                **فوریت اجرا:** {top_decision.execution_urgency}  
                **مدت زمان:** {top_decision.expected_duration}
                """)
            
            # دلایل تصمیم
            if top_decision.reasoning:
                st.markdown("**دلایل تصمیم:**")
                for reason in top_decision.reasoning:
                    st.write(f"• {reason}")
    
    else:
        st.info("🔍 در انتظار تصمیمات جدید...")
        st.markdown("سیستم در حال تحلیل بازار و شناسایی فرصت‌های معاملاتی است.")
    
    # تنظیمات
    with st.expander("⚙️ تنظیمات پیشرفته"):
        st.slider("حداکثر تاریخچه تصمیمات", 50, 200, monitor.max_history)
        st.slider("فاصله تازه‌سازی (ثانیه)", 5, 60, monitor.refresh_interval)
        
        if st.button("پاک کردن تاریخچه"):
            monitor.decision_history.clear()
            st.success("تاریخچه پاک شد!")
    
    # تازه‌سازی خودکار
    if auto_refresh:
        time.sleep(monitor.refresh_interval)
        st.rerun()

if __name__ == "__main__":
    show_decision_monitor()