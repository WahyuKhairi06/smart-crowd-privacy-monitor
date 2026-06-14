"""
pages/dashboard.py
Halaman dashboard -- menampilkan statistik agregat dan histori analisis
dalam bentuk Bar Chart, Pie Chart, dan History Chart.
"""

import streamlit as st
import pandas as pd

from src.theme import apply_flip7_theme, render_hero, section_title, density_badge
from src.storage import load_history, clear_history
from src.charts import density_pie_chart, history_line_chart, history_bar_by_level


st.set_page_config(
    page_title="Dashboard - Smart Crowd Privacy Monitor",
    page_icon="📊",
    layout="wide",
)

apply_flip7_theme()
render_hero(ribbon="ANALYTICS DASHBOARD")

history_df = load_history()

# ---------------------------------------------------------------------------
# Summary metrics
# ---------------------------------------------------------------------------
section_title("📈", "Ringkasan Statistik")

total_analisis = len(history_df)
total_wajah = int(history_df["face_count"].sum()) if not history_df.empty else 0
avg_wajah = round(history_df["face_count"].mean(), 1) if not history_df.empty else 0.0

if not history_df.empty:
    most_common_level = history_df["density_level"].mode().iloc[0]
else:
    most_common_level = "-"

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Total Analisis", total_analisis)

with m2:
    st.metric("Total Wajah Terdeteksi", total_wajah)

with m3:
    st.metric("Rata-rata Wajah / Gambar", avg_wajah)

with m4:
    st.markdown(
        f"""
        <div style="background:#FFFFFF; border-radius:16px; padding:12px 16px;
                     box-shadow:0 2px 8px rgba(0,0,0,0.08); border-left:6px solid #FFD23F;">
            <div style="font-size:13px; color:#555;">Level Terbanyak</div>
            <div style="margin-top:6px;">
                {density_badge(most_common_level) if most_common_level != "-" else "-"}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------
section_title("📊", "Grafik Analitik")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(density_pie_chart(history_df), use_container_width=True)

with col2:
    st.plotly_chart(history_bar_by_level(history_df), use_container_width=True)

st.plotly_chart(history_line_chart(history_df), use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------------------------
# History table
# ---------------------------------------------------------------------------
section_title("🗂️", "Histori Analisis")

if history_df.empty:
    st.info("Belum ada histori analisis. Unggah gambar pada halaman utama untuk memulai.")
else:
    display_df = history_df.copy()
    display_df["timestamp"] = display_df["timestamp"].dt.strftime("%d-%m-%Y %H:%M:%S")
    display_df = display_df.rename(columns={
        "timestamp": "Waktu",
        "filename": "Nama File",
        "face_count": "Jumlah Wajah",
        "density_level": "Tingkat Kepadatan",
        "image_path": "Path Gambar",
    })

    st.dataframe(
        display_df[["Waktu", "Nama File", "Jumlah Wajah", "Tingkat Kepadatan", "Path Gambar"]],
        use_container_width=True,
        hide_index=True,
    )

    col_a, col_b = st.columns([3, 1])
    with col_b:
        if st.button("🗑️ Hapus Histori", use_container_width=True):
            clear_history()
            st.success("Histori berhasil dihapus.")
            st.rerun()
