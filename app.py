"""
DIGITAL TWIN – SMART ENERGY
Surveillance & Optimisation en temps réel
Streamlit Dashboard — reproduction fidèle du design original
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Digital Twin – Smart Energy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;600;700&display=swap');

  /* ── Root & Background ── */
  html, body, [data-testid="stAppViewContainer"] {
    background: #080e1a !important;
    color: #e0e8f8 !important;
    font-family: 'Exo 2', sans-serif !important;
  }
  [data-testid="stAppViewContainer"] > .main {
    background: #080e1a !important;
  }
  [data-testid="stHeader"] { background: transparent !important; }
  section[data-testid="stSidebar"] {
    background: #0b1220 !important;
    border-right: 1px solid #1a2a40 !important;
  }

  /* ── Sidebar nav items ── */
  .nav-item {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px; margin: 3px 0;
    border-radius: 8px; cursor: pointer;
    font-size: 14px; color: #8aa0c0;
    transition: all .2s;
  }
  .nav-item.active {
    background: linear-gradient(90deg, #1a3560, #0f2040);
    color: #4af0c8; border-left: 3px solid #4af0c8;
  }
  .nav-item:hover { background: #12203a; color: #c0d8f8; }

  /* ── KPI Cards ── */
  .kpi-card {
    background: linear-gradient(135deg, #0d1b30 0%, #0a1525 100%);
    border: 1px solid #1c3055;
    border-radius: 12px;
    padding: 14px 16px;
    position: relative; overflow: hidden;
    height: 110px;
  }
  .kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent, #4af0c8);
  }
  .kpi-label { font-size: 11px; color: #6080a0; text-transform: uppercase; letter-spacing: 1px; }
  .kpi-value { font-family: 'Rajdhani', sans-serif; font-size: 2.2rem; font-weight: 700; line-height: 1.1; }
  .kpi-sub { font-size: 11px; color: #8aa0c0; margin-top: 2px; }
  .kpi-badge-pos { color: #4af0c8; font-size: 11px; font-weight: 600; }
  .kpi-badge-neg { color: #f04a7a; font-size: 11px; font-weight: 600; }

  /* ── Section titles ── */
  .section-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 13px; font-weight: 600;
    letter-spacing: 2px; text-transform: uppercase;
    color: #6080a0; margin-bottom: 8px;
  }

  /* ── Flow node ── */
  .flow-node {
    background: linear-gradient(135deg, #0d1b30, #0a1525);
    border: 1px solid #1c3055; border-radius: 12px;
    padding: 16px; text-align: center;
  }
  .flow-node-title { font-size: 11px; color: #6080a0; text-transform: uppercase; letter-spacing: 1px; }
  .flow-node-value { font-family: 'Rajdhani', sans-serif; font-size: 1.8rem; font-weight: 700; }
  .flow-node-sub { font-size: 11px; color: #8aa0c0; }

  /* ── Bilan rows ── */
  .bilan-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 8px 0; border-bottom: 1px solid #12203a;
    font-size: 14px;
  }
  .bilan-val { font-family: 'Rajdhani', sans-serif; font-size: 1rem; font-weight: 600; }

  /* ── Device row ── */
  .device-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 7px 0; border-bottom: 1px solid #12203a; font-size: 13px;
  }
  .online { color: #4af0c8; font-size: 11px; }

  /* ── Footer bar ── */
  .footer-bar {
    background: linear-gradient(90deg, #0d1b30, #0b1525);
    border: 1px solid #1c3055; border-radius: 12px;
    padding: 14px 24px;
    display: flex; justify-content: space-between; align-items: center;
    margin-top: 16px;
  }
  .footer-item { text-align: center; }
  .footer-val { font-family: 'Rajdhani', sans-serif; font-size: 1.5rem; font-weight: 700; }

  /* ── Top header bar ── */
  .top-bar {
    background: linear-gradient(90deg, #0b1525, #0d1b30);
    border: 1px solid #1c3055; border-radius: 10px;
    padding: 8px 16px; display: flex; align-items: center; gap: 24px;
    margin-bottom: 14px;
  }
  .status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 5px; }
  .dot-green { background: #4af0c8; box-shadow: 0 0 6px #4af0c8; }
  .dot-red   { background: #f04a7a; box-shadow: 0 0 6px #f04a7a; }

  /* ── Autonomy ring label ── */
  .ring-label { font-family: 'Rajdhani', sans-serif; font-size: 2.2rem; font-weight: 700; color: #4af0c8; }

  /* Remove streamlit default padding */
  .block-container { padding-top: 1rem !important; padding-bottom: 0 !important; }
  [data-testid="stVerticalBlock"] > div { gap: 0.5rem !important; }
  div[data-testid="metric-container"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ─── HELPERS ────────────────────────────────────────────────────────────────────
def dark_fig(fig, height=160):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=height,
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig

def sparkline(y, color):
    x = list(range(len(y)))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines",
        line=dict(color=color, width=2),
        fill="tozeroy",
        fillcolor=color.replace("rgb", "rgba").replace(")", ",0.15)") if color.startswith("rgb") else color + "26",
    ))
    return dark_fig(fig, 50)

def hourly_data():
    hours = pd.date_range("2024-05-19 00:00", periods=24, freq="h")
    prod = np.clip(np.sin(np.linspace(0, np.pi, 24)) * 3 + np.random.normal(0, 0.1, 24), 0, None)
    cons = np.clip(0.8 + np.random.normal(0, 0.15, 24), 0.3, 2)
    return hours, prod, cons

# ─── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:10px 0 20px'>
      <div style='display:flex;align-items:center;gap:10px'>
        <div style='width:36px;height:36px;background:linear-gradient(135deg,#0080ff,#00d4aa);
                    border-radius:8px;display:flex;align-items:center;justify-content:center;
                    font-size:18px'>⚡</div>
        <div>
          <div style='font-family:Rajdhani,sans-serif;font-weight:700;font-size:15px;color:#e0e8f8'>
            DIGITAL TWIN
          </div>
          <div style='font-size:10px;color:#6080a0'>SMART ENERGY</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    nav_items = [
        ("📊", "Aperçu", True),
        ("⚡", "Flux d'énergie", False),
        ("📱", "Appareils", False),
        ("🔋", "Stockage", False),
        ("📈", "Historique", False),
        ("🔬", "Analyses", False),
        ("🔔", "Alarmes", False),
        ("🎭", "Scénarios", False),
    ]
    for icon, label, active in nav_items:
        cls = "nav-item active" if active else "nav-item"
        st.markdown(f'<div class="{cls}">{icon} {label}</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1a2a40;margin:16px 0'>", unsafe_allow_html=True)

    # Weather
    st.markdown("""
    <div class='section-title'>MÉTÉO ACTUELLE</div>
    <div style='display:flex;align-items:center;gap:14px;padding:8px 0'>
      <div style='font-size:32px'>🌤</div>
      <div>
        <div style='font-family:Rajdhani,sans-serif;font-size:2rem;font-weight:700;color:#ffd060'>27°C</div>
        <div style='font-size:12px;color:#8aa0c0'>Ensoleillé</div>
      </div>
    </div>
    <div style='font-size:12px;color:#6080a0;margin-top:6px'>
      ☀️ Irradiation solaire <span style='color:#ffd060'>800 W/m²</span><br>
      💧 Humidité <span style='color:#60b8ff'>45 %</span><br>
      💨 Vent <span style='color:#8aa0c0'>12 km/h</span>
    </div>
    <div style='display:flex;gap:8px;margin-top:12px'>
      <div style='text-align:center;flex:1'>
        <div style='font-size:10px;color:#6080a0'>MAR</div>
        <div>🌤</div>
        <div style='font-size:10px;color:#e0e8f8'>28/16°C</div>
      </div>
      <div style='text-align:center;flex:1'>
        <div style='font-size:10px;color:#6080a0'>MER</div>
        <div>☀️</div>
        <div style='font-size:10px;color:#e0e8f8'>27/15°C</div>
      </div>
      <div style='text-align:center;flex:1'>
        <div style='font-size:10px;color:#6080a0'>JEU</div>
        <div>🌤</div>
        <div style='font-size:10px;color:#e0e8f8'>26/14°C</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─── MAIN AREA ──────────────────────────────────────────────────────────────────

# TOP STATUS BAR
st.markdown("""
<div class='top-bar'>
  <div style='font-family:Rajdhani,sans-serif;font-weight:700;font-size:16px;color:#e0e8f8'>
    ⚡ DIGITAL TWIN – SMART ENERGY &nbsp;
    <span style='font-size:11px;color:#6080a0;font-weight:400'>Surveillance & Optimisation en temps réel</span>
  </div>
  <div style='margin-left:auto;display:flex;gap:24px;align-items:center'>
    <div style='font-size:12px'>
      Mode de fonctionnement<br>
      <span class='status-dot dot-green'></span>
      <span style='color:#4af0c8;font-weight:600'>AUTONOME</span>
    </div>
    <div style='font-size:12px'>
      Statut système<br>
      <span class='status-dot dot-green'></span>
      <span style='color:#4af0c8;font-weight:600'>NORMAL</span>
    </div>
    <div style='font-size:12px'>
      Dernière mise à jour<br>
      <span class='status-dot dot-red'></span>
      <span style='color:#f04a7a;font-weight:600'>10:24:35 LIVE</span>
    </div>
    <div style='font-size:12px;color:#8aa0c0'>📅 19 Mai 2024 &nbsp; 🕐 10:24</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── KPI ROW ────────────────────────────────────────────────────────────────────
hours, prod_data, cons_data = hourly_data()
k1, k2, k3, k4, k5 = st.columns([1, 1, 1, 1, 0.8])

with k1:
    st.markdown("""
    <div class='kpi-card' style='--accent:#4af0c8'>
      <div class='kpi-label'>☀️ Production PV</div>
      <div class='kpi-value' style='color:#4af0c8'>2.45 <span style='font-size:1rem'>kW</span></div>
      <div class='kpi-sub'>Aujourd'hui : 18.7 kWh</div>
      <div class='kpi-badge-pos'>+12% vs hier</div>
    </div>
    """, unsafe_allow_html=True)
    fig = sparkline(prod_data, "#4af0c8")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with k2:
    st.markdown("""
    <div class='kpi-card' style='--accent:#60b8ff'>
      <div class='kpi-label'>🔋 Batterie</div>
      <div class='kpi-value' style='color:#60b8ff'>80<span style='font-size:1rem'>%</span></div>
      <div class='kpi-sub'>48.0 V &nbsp;|&nbsp; 40.0 A</div>
      <div style='font-size:11px;color:#8aa0c0'>Énergie stockée : 4.4 kWh</div>
    </div>
    """, unsafe_allow_html=True)
    bat_fig = go.Figure(go.Indicator(
        mode="gauge", value=80,
        gauge=dict(
            axis=dict(range=[0, 100], visible=False),
            bar=dict(color="#60b8ff", thickness=0.3),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            steps=[dict(range=[0, 100], color="#0d1b30")],
        )
    ))
    bat_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=10,r=10,t=10,b=0), height=50)
    st.plotly_chart(bat_fig, use_container_width=True, config={"displayModeBar": False})

with k3:
    st.markdown("""
    <div class='kpi-card' style='--accent:#ffd060'>
      <div class='kpi-label'>🏠 Consommation</div>
      <div class='kpi-value' style='color:#ffd060'>1.60 <span style='font-size:1rem'>kW</span></div>
      <div class='kpi-sub'>Aujourd'hui : 14.3 kWh</div>
      <div class='kpi-badge-pos'>+8% vs hier</div>
    </div>
    """, unsafe_allow_html=True)
    fig = sparkline(cons_data, "#ffd060")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with k4:
    net = np.random.normal(-0.3, 0.2, 24)
    st.markdown("""
    <div class='kpi-card' style='--accent:#c060ff'>
      <div class='kpi-label'>🔌 Réseau</div>
      <div class='kpi-value' style='color:#c060ff'>-0.85 <span style='font-size:1rem'>kW</span></div>
      <div class='kpi-sub'>Importation</div>
      <div class='kpi-badge-neg'>+0.2 kW vs hier</div>
    </div>
    """, unsafe_allow_html=True)
    fig = sparkline(net, "#c060ff")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with k5:
    # Autonomy donut
    aut_fig = go.Figure(go.Pie(
        values=[72, 28], hole=0.72,
        marker=dict(colors=["#4af0c8", "#1a3050"]),
        textinfo="none",
    ))
    aut_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=0,b=0), height=120,
        annotations=[dict(text="<b>72%</b>", x=0.5, y=0.5, font=dict(size=22, color="#4af0c8", family="Rajdhani"), showarrow=False)]
    )
    st.markdown("""
    <div class='kpi-card' style='--accent:#4af0c8;height:auto'>
      <div class='kpi-label'>Autonomie</div>
      <div style='font-size:11px;color:#8aa0c0'>Auto-consommation (PV→Charge)</div>
    </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(aut_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("<div style='text-align:center;font-size:11px;color:#4af0c8;margin-top:-10px'>✅ Objectif : 70%</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ─── MAIN ROW: FLUX + RIGHT PANELS ──────────────────────────────────────────────
col_main, col_right = st.columns([2.2, 1])

with col_main:
    # ── REAL-TIME ENERGY FLOW ────────────────────────────────────────────────────
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0d1b30,#0a1525);border:1px solid #1c3055;
                border-radius:12px;padding:16px;margin-bottom:10px'>
      <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:12px'>
        <div class='section-title' style='margin-bottom:0'>⚡ FLUX D'ÉNERGIE EN TEMPS RÉEL</div>
        <div style='font-size:11px;color:#6080a0'>
          <span style='color:#4af0c8'>━</span> Production &nbsp;
          <span style='color:#ffd060'>━</span> Consommation &nbsp;
          <span style='color:#60b8ff'>━</span> Stockage &nbsp;
          <span style='color:#c060ff'>━</span> Réseau
        </div>
      </div>
      <div style='display:grid;grid-template-columns:1fr 0.8fr 1fr;gap:16px;align-items:center'>

        <!-- PV -->
        <div style='text-align:center;background:linear-gradient(135deg,#0a2010,#0d1b30);
                    border:1px solid #1a4020;border-radius:12px;padding:16px'>
          <div style='font-size:11px;color:#4af0c8;text-transform:uppercase;letter-spacing:1px'>PANNEAUX PV</div>
          <div style='font-size:36px;margin:6px 0'>☀️</div>
          <div style='font-family:Rajdhani,sans-serif;font-size:2rem;font-weight:700;color:#4af0c8'>2.45 kW</div>
          <div style='font-size:11px;color:#4af0c8'>18.7 kWh aujourd'hui</div>
        </div>

        <!-- ONDULEUR -->
        <div style='display:flex;flex-direction:column;align-items:center;gap:8px'>
          <div style='font-size:20px;color:#4af0c8;letter-spacing:2px'>→→→</div>
          <div style='text-align:center;background:linear-gradient(135deg,#0d1b30,#0a2030);
                      border:2px solid #1a3a60;border-radius:12px;padding:14px 20px'>
            <div style='font-size:20px'>⚡</div>
            <div style='font-size:12px;color:#8aa0c0;text-transform:uppercase;letter-spacing:1px'>ONDULEUR</div>
            <div style='font-family:Rajdhani,sans-serif;font-size:1.5rem;font-weight:700;color:#60b8ff'>97%</div>
          </div>
          <div style='font-size:11px;color:#6080a0'>↓ 0.85 kW ↓</div>
          <div style='text-align:center;background:linear-gradient(135deg,#0a1530,#0d1b30);
                      border:1px solid #1a3055;border-radius:12px;padding:12px 16px'>
            <div style='font-size:18px'>🔋</div>
            <div style='font-size:11px;color:#60b8ff;text-transform:uppercase;letter-spacing:1px'>BATTERIE</div>
            <div style='font-family:Rajdhani,sans-serif;font-size:1.4rem;font-weight:700;color:#60b8ff'>80%</div>
            <div style='font-size:10px;color:#8aa0c0'>48.0 V &nbsp; 40.0 A</div>
            <div style='font-size:10px;color:#60b8ff'>4.4 kWh stockés</div>
          </div>
        </div>

        <!-- CHARGE + RESEAU -->
        <div style='display:flex;flex-direction:column;gap:10px'>
          <div style='display:flex;align-items:center;gap:8px'>
            <div style='font-size:16px;color:#ffd060'>→</div>
            <div style='flex:1;text-align:center;background:linear-gradient(135deg,#201a00,#1a1500);
                        border:1px solid #403000;border-radius:12px;padding:12px'>
              <div style='font-size:22px'>🏠</div>
              <div style='font-size:10px;color:#ffd060;text-transform:uppercase;letter-spacing:1px'>CHARGE</div>
              <div style='font-family:Rajdhani,sans-serif;font-size:1.6rem;font-weight:700;color:#ffd060'>1.60 kW</div>
              <div style='font-size:10px;color:#ffd060'>14.3 kWh aujourd'hui</div>
            </div>
          </div>
          <div style='display:flex;align-items:center;gap:8px'>
            <div style='font-size:16px;color:#c060ff'>→</div>
            <div style='flex:1;text-align:center;background:linear-gradient(135deg,#150a25,#100820);
                        border:1px solid #302040;border-radius:12px;padding:12px'>
              <div style='font-size:22px'>🔌</div>
              <div style='font-size:10px;color:#c060ff;text-transform:uppercase;letter-spacing:1px'>RÉSEAU</div>
              <div style='font-family:Rajdhani,sans-serif;font-size:1.6rem;font-weight:700;color:#c060ff'>-0.85 kW</div>
              <div style='font-size:10px;color:#c060ff'>Importation</div>
            </div>
          </div>
        </div>

      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PERFORMANCE CHART ────────────────────────────────────────────────────────
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0d1b30,#0a1525);border:1px solid #1c3055;
                border-radius:12px;padding:16px'>
      <div class='section-title'>📈 PERFORMANCE DU SYSTÈME</div>
    """, unsafe_allow_html=True)

    perf_fig = go.Figure()
    perf_fig.add_trace(go.Scatter(
        x=hours, y=prod_data, name="Production PV",
        line=dict(color="#4af0c8", width=2), fill="tozeroy",
        fillcolor="rgba(74,240,200,0.08)"
    ))
    perf_fig.add_trace(go.Scatter(
        x=hours, y=cons_data, name="Consommation",
        line=dict(color="#ffd060", width=2)
    ))
    stor = np.sin(np.linspace(0, 2*np.pi, 24)) * 0.5
    perf_fig.add_trace(go.Scatter(
        x=hours, y=stor, name="Stockage",
        line=dict(color="#60b8ff", width=1.5)
    ))
    net2 = cons_data - prod_data
    perf_fig.add_trace(go.Scatter(
        x=hours, y=net2, name="Réseau",
        line=dict(color="#c060ff", width=1.5)
    ))
    perf_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=10, t=10, b=30), height=180,
        xaxis=dict(
            gridcolor="#12203a", color="#6080a0",
            tickformat="%H:%M", showline=False, zeroline=False,
        ),
        yaxis=dict(
            gridcolor="#12203a", color="#6080a0",
            zeroline=True, zerolinecolor="#1c3055", title="kW",
            title_font=dict(size=10, color="#6080a0"),
        ),
        legend=dict(
            orientation="h", y=-0.2, x=0,
            font=dict(size=10, color="#8aa0c0"),
            bgcolor="rgba(0,0,0,0)",
        )
    )
    st.plotly_chart(perf_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    # ── RÉPARTITION ÉNERGÉTIQUE ──────────────────────────────────────────────────
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0d1b30,#0a1525);border:1px solid #1c3055;
                border-radius:12px;padding:14px;margin-bottom:10px'>
      <div class='section-title'>🥧 RÉPARTITION ÉNERGÉTIQUE</div>
    """, unsafe_allow_html=True)

    rep_fig = go.Figure(go.Pie(
        values=[54, 28, 18],
        labels=["Production PV", "Consommation", "Stockage"],
        hole=0.55,
        marker=dict(colors=["#4af0c8", "#ffd060", "#60b8ff"],
                    line=dict(color="#080e1a", width=2)),
        textinfo="none",
    ))
    rep_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=0,b=0), height=160,
        annotations=[dict(text="<b>18.7</b><br><span style='font-size:10px'>kWh</span>",
                          x=0.5, y=0.5, font=dict(size=16, color="#e0e8f8", family="Rajdhani"), showarrow=False)],
        legend=dict(orientation="v", x=0.72, y=0.5,
                    font=dict(size=10, color="#8aa0c0"), bgcolor="rgba(0,0,0,0)")
    )
    st.plotly_chart(rep_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    # ── ANALYSE QUOTIDIENNE ──────────────────────────────────────────────────────
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0d1b30,#0a1525);border:1px solid #1c3055;
                border-radius:12px;padding:14px;margin-bottom:10px'>
      <div class='section-title'>📊 ANALYSE QUOTIDIENNE</div>
    """, unsafe_allow_html=True)

    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(x=list(range(24)), y=prod_data, name="Production",
                             marker_color="#4af0c8", opacity=0.85))
    bar_fig.add_trace(go.Bar(x=list(range(24)), y=cons_data, name="Consommation",
                             marker_color="#ffd060", opacity=0.85))
    bar_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=5, t=5, b=20), height=130, barmode="group",
        xaxis=dict(gridcolor="#12203a", color="#6080a0", tickfont=dict(size=8)),
        yaxis=dict(gridcolor="#12203a", color="#6080a0", title="kWh",
                   title_font=dict(size=8, color="#6080a0")),
        legend=dict(orientation="h", y=1.15, font=dict(size=9, color="#8aa0c0"),
                    bgcolor="rgba(0,0,0,0)"),
        bargap=0.1,
    )
    st.plotly_chart(bar_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    # ── APPAREILS CONNECTÉS ──────────────────────────────────────────────────────
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0d1b30,#0a1525);border:1px solid #1c3055;
                border-radius:12px;padding:14px'>
      <div class='section-title'>📱 APPAREILS CONNECTÉS</div>
      <div class='device-row'>
        <span>⚡ Onduleur</span>
        <span><span class='online'>En ligne</span> &nbsp;<span style='font-family:Rajdhani;color:#60b8ff'>2.45 kW</span></span>
      </div>
      <div class='device-row'>
        <span>🔋 Batterie</span>
        <span><span class='online'>En ligne</span> &nbsp;<span style='font-family:Rajdhani;color:#60b8ff'>0.85 kW</span></span>
      </div>
      <div class='device-row'>
        <span>📊 Smart Meter</span>
        <span><span class='online'>En ligne</span> &nbsp;<span style='font-family:Rajdhani;color:#c060ff'>-0.85 kW</span></span>
      </div>
      <div class='device-row'>
        <span>☀️ Panneaux PV</span>
        <span><span class='online'>En ligne</span> &nbsp;<span style='font-family:Rajdhani;color:#4af0c8'>2.45 kW</span></span>
      </div>
      <div class='device-row' style='border-bottom:none'>
        <span>🏠 Charge Principale</span>
        <span><span class='online'>En ligne</span> &nbsp;<span style='font-family:Rajdhani;color:#ffd060'>1.60 kW</span></span>
      </div>
      <div style='margin-top:10px;text-align:center'>
        <div style='background:#12203a;border-radius:6px;padding:6px 12px;
                    font-size:11px;color:#60b8ff;cursor:pointer'>
          Voir tous les appareils →
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─── BILAN ROW ───────────────────────────────────────────────────────────────────
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

_, col_bilan, _ = st.columns([2.2, 1, 0.001])

with col_bilan:
    # We need to show bilan beside performance chart
    pass

# Redo layout: perf chart left, bilan center-right
# Actually inject bilan inline with the charts row
col_perf2, col_bilan2 = st.columns([1, 1])

# We already drew perf above, so let's add bilan in col_bilan2
with col_bilan2:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0d1b30,#0a1525);border:1px solid #1c3055;
                border-radius:12px;padding:16px'>
      <div class='section-title'>💰 BILAN ÉNERGÉTIQUE — AUJOURD'HUI</div>
      <div class='bilan-row'>
        <span style='color:#4af0c8'>⚡ Énergie produite</span>
        <span class='bilan-val' style='color:#4af0c8'>18.7 kWh</span>
      </div>
      <div class='bilan-row'>
        <span style='color:#ffd060'>🏠 Énergie consommée</span>
        <span class='bilan-val' style='color:#ffd060'>14.3 kWh</span>
      </div>
      <div class='bilan-row'>
        <span style='color:#60b8ff'>🔋 Énergie stockée</span>
        <span class='bilan-val' style='color:#60b8ff'>4.4 kWh</span>
      </div>
      <div class='bilan-row'>
        <span style='color:#c060ff'>🔌 Énergie importée</span>
        <span class='bilan-val' style='color:#c060ff'>2.1 kWh</span>
      </div>
      <div class='bilan-row' style='border-bottom:none'>
        <span style='color:#8aa0c0'>📤 Énergie exportée</span>
        <span class='bilan-val' style='color:#8aa0c0'>0.0 kWh</span>
      </div>
      <div style='display:flex;justify-content:space-between;align-items:center;
                  margin-top:12px;background:#0a2018;border-radius:8px;padding:10px 14px'>
        <span style='font-size:13px;color:#4af0c8'>⟳ Auto-consommation</span>
        <span style='font-family:Rajdhani,sans-serif;font-size:1.8rem;font-weight:700;color:#4af0c8'>72%</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─── FOOTER BAR ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer-bar'>
  <div style='display:flex;align-items:center;gap:12px'>
    <div style='width:36px;height:36px;background:linear-gradient(135deg,#00cc66,#004422);
                border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px'>✅</div>
    <div>
      <div style='font-family:Rajdhani,sans-serif;font-weight:700;color:#4af0c8;font-size:14px'>SYSTÈME SAIN</div>
      <div style='font-size:11px;color:#6080a0'>Aucune alarme active</div>
    </div>
  </div>

  <div class='footer-item'>
    <div style='font-size:11px;color:#6080a0;text-transform:uppercase;letter-spacing:1px'>🌿 Émissions CO₂ évitées</div>
    <div class='footer-val' style='color:#4af0c8'>12.6 <span style='font-size:1rem'>kg</span></div>
    <div style='font-size:10px;color:#6080a0'>Aujourd'hui</div>
  </div>

  <div class='footer-item'>
    <div style='font-size:11px;color:#6080a0;text-transform:uppercase;letter-spacing:1px'>🌳 Équivalent arbres plantés</div>
    <div class='footer-val' style='color:#4af0c8'>0.6</div>
    <div style='font-size:10px;color:#6080a0'>Aujourd'hui</div>
  </div>

  <div class='footer-item'>
    <div style='font-size:11px;color:#6080a0;text-transform:uppercase;letter-spacing:1px'>💰 Économie réalisée</div>
    <div class='footer-val' style='color:#ffd060'>2.35 <span style='font-size:1rem'>€</span></div>
    <div style='font-size:10px;color:#6080a0'>Aujourd'hui</div>
  </div>
</div>
""", unsafe_allow_html=True)
