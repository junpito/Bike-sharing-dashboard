import streamlit as st
import pandas as pd
import math
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Bike Sharing: dashboard ',
    page_icon=':bike:', # This is an emoji shortcode. Could be a URL too.r
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

#@st.cache_data
def load_data():
    df = pd.read_csv('/workspaces/gdp-dashboard/data/hour.csv')
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# Fungsi untuk memetakan musim
def map_season(season):
    return {
        'Musim Semi': 1,
        'Musim Panas': 2,
        'Musim Gugur': 3,
        'Musim Dingin': 4
    }[season]



# Title of the dashboard

'''
# :bike: Dashboard Analisis Penyewewaan Sepeda

Sistem penyewaan sepeda adalah evolusi otomatis dari penyewaan sepeda 
tradisional, memungkinkan pengguna untuk dengan mudah menyewa dan 
mengembalikan sepeda di berbagai lokasi. Saat ini, terdapat lebih dari 
500 program di seluruh dunia dengan lebih dari 500.000 sepeda. .
'''

# Sidebar untuk filter
#st.sidebar.title("Filter Data")
#season = st.sidebar.selectbox("Pilih Musim", ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])

# Mapping musim ke angka
#filtered_season = map_season(season)

# Create Tabs
tab1, tab2 = st.tabs(["📊 Tren Penyewaan Sepeda", "📈 Pengaruh Cuaca terhadap penyewaan"])

# Filter data berdasarkan musim yang dipilih dari sidebar
#filtered_data = df[df['season'] == filtered_season]

# Visualisasi Tren Penyewaan dengan Data 
with tab1:
    st.subheader('Tren Penyewaan Sepeda ')
    
    # Membuat figure dengan ukuran yang lebih besar
    plt.figure(figsize=(12, 7))
    
    # Menggunakan seaborn untuk plot dengan palet warna yang lebih menarik
    sns.set(style="whitegrid")  # Tema whitegrid agar tampilan lebih bersih
    sns.lineplot(x='mnth', y='cnt', hue='yr', data=df, marker="o", 
                 palette="coolwarm",  # Menggunakan palet warna yang lebih menarik
                 linewidth=2.5)  # Membuat garis lebih tebal

    # Menambahkan judul dan label sumbu yang lebih estetis
    plt.title('Tren Penyewaan Sepeda Berdasarkan Bulan (Semua Musim)', 
              fontsize=16, fontweight='bold', color='darkblue')
    plt.xlabel('Bulan', fontsize=12, fontweight='bold')
    plt.ylabel('Jumlah Penyewaan (cnt)', fontsize=12, fontweight='bold')

    # Menambahkan format khusus pada ticks untuk membuat sumbu X lebih rapi
    plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
               fontsize=10)
    plt.yticks(fontsize=10)

    # Menyesuaikan legenda agar lebih jelas dan tidak bertumpuk
    plt.legend(title='Tahun', title_fontsize='13', fontsize='11', loc='upper right', frameon=True)

    # Menampilkan plot di Streamlit
    st.pyplot(plt)

    st.subheader('Ringkasan Penyewaan Sepeda')

    # Buat kolom untuk metrik dan grafik batang
    col1, col2 = st.columns(2)

    with col1:
        # Hitung total penyewaan untuk seluruh data (tanpa filter musim)
        total_penyewaan = df['cnt'].sum()
        st.metric(label="Total Penyewaan Sepeda", value=total_penyewaan)

        # Total penyewaan oleh member terdaftar untuk seluruh data
        total_registered = df['registered'].sum()
        st.metric(label="Total Penyewaan oleh Member Terdaftar", value=total_registered)

        # Total penyewaan oleh non-member (casual) untuk seluruh data
        total_casual = df['casual'].sum()
        st.metric(label="Total Penyewaan oleh Non-Member", value=total_casual)

        # Rata-rata penyewaan untuk seluruh data
        avg_penyewaan = df['cnt'].mean()
        st.metric(label="Rata-rata Penyewaan Sepeda", value=round(avg_penyewaan, 2))

    with col2:
        # Visualisasi total penyewaan per musim dalam bentuk grafik batang
        plt.figure(figsize=(6, 4))
        sns.set(style="whitegrid")  # Tema untuk mempercantik tampilan
        season_totals = df.groupby('season')['cnt'].sum().reset_index()
        season_totals['season'] = season_totals['season'].replace({1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'})
        sns.barplot(x='season', y='cnt', data=season_totals, palette='Blues_d')

        # Menambahkan judul dan label pada grafik batang
        plt.title('Total Penyewaan Sepeda per Musim', fontsize=14, fontweight='bold')
        plt.xlabel('Musim', fontsize=12)
        plt.ylabel('Total Penyewaan (cnt)', fontsize=12)

        # Tampilkan grafik batang di Streamlit
        st.pyplot(plt)




with tab2:
    st.subheader("Pengaruh Cuaca terhadap Penyewaan")

    st.write("**Hubungan Suhu dengan Penyewaan**")
    
    # Membuat figur baru untuk line chart
    plt.figure(figsize=(20, 6))  # Atur ukuran plot lebih lebar
    temp_bins = pd.cut(df['temp'], bins=10)
    avg_by_temp = df.groupby(temp_bins)['cnt'].mean().reset_index()
    sns.lineplot(x=avg_by_temp['temp'].astype(str), y='cnt', data=avg_by_temp)
    
    plt.title('Rata-rata Penyewaan Berdasarkan Suhu')
    plt.xlabel('Suhu (interval)')
    plt.ylabel('Rata-rata Penyewaan')
    
    st.pyplot(plt)  # Menampilkan plot

    # Kolom untuk metrik dan bar chart yang sederhana
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Rata-rata Penyewaan Berdasarkan Kondisi Cuaca**")
        avg_by_weather = df.groupby('weathersit')['cnt'].mean().reset_index()
        avg_by_weather['weathersit'] = avg_by_weather['weathersit'].replace({
            1: 'Clear', 2: 'Mist', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'})
        
        plt.figure(figsize=(8, 6))  # Atur ukuran plot lebih lebar
        sns.barplot(x='weathersit', y='cnt', data=avg_by_weather, palette='Blues_d')

        plt.title('Rata-rata Penyewaan Berdasarkan Cuaca')
        plt.xlabel('Kondisi Cuaca')
        plt.ylabel('Rata-rata Penyewaan')
        
        # Rotasi label di X-axis agar tidak bertumpuk
        plt.xticks(rotation=45)
        
        # Format ulang Y-axis agar tidak menggunakan notasi ilmiah
        import matplotlib.ticker as ticker
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
        
        st.pyplot(plt)
    with col2:

    
        total_clear = df[df['weathersit'] == 1]['cnt'].sum()
        st.metric(label="Total Penyewaan Cuaca Cerah", value=total_clear)

        total_mist = df[df['weathersit'] == 2]['cnt'].sum()
        st.metric(label="Total Penyewaan Cuaca Berkabut", value=total_mist)

        total_rain_snow = df[df['weathersit'] == 3]['cnt'].sum()
        st.metric(label="Total Penyewaan Hujan/Salju", value=total_rain_snow)

        total_rain_snow = df[df['weathersit'] == 4]['cnt'].sum()
        st.metric(label="Total Penyewaan Cuaca Ekstream", value=total_rain_snow)




    # Tambahkan interpretasi
    st.write("""
    **Kesimpulan:**
    - Suhu sedang cenderung meningkatkan jumlah penyewaan.
    - Cuaca cerah menghasilkan penyewaan tertinggi.
    """)
    
    