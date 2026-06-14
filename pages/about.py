"""
pages/about.py
Informasi proyek -- Smart Crowd Privacy Monitoring System.
"""

import streamlit as st

from src.theme import apply_flip7_theme, render_hero, section_title


st.set_page_config(
    page_title="About - Smart Crowd Privacy Monitor",
    page_icon="ℹ️",
    layout="wide",
)

apply_flip7_theme()
render_hero(ribbon="ABOUT THIS PROJECT")

section_title("🛡️", "Smart Crowd Privacy Monitoring System")

st.markdown(
    """
    <div class="flip7-card">
        Sistem web berbasis <b>Streamlit</b> yang mendeteksi wajah pada foto keramaian
        menggunakan <b>Haar Cascade</b>, menyamarkan wajah dengan <b>Gaussian Blur</b>,
        menghitung jumlah orang, menganalisis tingkat kepadatan keramaian, dan
        menghasilkan dashboard serta laporan PDF otomatis.
    </div>
    """,
    unsafe_allow_html=True,
)

section_title("🔁", "Alur Sistem")

st.markdown(
    """
    <div class="flip7-card sky">
        Upload Gambar &rarr; Face Detection (Haar Cascade) &rarr; Gaussian Blur
        &rarr; Face Counting &rarr; Density Classification &rarr; Dashboard &rarr; PDF Report
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    section_title("🧠", "Metode yang Digunakan")
    st.markdown(
        """
        <div class="flip7-card">
            <b>1. Haar Cascade</b><br/>
            Digunakan untuk mendeteksi wajah pada gambar.<br/>
            <i>Output:</i> koordinat wajah (x, y, w, h)
        </div>
        <div class="flip7-card coral">
            <b>2. Gaussian Blur</b><br/>
            Digunakan untuk menyamarkan wajah dan melindungi privasi individu.<br/>
            <i>Output:</i> wajah menjadi blur
        </div>
        <div class="flip7-card">
            <b>3. Face Counting</b><br/>
            Digunakan untuk menghitung jumlah wajah.<br/>
            <i>Output:</i> jumlah orang dalam gambar
        </div>
        <div class="flip7-card gold">
            <b>4. Density Classification</b><br/>
            Digunakan untuk mengukur tingkat keramaian.<br/>
            <i>Rule:</i> 0&ndash;5 = Low, 6&ndash;15 = Medium, &gt;15 = High
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    section_title("⚙️", "Teknologi")
    st.markdown(
        """
        <div class="flip7-card">
            🐍 Python<br/>
            🖥️ Streamlit<br/>
            👁️ OpenCV<br/>
            🐼 Pandas<br/>
            📊 Plotly<br/>
            📄 ReportLab
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_title("🎓", "Nilai Akademik yang Didapat")
    st.markdown(
        """
        <div class="flip7-card">
            <b>Image Processing</b> &mdash; Grayscale Conversion, Gaussian Blur<br/><br/>
            <b>Computer Vision</b> &mdash; Haar Cascade Face Detection<br/><br/>
            <b>Data Analytics</b> &mdash; Face Counting, Density Classification<br/><br/>
            <b>Web Development</b> &mdash; Streamlit Dashboard<br/><br/>
            <b>Reporting</b> &mdash; PDF Generator
        </div>
        """,
        unsafe_allow_html=True,
    )

section_title("📥📤", "Input & Output")

col_in, col_out = st.columns(2)

with col_in:
    st.markdown(
        """
        <div class="flip7-card">
            <b>Input</b><br/>
            Format: JPG, JPEG, PNG<br/>
            Berupa: foto keramaian, foto publik, foto acara, foto kampus, foto jalan raya
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_out:
    st.markdown(
        """
        <div class="flip7-card gold">
            <b>Output</b><br/>
            1. Protected Image (gambar hasil blur)<br/>
            2. Detected Faces: X<br/>
            3. Tingkat Kepadatan (Low / Medium / High)<br/>
            4. Dashboard (Bar Chart, Pie Chart, History Chart)<br/>
            5. PDF Report (report.pdf)
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#2BA8A2; font-size:13px;">
        Smart Crowd Privacy Monitoring System &mdash; Web-based Crowd Density Analysis
        with Privacy Protection.
    </div>
    """,
    unsafe_allow_html=True,
)
