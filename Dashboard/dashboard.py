import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

df = pd.read_csv('./hour_cleaned.csv')


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

# 1. Pengaruh Kondisi Cuaca terhadap Peminjaman Sepeda
st.subheader("🌤️ Pengaruh Kondisi Cuaca terhadap Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(8, 5))
order = ["Cerah", "Berawan", "Hujan ringan", "Hujan lebat"]
sns.barplot(x="weather_label", y="cnt", data=df, palette="viridis", estimator=sum, ci=None, order=order)
ax.set_title("Distribusi Peminjaman Sepeda Berdasarkan Kondisi Cuaca")
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Jumlah Peminjaman")
plt.xticks(rotation=20)
st.pyplot(fig)

# 2. Tren Peminjaman Sepeda dari Tahun 2011 ke 2012
st.subheader("📈 Tren Peminjaman Sepeda per Bulan (2011 vs 2012)")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x="mnth", y="cnt", hue="yr", data=df, ci=None, marker="o", palette="muted")
ax.set_title("Tren Peminjaman Sepeda per Bulan (2011 vs 2012)")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Peminjaman")
plt.xticks(ticks=range(1, 13), labels=["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
ax.legend(title="Tahun", labels=["2011", "2012"])
st.pyplot(fig)

# 3. Pola Peminjaman Sepeda Berdasarkan Waktu
st.subheader("🕒 Pola Peminjaman Sepeda Berdasarkan Jam")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x="hr", y="cnt", data=df, ci=None, marker="o", color="b")
ax.set_title("Pola Peminjaman Sepeda Berdasarkan Jam")
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Peminjaman")
plt.xticks(ticks=range(0, 24))
st.pyplot(fig)

# Data Tersaring
st.subheader("📋 Data Tersaring")
st.dataframe(df_filtered)
