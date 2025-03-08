import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# Load dataset
df = pd.read_csv('/Users/ACER/Submission/Dashboard/hour_clean.csv')

# Dashboard title
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("🚴 Bike Sharing Data Dashboard")
st.markdown("#### Proyek Akhir Analisis Data")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
month = st.sidebar.selectbox("Pilih Bulan", df["mnth"].unique())
hour = st.sidebar.slider("Pilih Jam", min_value=int(df["hr"].min()), max_value=int(df["hr"].max()), value=int(df["hr"].min()))
season = st.sidebar.multiselect("Pilih Musim", df["season"].unique(), default=df["season"].unique())
weather = st.sidebar.multiselect("Pilih Cuaca", df["weathersit"].unique(), default=df["weathersit"].unique())

# Sidebar analysis
st.sidebar.header("📊 Statistik Data")
st.sidebar.write(f"- **Total Data Points:** {df.shape[0]}")
st.sidebar.write(f"- **Rata-rata Peminjaman Sepeda:** {df['cnt'].mean():.2f}")
st.sidebar.write(f"- **Jam dengan Peminjaman Tertinggi:** {df.groupby('hr')['cnt'].mean().idxmax()}")
st.sidebar.write(f"- **Musim Terbanyak:** {df['season'].mode()[0]}")
st.sidebar.write(f"- **Kondisi Cuaca Paling Umum:** {df['weathersit'].mode()[0]}")

# Filtered data
df_filtered = df[(df["mnth"] == month) & (df["hr"] == hour) & (df["season"].isin(season)) & (df["weathersit"].isin(weather))]

# Layout
col1, col2 = st.columns(2)

# Trend of Bike Rentals
with col1:
    st.subheader("📈 Tren Peminjaman Sepeda")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=df, x="hr", y="cnt", hue="mnth", palette="coolwarm", ax=ax)
    ax.set_title("Peminjaman Sepeda berdasarkan Jam dan Bulan")
    st.pyplot(fig)

# Histogram of bike rentals
with col2:
    st.subheader("📊 Distribusi Peminjaman")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["cnt"], bins=30, kde=True, color="skyblue", ax=ax)
    ax.set_title("Distribusi Peminjaman Sepeda")
    st.pyplot(fig)

# Bike Rentals by Season
st.subheader("🌤️ Peminjaman Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=df, x="season", y="cnt", palette="Set2", ax=ax)
ax.set_title("Peminjaman Sepeda Berdasarkan Musim")
st.pyplot(fig)

# Scatter Plot of Temperature vs Bike Rentals
st.subheader("🌡️ Pengaruh Suhu terhadap Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=df, x="temp", y="cnt", hue="weathersit", alpha=0.7, palette="coolwarm", ax=ax)
ax.set_title("Hubungan antara Suhu dan Peminjaman Sepeda")
st.pyplot(fig)

# Filtered Data Table
st.subheader("📋 Data Tersaring")
st.dataframe(df_filtered)