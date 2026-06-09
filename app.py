# app.py
import streamlit as st
from logic import clean_data, detect_anomalies
from visuals import set_pwa_styles, draw_kpi, plot_main_donut

st.set_page_config(page_title="LedgerLens", layout="wide")
set_pwa_styles()

st.sidebar.title("💎 LedgerLens")
uploaded_file = st.sidebar.file_uploader("📂 آپلود اکسل", type=['xlsx'])

if uploaded_file:
    df = clean_data(uploaded_file)
    if df is not None:
        # ۱. تحلیل هوشمند (نوآوری)
        anomalies = detect_anomalies(df)
        if not anomalies.empty:
            st.warning(f"⚠️ {len(anomalies)} مخارج مشکوک و سنگین شناسایی شد!")
            with st.expander("مشاهده لیست"):
                st.table(anomalies[['تاریخ', 'کلاس', 'برداشت (ریال)']])

        # ۲. نمایش شاخص‌ها (KPIs)
        t_inc = df['واریز (ریال)'].sum()
        t_exp = df['برداشت (ریال)'].sum()
        c1, c2, c3 = st.columns(3)
        with c1: draw_kpi("درآمد کل", t_inc, "#2ecc71")
        with c2: draw_kpi("هزینه کل", t_exp, "#e74c3c")
        with c3: draw_kpi("تراز", (t_inc - t_exp), "#3498db")

        # ۳. نمودار اصلی
        st.plotly_chart(plot_main_donut(df, t_inc), use_container_width=True)

        # ۴. تب‌ها (بخش لیست تراکنش‌ها که خواسته بودی ساده باشه)
        t1, t2, t3 = st.tabs(["👤 شخصی", "🏭 کارگاه", "📋 لیست کل"])
        with t1:
            st.dataframe(df[df['مرکز'] == 'شخصی'].style.format("{:,.0f}"), use_container_width=True)
        with t2:
            st.dataframe(df[df['مرکز'] == 'کارگاه'].style.format("{:,.0f}"), use_container_width=True)
        with t3:
            st.dataframe(df.style.format("{:,.0f}"), use_container_width=True)
else:
    st.info("حاجی فایل رو آپلود کن تا اپلیکیشن گوشی‌ت فعال بشه!")