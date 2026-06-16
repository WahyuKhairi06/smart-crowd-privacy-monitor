"""
app.py
Halaman utama -- Smart Crowd Privacy Monitoring System
Menggunakan Haar Cascade dan Gaussian Blur untuk Analisis Kepadatan
Keramaian Berbasis Web.

Alur:
    Upload Gambar -> Face Detection (Haar Cascade) -> Gaussian Blur
    -> Face Counting -> Density Classification -> Dashboard -> PDF Report
"""

import streamlit as st
from PIL import Image

from src.theme import apply_flip7_theme, render_hero, section_title, density_badge
from src.utils import pil_to_cv2, cv2_to_rgb, ensure_dirs, readable_timestamp
from src.processor import process_image
from src.charts import density_bar_chart
from src.report_generator import generate_pdf_report


st.set_page_config(
    page_title="Smart Crowd Privacy Monitor",
    page_icon="🛡️",
    layout="wide",
)

ensure_dirs()
apply_flip7_theme()
render_hero(ribbon="SMART CROWD PRIVACY MONITOR")

# Tampilkan nama dan NIM di bawah judul
st.markdown(
    """
    <div style="text-align:center; margin-bottom:24px;">
        <p style="color:#1E8C86; font-size:14px; font-weight:500; margin:0;">
            <b>Wahyu Khairi - 2311531009</b>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="text-align:center; max-width: 720px; margin: 0 auto 24px auto;
                color:#1E8C86; font-size:15px;">
        Unggah foto keramaian (acara, jalan raya, kampus, atau ruang publik).
        Sistem akan mendeteksi wajah menggunakan <b>Haar Cascade</b>,
        menyamarkannya dengan <b>Gaussian Blur</b> untuk melindungi privasi,
        lalu menghitung jumlah orang dan mengklasifikasikan tingkat kepadatan.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------
section_title("📤", "Upload Gambar")

uploaded_file = st.file_uploader(
    "Pilih gambar keramaian (JPG, JPEG, atau PNG)",
    type=["jpg", "jpeg", "png"],
)

with st.expander("⚙️ Pengaturan Lanjutan (Opsional)"):
    blur_strength = st.slider(
        "Kekuatan Gaussian Blur",
        min_value=15, max_value=99, value=51, step=2,
        help="Nilai lebih tinggi = blur lebih kuat. Harus bernilai ganjil (otomatis disesuaikan).",
    )

# ---------------------------------------------------------------------------
# Processing
# ---------------------------------------------------------------------------
if uploaded_file is not None:

    pil_image = Image.open(uploaded_file)
    cv2_image = pil_to_cv2(pil_image)

    col_original, col_protected = st.columns(2)

    with col_original:
        section_title("🖼️", "Gambar Asli")
        st.image(pil_image, use_container_width=True)

    if st.button("🔍 Jalankan Analisis", type="primary", use_container_width=True):
        with st.spinner("Mendeteksi wajah dan menerapkan privasi..."):
            result = process_image(cv2_image, uploaded_file.name, blur_strength=blur_strength)

        # Simpan hasil ke session state agar tetap muncul setelah rerun
        st.session_state["last_result"] = result
        st.session_state["last_filename"] = uploaded_file.name

    # ---------------------------------------------------------------------
    # Tampilkan hasil jika sudah ada di session_state
    # ---------------------------------------------------------------------
    if "last_result" in st.session_state:
        result = st.session_state["last_result"]

        with col_protected:
            section_title("🔒", "Protected Image (Wajah Tersamarkan)")
            st.image(cv2_to_rgb(result["protected_image"]), use_container_width=True)

        st.markdown("---")

        # --- Output Cards ---
        section_title("📊", "Hasil Analisis")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                f"""
                <div class="flip7-card sky">
                    <div style="font-size:13px; color:#5DADE2; font-weight:700;">DETECTED FACES</div>
                    <div style="font-size:36px; font-weight:800; color:#1E8C86;">
                        {result['face_count']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown(
                f"""
                <div class="flip7-card gold">
                    <div style="font-size:13px; color:#E6B800; font-weight:700;">TINGKAT KEPADATAN</div>
                    <div style="margin-top:6px;">
                        {result['density_emoji']} {density_badge(result['density_level'])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown(
                f"""
                <div class="flip7-card">
                    <div style="font-size:13px; color:#2BA8A2; font-weight:700;">WAKTU ANALISIS</div>
                    <div style="font-size:16px; font-weight:700; color:#1E8C86; margin-top:6px;">
                        {readable_timestamp()}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c4:
            st.markdown(
                f"""
                <div class="flip7-card">
                    <div style="font-size:13px; color:#2BA8A2; font-weight:700;">CONFIDENCE SCORE</div>
                    <div style="font-size:16px; font-weight:700; color:#1E8C86; margin-top:6px;">
                        {result['confidence']}%
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # --- Bar chart hasil deteksi ---
        st.plotly_chart(
            density_bar_chart(result["face_count"], result["density_level"]),
            use_container_width=True,
        )

        # --- PDF Report ---
        section_title("📄", "Laporan PDF")

        if st.button("📥 Buat Laporan PDF", use_container_width=True):
            with st.spinner("Membuat laporan PDF..."):
                pdf_path = generate_pdf_report(
                    image_path=result["saved_path"],
                    face_count=result["face_count"],
                    density_level=result["density_level"],
                    timestamp=result["timestamp"],
                )
            st.session_state["last_pdf_path"] = pdf_path
            st.success("Laporan PDF berhasil dibuat!")

        if "last_pdf_path" in st.session_state:
            with open(st.session_state["last_pdf_path"], "rb") as f:
                st.download_button(
                    label="⬇️ Unduh report.pdf",
                    data=f,
                    file_name="report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

else:
    st.info("⬆️ Silakan unggah gambar untuk memulai analisis.")

# ---------------------------------------------------------------------------
# Footer / navigation hint
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#2BA8A2; font-size:13px;">
        Buka menu <b>Dashboard</b> di sidebar untuk melihat statistik &amp; histori lengkap,
        atau menu <b>About</b> untuk informasi proyek.
    </div>
    """,
    unsafe_allow_html=True,
    
)
