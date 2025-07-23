import streamlit as st
import pandas as pd
import os

st.title('🏠 Gyeonggi Home Insight')
st.markdown("date: 2024-01-01 ~ 2024-12-31")

current_path = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_path)
file_path = os.path.join(parent_dir, 'data', 'gyeonggi_home_price.csv')

df = pd.read_csv(file_path, encoding='cp949', header=15)
st.write(df.head())
st.write(df.columns)

if '시군구' in df.columns:
    df['시'] = df['시군구'].str.extract(r'(\S+시)', expand=False)

price_col = '보증금(만원)'

if price_col in df.columns:
    df[price_col] = pd.to_numeric(
        df[price_col].astype(str).str.replace(',', ''),
        errors='coerce'
    )
    df.dropna(subset=[price_col], inplace=True)

avg_by_gu = df.groupby('시')[price_col].mean().round(2).reset_index()
avg_by_gu = avg_by_gu.sort_values(by=[price_col], ascending=False).reset_index(drop=True)

st.markdown("🪙 Avg Price per District")
st.dataframe(avg_by_gu)