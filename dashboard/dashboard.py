import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

all_df = pd.read_csv("main_data.csv")

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='M', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum",
        "year_group": "last",
        "season_group": "last"
    })
    daily_orders_df.index = daily_orders_df.index.strftime('%B')
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "instant": "data_count",
        "cnt": "total_rental",
        "year_group": "tahun",
        "season_group": "musim"
    }, inplace=True)
    
    return daily_orders_df

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("month_group").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season_group").instant.nunique().reset_index()
    byseason_df.rename(columns={
        "instant": "data_count"
    }, inplace=True)
    byseason_df['season_group'] = pd.Categorical(byseason_df['season_group'], ["Springer", "Fall", "Summer", "Winter"])
    
    return byseason_df

def create_byyear_df(df):
    byyear_df = df.groupby(by="year_group").instant.nunique().reset_index()
    byyear_df.rename(columns={
        "instant": "data_count"
    }, inplace=True)
    byyear_df['year_group'] = pd.Categorical(byyear_df['year_group'], ["2011", "2012"])
    
    return byyear_df

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Membuat Komponen Filter
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://media.istockphoto.com/id/1252019979/id/vektor/ikon-papan-nama-penyewaan-sepeda-padat-konsep-olahraga-luar-ruangan-logo-sepeda-untuk-toko.jpg?s=1024x1024&w=is&k=20&c=KW7WVaYVoBxIN2tADOJ-4frVIH1m_WFSi2D9mddfoOk=")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
byseason_df = create_byseason_df(main_df)
byyear_df = create_byyear_df(main_df)

# Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Rental Sepeda Dashboard :sparkles:')

st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df.data_count.sum()
    st.metric("Total orders", value=total_orders)

with col2:
    total_revenue = daily_orders_df.total_rental.sum() 
    st.metric("Total Rental", value=total_revenue)

st.subheader("Data yg Digunakan")
daily_orders_df

st.subheader("Performa Rental Sepeda Pada Musim Dingin")
fig, ax = plt.subplots(figsize=(16, 8))

season = daily_orders_df[daily_orders_df['musim']=='Winter']
season.set_index('dteday', inplace=True)
season.groupby('tahun')['data_count'].plot(
    marker='o', 
    linewidth=2,
    legend=True,
    title='Performa Rental Sepeda Pada Musim Dingin'
)
# ax.legend(['2011','2012'])
# ax.set_title("Performa Rental Sepeda Pada Musim Dingin", loc="center", fontsize=30)
# ax.tick_params(axis='y', labelsize=20)
# ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader("Performa Rental Sepeda Pada Tahun 2012")
fig, ax = plt.subplots(figsize=(20, 10))

tahunn = daily_orders_df[daily_orders_df['tahun']==2012]
ax.plot(
    tahunn["dteday"],
    tahunn["data_count"],
    marker='o', 
    linewidth=2
)
ax.legend(['2012'])
ax.set_title("Performa Rental Sepeda Pada Tahun 2012", loc="center", fontsize=30)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.caption('Copyright (c) Farizul 2023')

