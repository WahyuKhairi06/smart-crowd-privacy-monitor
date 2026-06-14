# Smart Crowd Privacy Monitoring System

Sistem web berbasis **Streamlit** yang mendeteksi wajah pada foto keramaian
menggunakan **Haar Cascade**, menyamarkan wajah dengan **Gaussian Blur**,
menghitung jumlah orang, menganalisis tingkat kepadatan keramaian, dan
menghasilkan dashboard serta laporan PDF otomatis.

UI styled dengan **Flip7 Design System** (retro-playful, teal-coral-gold).

## Alur Sistem

```
Upload Gambar
     │
     ▼
Face Detection (Haar Cascade)
     │
     ▼
Gaussian Blur
     │
     ▼
Face Counting
     │
     ▼
Density Classification
     │
     ▼
Dashboard
     │
     ▼
PDF Report
```

## Rule Klasifikasi Kepadatan

| Jumlah Wajah | Level  |
|--------------|--------|
| 0 - 5        | Low    |
| 6 - 15       | Medium |
| > 15         | High   |

## Instalasi

```bash
pip install -r requirements.txt
```

## Menjalankan Aplikasi

```bash
streamlit run app.py
```

Buka browser ke `http://localhost:8501`.

- **Halaman utama (app.py)** — upload gambar, jalankan analisis, unduh laporan PDF.
- **Dashboard** — statistik agregat, bar/pie/history chart, tabel histori.
- **About** — informasi proyek, metode, teknologi, dan nilai akademik.

## Struktur Folder

```
smart-crowd-privacy-monitor/
│
├── app.py
├── requirements.txt
│
├── src/
│   ├── detector.py
│   ├── privacy.py
│   ├── analytics.py
│   ├── processor.py
│   ├── charts.py
│   ├── report_generator.py
│   ├── storage.py
│   ├── theme.py
│   └── utils.py
│
├── pages/
│   ├── dashboard.py
│   └── about.py
│
├── outputs/
│   ├── reports/
│   └── images/
│
└── data/
    └── analytics.csv
```

## Teknologi

- Python
- Streamlit
- OpenCV
- Pandas
- Plotly
- ReportLab
