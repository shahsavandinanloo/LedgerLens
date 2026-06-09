# logic.py
import pandas as pd
import streamlit as st

def clean_data(file):
    """پاکسازی و استخراج تگ‌ها از فایل اکسل"""
    try:
        df = pd.read_excel(file, header=3)
        df = df.dropna(subset=['تاریخ'], how='all')

        # ۱. نرمال‌سازی تاریخ و مبالغ
        df['تاریخ'] = df['تاریخ'].apply(lambda x: str(x).split(' ')[0].replace('-', '/'))
        for col in ['واریز (ریال)', 'برداشت (ریال)']:
            df[col] = df[col].apply(lambda x: int(str(x).replace(',', '').strip()) if pd.notna(x) and x != '-' else 0)

        # ۲. شکستن تگ‌ها (ماهیت/مرکز/کلاس/جزئیات/تکمیلی)
        tags = df['توضیحات کاربر'].str.strip('/').str.split('/', expand=True).iloc[:, :5]
        tags.columns = ['ماهیت', 'مرکز', 'کلاس', 'جزئیات', 'تکمیلی']
        df = pd.concat([df, tags.fillna('-')], axis=1)
        df['مرکز'] = df['مرکز'].str.strip()
        
        return df.sort_values('تاریخ')
    except Exception as e:
        st.error(f"خطا در ساختار فایل: {e}")
        return None

def detect_anomalies(df):
    """نوآوری: شناسایی مخارجی که به طور غیرعادی زیاد هستند"""
    exp_df = df[df['برداشت (ریال)'] > 0]
    if exp_df.empty: return pd.DataFrame()
    
    # فرمول آماری: میانگین + ۲ برابر انحراف معیار
    threshold = exp_df['برداشت (ریال)'].mean() + (2 * exp_df['برداشت (ریال)'].std())
    return exp_df[exp_df['برداشت (ریال)'] > threshold]