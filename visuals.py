# visuals.py
import streamlit as st
import plotly.express as px

def set_pwa_styles():
    """تنظیمات مخصوص برای تبدیل شدن به اپلیکیشن موبایل"""
    st.markdown("""
    <head>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    </head>
    <style>
        @import url('https://v1.fontapi.ir/css/Vazir');
        * { direction: rtl; font-family: 'Vazir', sans-serif; }
        .kpi-card {
            background: white; padding: 15px; border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05); text-align: center;
            border-right: 5px solid #0068c9; margin-bottom: 10px;
        }
        .stMetric { background: #f8f9fa; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

def draw_kpi(label, value, color="#0068c9"):
    st.markdown(f"""
        <div class="kpi-card" style="border-right-color: {color};">
            <div style="color: #666; font-size: 13px;">{label}</div>
            <div style="font-size: 20px; font-weight: bold;">{value:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

def plot_main_donut(df, total_inc):
    p_exp = df[df['مرکز'] == 'شخصی']['برداشت (ریال)'].sum()
    w_exp = df[df['مرکز'] == 'کارگاه']['برداشت (ریال)'].sum()
    fig = px.pie(names=['درآمد', 'هزینه کارگاه', 'هزینه شخصی'], 
                 values=[total_inc, w_exp, p_exp], hole=0.5,
                 color_discrete_sequence=['#2ecc71', '#e74c3c', '#f39c12'])
    fig.update_layout(margin=dict(t=20, b=20, l=0, r=0), height=300)
    return fig