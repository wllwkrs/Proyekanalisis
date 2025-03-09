import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
df = pd.read_csv('Dashboard/hour_clean.csv')

# Konversi label kategorikal
season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weather_map = {1: "Cerah", 2: "Berawan", 3: "Hujan ringan", 4: "Hujan lebat"}
df["season_label"] = df["season"].map(season_map)
df["weather_label"] = df["weathersit"].map(weather_map)

# Konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("🚴 Bike Sharing Data Dashboard")
st.markdown("#### Proyek Akhir Analisis Data")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")

# Filter Bulan
month_options = ["All"] + sorted(df["mnth"].unique().tolist())
selected_month = st.sidebar.selectbox("Pilih Bulan", month_options)

# Filter Jam
selected_hour = st.sidebar.slider("Pilih Jam", min_value=int(df["hr"].min()), max_value=int(df["hr"].max()), value=int(df["hr"].min()))

# Filter Musim
season_options = ["All"] + df["season_label"].unique().tolist()
selected_season = st.sidebar.selectbox("Pilih Musim", season_options)

# Filter Cuaca
weather_options = ["All"] + df["weather_label"].unique().tolist()
selected_weather = st.sidebar.selectbox("Pilih Cuaca", weather_options)

# Sidebar Statistik
st.sidebar.header("📊 Statistik Data")
st.sidebar.write(f"- **Total Data Points:** {df.shape[0]}")
st.sidebar.write(f"- **Rata-rata Peminjaman Sepeda:** {df['cnt'].mean():.2f}")
st.sidebar.write(f"- **Jam dengan Peminjaman Tertinggi:** {df.groupby('hr')['cnt'].mean().idxmax()}")
st.sidebar.write(f"- **Musim Terbanyak:** {df['season_label'].mode()[0]}")
st.sidebar.write(f"- **Kondisi Cuaca Paling Umum:** {df['weather_label'].mode()[0]}")

# Filter Data
df_filtered = df.copy()
if selected_month != "All":
    df_filtered = df_filtered[df_filtered["mnth"] == int(selected_month)]
if selected_season != "All":
    df_filtered = df_filtered[df_filtered["season_label"] == selected_season]
if selected_weather != "All":
    df_filtered = df_filtered[df_filtered["weather_label"] == selected_weather]
df_filtered = df_filtered[df_filtered["hr"] == selected_hour]

# Layout
col1, col2 = st.columns(2)

# Tren Peminjaman Sepeda
with col1:
    st.subheader("📈 Tren Peminjaman Sepeda")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=df, x="hr", y="cnt", hue="mnth", palette="coolwarm", ax=ax)
    ax.set_title("Peminjaman Sepeda berdasarkan Jam dan Bulan")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Peminjaman")
    st.pyplot(fig)

# Distribusi Peminjaman
with col2:
    st.subheader("📊 Distribusi Peminjaman")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["cnt"], bins=30, kde=True, color="skyblue", ax=ax)
    ax.set_title("Distribusi Peminjaman Sepeda")
    ax.set_xlabel("Jumlah Peminjaman")
    st.pyplot(fig)

# Peminjaman Sepeda Berdasarkan Musim
st.subheader("🌤️ Peminjaman Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=df, x="season_label", y="cnt", palette="Set2", ax=ax)
ax.set_title("Peminjaman Sepeda Berdasarkan Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig)

# Pengaruh Suhu terhadap Peminjaman Sepeda
st.subheader("🌡️ Pengaruh Suhu terhadap Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=df, x="temp_C", y="cnt", hue="weather_label", alpha=0.7, palette="coolwarm", ax=ax)
ax.set_title("Hubungan antara Suhu dan Peminjaman Sepeda")
ax.set_xlabel("Suhu (°C)")
ax.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig)

# Data Tersaring
st.subheader("📋 Data Tersaring")
st.dataframe(df_filtered)
