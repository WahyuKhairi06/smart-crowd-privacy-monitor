"""
charts.py
Grafik dashboard menggunakan Plotly.
Tema warna mengikuti Flip7 Design System (teal-coral-gold, retro-playful).
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------------------------------------------------------
# Flip7 Design System -- Color Tokens
# ---------------------------------------------------------------------------
PRIMARY_TEAL = "#2BA8A2"
PRIMARY_LIGHT = "#3CC4BD"
PRIMARY_DARK = "#1E8C86"
PRIMARY_BG = "#E8F6F5"
ACCENT_GOLD = "#FFD23F"
ACCENT_LIGHT = "#FFE47A"
ACCENT_DARK = "#E6B800"
CORAL = "#EF6C4A"
CORAL_LIGHT = "#FF8A6A"
CORAL_DARK = "#D45233"
CREAM = "#FFF8E7"
SKY_BLUE = "#5DADE2"
SURFACE_BASE = "#EFF8F7"
SURFACE_CARD = "#FFFFFF"
SUCCESS = "#27AE60"
ERROR = "#E74C3C"

# Warna per level kepadatan (selaras dengan analytics.py)
DENSITY_COLOR_MAP = {
    "Low": SUCCESS,
    "Medium": ACCENT_GOLD,
    "High": CORAL,
}

FONT_FAMILY = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif"


def _base_layout(fig: go.Figure, title: str) -> go.Figure:
    """Terapkan layout dasar bertema Flip7 ke figure Plotly."""
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family=FONT_FAMILY, size=20, color=PRIMARY_DARK, weight="bold"),
            x=0.02,
        ),
        font=dict(family=FONT_FAMILY, color=PRIMARY_DARK),
        plot_bgcolor=SURFACE_CARD,
        paper_bgcolor=SURFACE_CARD,
        margin=dict(l=40, r=20, t=60, b=40),
        legend=dict(bgcolor=SURFACE_CARD, bordercolor=PRIMARY_BG, borderwidth=1),
    )
    return fig


def density_bar_chart(face_count: int, density_level: str) -> go.Figure:
    """
    Bar chart tunggal menampilkan jumlah wajah terdeteksi,
    diwarnai sesuai tingkat kepadatan.
    """
    color = DENSITY_COLOR_MAP.get(density_level, PRIMARY_TEAL)

    fig = go.Figure(
        data=[
            go.Bar(
                x=["Jumlah Wajah Terdeteksi"],
                y=[face_count],
                marker=dict(
                    color=color,
                    line=dict(color=PRIMARY_DARK, width=1.5),
                ),
                text=[f"{face_count}"],
                textposition="outside",
                textfont=dict(size=22, color=PRIMARY_DARK, family=FONT_FAMILY, weight="bold"),
                width=[0.4],
            )
        ]
    )

    fig.update_yaxes(title="Jumlah Wajah", gridcolor=PRIMARY_BG, zerolinecolor=PRIMARY_BG)
    fig.update_xaxes(title="")

    return _base_layout(fig, f"Hasil Deteksi -- Kepadatan: {density_level}")


def density_pie_chart(history_df: pd.DataFrame) -> go.Figure:
    """
    Pie chart distribusi tingkat kepadatan dari seluruh histori analisis.
    """
    if history_df.empty:
        counts = pd.Series({"Low": 0, "Medium": 0, "High": 0})
    else:
        counts = history_df["density_level"].value_counts()
        for level in ["Low", "Medium", "High"]:
            if level not in counts:
                counts[level] = 0
        counts = counts.reindex(["Low", "Medium", "High"])

    colors = [DENSITY_COLOR_MAP[level] for level in counts.index]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=counts.index,
                values=counts.values,
                marker=dict(colors=colors, line=dict(color=SURFACE_CARD, width=2)),
                hole=0.45,
                textinfo="label+percent",
                textfont=dict(family=FONT_FAMILY, size=14, color=PRIMARY_DARK),
            )
        ]
    )

    return _base_layout(fig, "Distribusi Tingkat Kepadatan (Histori)")


def history_line_chart(history_df: pd.DataFrame) -> go.Figure:
    """
    Line chart tren jumlah wajah terdeteksi dari waktu ke waktu.
    """
    fig = go.Figure()

    if history_df.empty:
        fig.add_annotation(
            text="Belum ada data histori",
            showarrow=False,
            font=dict(size=16, color=PRIMARY_DARK, family=FONT_FAMILY),
        )
    else:
        df = history_df.sort_values("timestamp")

        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["face_count"],
                mode="lines+markers",
                line=dict(color=PRIMARY_TEAL, width=3, shape="spline"),
                marker=dict(
                    size=9,
                    color=df["density_level"].map(DENSITY_COLOR_MAP),
                    line=dict(color=PRIMARY_DARK, width=1),
                ),
                name="Jumlah Wajah",
                hovertemplate="%{x}<br>Wajah: %{y}<extra></extra>",
            )
        )

    fig.update_yaxes(title="Jumlah Wajah", gridcolor=PRIMARY_BG, zerolinecolor=PRIMARY_BG)
    fig.update_xaxes(title="Waktu", gridcolor=PRIMARY_BG)

    return _base_layout(fig, "Tren Histori Analisis Kepadatan")


def history_bar_by_level(history_df: pd.DataFrame) -> go.Figure:
    """
    Bar chart jumlah analisis berdasarkan level kepadatan (agregat histori).
    """
    if history_df.empty:
        counts = pd.Series({"Low": 0, "Medium": 0, "High": 0})
    else:
        counts = history_df["density_level"].value_counts()
        for level in ["Low", "Medium", "High"]:
            if level not in counts:
                counts[level] = 0
        counts = counts.reindex(["Low", "Medium", "High"])

    colors = [DENSITY_COLOR_MAP[level] for level in counts.index]

    fig = go.Figure(
        data=[
            go.Bar(
                x=counts.index,
                y=counts.values,
                marker=dict(color=colors, line=dict(color=PRIMARY_DARK, width=1.5)),
                text=counts.values,
                textposition="outside",
                textfont=dict(family=FONT_FAMILY, color=PRIMARY_DARK),
            )
        ]
    )

    fig.update_yaxes(title="Jumlah Analisis", gridcolor=PRIMARY_BG, zerolinecolor=PRIMARY_BG)
    fig.update_xaxes(title="Tingkat Kepadatan")

    return _base_layout(fig, "Jumlah Analisis per Tingkat Kepadatan")
