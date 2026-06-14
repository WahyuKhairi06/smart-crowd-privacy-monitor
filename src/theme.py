"""
theme.py
CSS kustom bertema Flip7 Design System (retro-playful, teal-coral-gold)
untuk diterapkan pada seluruh halaman Streamlit.
"""

import streamlit as st

FLIP7_CSS = """
<style>
/* ============================================================
   Flip7 Design System -- Streamlit Theming
   teal-coral-gold, retro-playful
   ============================================================ */

:root {
    --primary-teal: #2BA8A2;
    --primary-light: #3CC4BD;
    --primary-dark: #1E8C86;
    --primary-bg: #E8F6F5;
    --accent-gold: #FFD23F;
    --accent-light: #FFE47A;
    --accent-dark: #E6B800;
    --coral: #EF6C4A;
    --coral-light: #FF8A6A;
    --coral-dark: #D45233;
    --cream: #FFF8E7;
    --sky-blue: #5DADE2;
    --surface-base: #EFF8F7;
    --surface-card: #FFFFFF;
    --success: #27AE60;
    --error: #E74C3C;
}

/* App background */
.stApp {
    background-color: var(--surface-base);
}

/* Headings */
h1, h2, h3 {
    font-weight: 800 !important;
    color: var(--primary-dark) !important;
    letter-spacing: 0.04em;
}

/* ---------------- Hero / Logo banner ---------------- */
.flip7-hero {
    position: relative;
    text-align: center;
    padding: 28px 16px 22px 16px;
    margin-bottom: 12px;
}

.flip7-hero-title {
    display: inline-block;
    font-size: 44px;
    font-weight: 800;
    color: var(--primary-dark);
    background: var(--cream);
    border: 3px solid var(--primary-dark);
    border-radius: 16px;
    padding: 10px 32px;
    transform: rotate(-2deg);
    box-shadow: 0 4rpx 20px rgba(43, 168, 162, 0.20);
    letter-spacing: 0.08em;
}

.flip7-logo {
    display: inline-block;
    background: var(--cream);
    border: 3px solid var(--primary-dark);
    border-radius: 14px;
    padding: 8px 12px;
    transform: rotate(-2deg);
    box-shadow: 0 6px 24px rgba(0,0,0,0.06);
}

.flip7-logo img {
    display: block;
    height: 56px;
    width: auto;
}

.flip7-hero-title .flip7-7 {
    color: var(--accent-gold);
    text-shadow: 1px 1px 0 var(--primary-dark), -1px -1px 0 var(--primary-dark);
    font-size: 52px;
}

.flip7-ribbon {
    display: inline-block;
    margin-top: 14px;
    background: var(--cream);
    border: 3px solid var(--primary-dark);
    border-radius: 999px;
    padding: 6px 28px;
    font-weight: 800;
    color: var(--primary-dark);
    letter-spacing: 0.12em;
    font-size: 13px;
}

/* ---------------- Section title ---------------- */
.flip7-section-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 22px;
    font-weight: 800;
    color: var(--primary-dark);
    border-bottom: 3px dashed var(--primary-light);
    padding-bottom: 8px;
    margin: 18px 0 14px 0;
}

/* ---------------- Cards ---------------- */
.flip7-card {
    background: var(--surface-card);
    border-radius: 24px;
    box-shadow: 0 4px 20px rgba(43, 168, 162, 0.10);
    border-left: 6px solid var(--primary-light);
    padding: 18px 20px;
    margin-bottom: 16px;
}

.flip7-card.gold {
    border-left-color: var(--accent-gold);
    background: linear-gradient(135deg, var(--cream) 0%, var(--surface-card) 100%);
    box-shadow: 0 4px 20px rgba(255, 210, 63, 0.40);
}

.flip7-card.coral {
    border-left-color: var(--coral);
    background: linear-gradient(135deg, #fff0ec 0%, var(--surface-card) 100%);
    box-shadow: 0 4px 20px rgba(239, 108, 74, 0.35);
}

.flip7-card.sky {
    border-left-color: var(--sky-blue);
    box-shadow: 0 4px 16px rgba(93, 173, 226, 0.30);
}

/* ---------------- Metric badges ---------------- */
.flip7-badge {
    display: inline-block;
    padding: 8px 22px;
    border-radius: 999px;
    font-weight: 800;
    font-size: 15px;
    letter-spacing: 0.06em;
    color: #fff;
}

.flip7-badge.low { background: var(--success); box-shadow: 0 4px 16px rgba(39,174,96,0.35); }
.flip7-badge.medium { background: var(--accent-dark); box-shadow: 0 4px 16px rgba(255,210,63,0.45); }
.flip7-badge.high { background: var(--coral); box-shadow: 0 4px 20px rgba(239,108,74,0.40); }

/* ---------------- Buttons ---------------- */
.stButton > button {
    border-radius: 999px !important;
    font-weight: 800 !important;
    min-height: 48px !important;
    border: none !important;
    background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-dark) 100%) !important;
    color: var(--primary-dark) !important;
    box-shadow: 0 4px 20px rgba(255, 210, 63, 0.40) !important;
    letter-spacing: 0.04em;
    transition: transform 0.15s ease-out;
}

.stButton > button:hover {
    transform: scale(1.02);
}

.stButton > button:active {
    transform: scale(0.96);
}

/* Download button */
.stDownloadButton > button {
    border-radius: 999px !important;
    font-weight: 800 !important;
    min-height: 48px !important;
    border: 2px solid var(--primary-teal) !important;
    background: var(--surface-card) !important;
    color: var(--primary-dark) !important;
    box-shadow: 0 4px 16px rgba(43, 168, 162, 0.25) !important;
}

/* ---------------- File uploader ---------------- */
[data-testid="stFileUploaderDropzone"] {
    background: var(--cream) !important;
    border: 2px dashed var(--primary-light) !important;
    border-radius: 16px !important;
}

/* ---------------- Sidebar ---------------- */
[data-testid="stSidebar"] {
    background: var(--surface-card);
    border-right: 3px dashed var(--primary-light);
}

/* ---------------- Tabs ---------------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background: var(--cream);
    border-radius: 999px;
    padding: 8px 20px;
    font-weight: 700;
    color: var(--primary-dark);
}

.stTabs [aria-selected="true"] {
    background: var(--primary-teal) !important;
    color: #fff !important;
    box-shadow: 0 4px 16px rgba(43, 168, 162, 0.30);
}

/* ---------------- Dataframe / table ---------------- */
[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(43,168,162,0.10);
}

/* ---------------- Metrics ---------------- */
[data-testid="stMetric"] {
    background: var(--surface-card);
    border-radius: 16px;
    padding: 12px 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-left: 6px solid var(--primary-light);
}
</style>
"""


def apply_flip7_theme():
    """Suntikkan CSS Flip7 Design System ke halaman Streamlit saat ini."""
    st.markdown(FLIP7_CSS, unsafe_allow_html=True)


def render_hero(title: str = "FLIP", number: str = "7", ribbon: str = "CROWD PRIVACY MONITOR"):
    """Render header. Uses an image logo (overrides textual Flip7 mark)."""
    # VIDIO logo from blog (small shape); fallback to text if blocked
    logo_url = "https://d1y832s0jkkru8.cloudfront.net/assets/images/logos/vidio-shape-logo-small.webp"
    st.markdown(
        f"""
        <div class="flip7-hero">
            <div class="flip7-logo"><img src="{logo_url}" alt="logo"/></div>
            <br/>
            <div class="flip7-ribbon">{ribbon}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(emoji: str, text: str):
    """Render judul section dengan emoji icon dan border dashed."""
    st.markdown(
        f'<div class="flip7-section-title"><span>{emoji}</span><span>{text}</span></div>',
        unsafe_allow_html=True,
    )


def density_badge(level: str) -> str:
    """Kembalikan HTML badge untuk level kepadatan tertentu."""
    css_class = {"Low": "low", "Medium": "medium", "High": "high"}.get(level, "low")
    return f'<span class="flip7-badge {css_class}">{level.upper()}</span>'
