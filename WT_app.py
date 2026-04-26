import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(
    page_title="Digital Twin – Smart Energy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Style CSS moderne sans emojis
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f5f7fb;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e5e9f0;
    padding: 1rem;
}

/* Main content */
[data-testid="stAppViewContainer"] > .main {
    background: #f5f7fb;
}

/* Remove default Streamlit elements */
#MainMenu, footer, [data-testid="stToolbar"] {
    visibility: hidden;
}

.block-container {
    padding: 1rem 2rem !important;
    max-width: 1400px;
}

/* Card styling */
.card {
    background: white;
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    border: 1px solid #e5e9f0;
}

.card-title {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #8b9eb0;
    margin-bottom: 1rem;
}

/* KPI cards */
.kpi-card {
    background: white;
    border-radius: 12px;
    padding: 1rem;
    border-left: 3px solid;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    margin-bottom: 0.5rem;
}

.kpi-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #8b9eb0;
}

.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    margin: 0.25rem 0;
}

.kpi-sub {
    font-size: 0.7rem;
    color: #6b7f92;
}

.kpi-badge {
    font-size: 0.65rem;
    font-weight: 600;
    margin-top: 0.25rem;
}

.badge-up {
    color: #10b981;
}

.badge-down {
    color: #ef4444;
}

/* Progress bar */
.progress-bar {
    background: #e5e9f0;
    border-radius: 4px;
    height: 6px;
    margin-top: 0.5rem;
}

.progress-fill {
    background: #3b82f6;
    border-radius: 4px;
    height: 100%;
}

/* Stats row */
.stat-row {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid #f0f2f5;
    font-size: 0.8rem;
}

.stat-label {
    color: #6b7f92;
}

.stat-value {
    font-weight: 600;
    color: #1a2c3e;
}

/* Device row */
.device-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid #f0f2f5;
    font-size: 0.85rem;
}

.device-name {
    color: #1a2c3e;
}

.device-status {
    color: #10b981;
    font-size: 0.7rem;
}

.device-value {
    font-weight: 600;
    color: #1a2c3e;
}

/* Flow diagram */
.flow-node {
    text-align: center;
    padding: 1rem;
    background: #f8fafc;
    border-radius: 10px;
    border: 1px solid #e5e9f0;
}

.flow-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #8b9eb0;
    margin-bottom: 0.25rem;
}

.flow-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1a2c3e;
}

.flow-sub {
    font-size: 0.65rem;
    color: #6b7f92;
    margin-top: 0.25rem;
}

/* Flex layouts */
.flex-between {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.flex-center {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Donut chart placeholder */
.donut-placeholder {
    width: 100px;
    height: 100px;
    margin: 0 auto;
    position: relative;
}

/* Footer stats */
.footer-stats {
    background: white;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-top: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid #e5e9f0;
}

.footer-item {
    text-align: center;
}

.footer-label {
    font-size: 0.65rem;
    text-transform: uppercase;
    color: #8b9eb0;
    letter-spacing: 1px;
}

.footer-value {
    font-size: 1.2rem;
    font-weight: 700;
    color: #1a2c3e;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# DONNEES STATIQUES
# ============================================

# Meteo
weather = {
    "temp": "27°C",
    "condition": "Ensoleille",
    "solar": "800 W/m²",
    "humidity": "45 %",
    "wind": "12 km/h"
}

# KPI Principaux
kpi_data = {
    "production": {"value": "2.45", "unit": "kW", "daily": "18.7 kWh", "trend": "+12%", "trend_up": True},
    "battery": {"percent": 80, "voltage": "48.0 V", "current": "40.0 A", "stored": "4.4 kWh"},
    "consumption": {"value": "1.60", "unit": "kW", "daily": "14.3 kWh", "trend": "+8%", "trend_up": True},
    "grid": {"value": "-0.85", "unit": "kW", "status": "Importation", "trend": "+0.2 kW", "trend_up": True}
}

# Donnees graphiques
hours = list(range(24))
prod_data = [0.2, 0.15, 0.1, 0.08, 0.05, 0.1, 0.3, 0.8, 1.5, 2.2, 2.6, 2.8, 2.7, 2.5, 2.3, 2.0, 1.6, 1.2, 0.8, 0.5, 0.3, 0.2, 0.15, 0.1]
cons_data = [0.8, 0.7, 0.65, 0.6, 0.7, 0.9, 1.2, 1.5, 1.4, 1.3, 1.2, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.7, 1.4, 1.1, 0.9]

# Bilan energetique
bilan = {
    "produite": "18.7 kWh",
    "consommee": "14.3 kWh",
    "stockee": "4.4 kWh",
    "importee": "2.1 kWh",
    "exportee": "0.0 kWh"
}

# Appareils
devices = [
    {"name": "Onduleur", "status": "En ligne", "value": "2.45 kW"},
    {"name": "Batterie", "status": "En ligne", "value": "0.85 kW"},
    {"name": "Smart Meter", "status": "En ligne", "value": "-0.85 kW"},
    {"name": "Panneaux PV", "status": "En ligne", "value": "2.45 kW"},
    {"name": "Charge Principale", "status": "En ligne", "value": "1.60 kW"}
]

# ============================================
# FONCTIONS DE GRAPHIQUES
# ============================================

def make_line_chart(y_data, color, height=100):
    df = pd.DataFrame({"x": hours, "y": y_data})
    return alt.Chart(df).mark_line(
        color=color,
        strokeWidth=2
    ).encode(
        x=alt.X("x:Q", axis=None),
        y=alt.Y("y:Q", axis=None)
    ).properties(
        height=height,
        background="transparent"
    ).configure_view(strokeWidth=0)

def make_performance_chart():
    df = pd.DataFrame({
        "Heure": hours * 4,
        "kW": prod_data + cons_data + [0.5, 0.4, 0.3, 0.2, 0.1, 0, -0.1, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0] + [-0.85] * 24,
        "Serie": (["Production PV"]*24 + ["Consommation"]*24 + ["Stockage"]*24 + ["Reseau"]*24)
    })
    
    color_scale = alt.Scale(
        domain=["Production PV", "Consommation", "Stockage", "Reseau"],
        range=["#10b981", "#f59e0b", "#3b82f6", "#8b5cf6"]
    )
    
    return alt.Chart(df).mark_line(strokeWidth=2).encode(
        x=alt.X("Heure:Q", axis=alt.Axis(title="Heure", format="d", tickCount=6)),
        y=alt.Y("kW:Q", axis=alt.Axis(title="kW")),
        color=alt.Color("Serie:N", scale=color_scale, legend=alt.Legend(orient="bottom"))
    ).properties(height=200, background="transparent").configure_view(strokeWidth=0)

def make_bar_chart():
    df = pd.DataFrame({
        "Heure": hours * 2,
        "kWh": prod_data + cons_data,
        "Serie": ["Production"]*24 + ["Consommation"]*24
    })
    
    color_scale = alt.Scale(domain=["Production", "Consommation"], range=["#10b981", "#f59e0b"])
    
    return alt.Chart(df).mark_bar(opacity=0.8, size=15).encode(
        x=alt.X("Heure:O", axis=alt.Axis(title="Heure", tickCount=6)),
        y=alt.Y("kWh:Q", axis=alt.Axis(title="kWh")),
        color=alt.Color("Serie:N", scale=color_scale, legend=alt.Legend(orient="top")),
        xOffset="Serie:N"
    ).properties(height=150, background="transparent").configure_view(strokeWidth=0)

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("### DIGITAL TWIN")
    st.markdown("#### SMART ENERGY")
    st.markdown("---")
    
    # Menu
    menu_items = ["Apercu", "Flux d'energie", "Appareils", "Stockage", "Historique", "Analyses", "Alarmes", "Scenarios"]
    selected = st.radio("", menu_items, index=0, label_visibility="collapsed")
    
    st.markdown("---")
    
    # Meteo
    st.markdown("#### METEO ACTUELLE")
    st.markdown(f"**{weather['temp']}**")
    st.markdown(f"*{weather['condition']}*")
    st.markdown(f"☀️ Irradiation solaire: {weather['solar']}")
    st.markdown(f"💧 Humidite: {weather['humidity']}")
    st.markdown(f"💨 Vent: {weather['wind']}")
    
    # Previsions
    col1, col2, col3 = st.columns(3)
    col1.markdown("**MAR**\n🌤\n28/16°")
    col2.markdown("**MER**\n☀️\n27/15°")
    col3.markdown("**JEU**\n🌤\n26/14°")

# ============================================
# TOP BAR
# ============================================

st.markdown("""
<div style="background: white; border-radius: 12px; padding: 0.75rem 1.5rem; margin-bottom: 1.5rem; border: 1px solid #e5e9f0;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <strong style="font-size: 1rem;">DIGITAL TWIN - SMART ENERGY</strong>
            <div style="font-size: 0.7rem; color: #8b9eb0;">Surveillance & Optimisation en temps reel</div>
        </div>
        <div style="display: flex; gap: 2rem;">
            <div>
                <div style="font-size: 0.7rem; color: #8b9eb0;">Mode de fonctionnement</div>
                <div style="font-size: 0.8rem; font-weight: 600; color: #10b981;">AUTONOME</div>
            </div>
            <div>
                <div style="font-size: 0.7rem; color: #8b9eb0;">Statut systeme</div>
                <div style="font-size: 0.8rem; font-weight: 600; color: #10b981;">NORMAL</div>
            </div>
            <div>
                <div style="font-size: 0.7rem; color: #8b9eb0;">Derniere mise a jour</div>
                <div style="font-size: 0.8rem; font-weight: 600; color: #ef4444;">10:24:35 LIVE</div>
            </div>
        </div>
        <div style="font-size: 0.75rem; color: #8b9eb0;">📅 19 Mai 2024 🕐 10:24 🔔 ⚙</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# KPI ROW
# ============================================

col1, col2, col3, col4, col5 = st.columns([1.2, 1.2, 1.2, 1.2, 0.8])

with col1:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #10b981;">
        <div class="kpi-label">PRODUCTION PV</div>
        <div class="kpi-value" style="color: #10b981;">{kpi_data['production']['value']} <span style="font-size: 0.9rem;">{kpi_data['production']['unit']}</span></div>
        <div class="kpi-sub">Aujourd'hui: {kpi_data['production']['daily']}</div>
        <div class="kpi-badge badge-up">▲ {kpi_data['production']['trend']} vs hier</div>
    </div>
    """, unsafe_allow_html=True)
    st.altair_chart(make_line_chart(prod_data, "#10b981", 60), use_container_width=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #3b82f6;">
        <div class="kpi-label">BATTERIE</div>
        <div class="kpi-value" style="color: #3b82f6;">{kpi_data['battery']['percent']} <span style="font-size: 0.9rem;">%</span></div>
        <div class="kpi-sub">{kpi_data['battery']['voltage']} | {kpi_data['battery']['current']}</div>
        <div class="kpi-sub">Energie stockee: {kpi_data['battery']['stored']}</div>
        <div class="progress-bar"><div class="progress-fill" style="width: {kpi_data['battery']['percent']}%; background: #3b82f6;"></div></div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #f59e0b;">
        <div class="kpi-label">CONSOMMATION</div>
        <div class="kpi-value" style="color: #f59e0b;">{kpi_data['consumption']['value']} <span style="font-size: 0.9rem;">{kpi_data['consumption']['unit']}</span></div>
        <div class="kpi-sub">Aujourd'hui: {kpi_data['consumption']['daily']}</div>
        <div class="kpi-badge badge-up">▲ {kpi_data['consumption']['trend']} vs hier</div>
    </div>
    """, unsafe_allow_html=True)
    st.altair_chart(make_line_chart(cons_data, "#f59e0b", 60), use_container_width=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #8b5cf6;">
        <div class="kpi-label">RESEAU</div>
        <div class="kpi-value" style="color: #8b5cf6;">{kpi_data['grid']['value']} <span style="font-size: 0.9rem;">{kpi_data['grid']['unit']}</span></div>
        <div class="kpi-sub">{kpi_data['grid']['status']}</div>
        <div class="kpi-badge badge-up">▲ {kpi_data['grid']['trend']} vs hier</div>
    </div>
    """, unsafe_allow_html=True)
    st.altair_chart(make_line_chart([-0.85]*24, "#8b5cf6", 60), use_container_width=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #10b981; text-align: center;">
        <div class="kpi-label">AUTONOMIE</div>
        <div style="margin: 0.5rem 0;">
            <svg width="90" height="90" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" fill="none" stroke="#e5e9f0" stroke-width="12"/>
                <circle cx="50" cy="50" r="40" fill="none" stroke="#10b981" stroke-width="12"
                    stroke-dasharray="{(2*3.14159*40)*0.72} {(2*3.14159*40)*0.28}"
                    stroke-linecap="round" transform="rotate(-90 50 50)"/>
                <text x="50" y="55" text-anchor="middle" fill="#1a2c3e" font-size="20" font-weight="700">72%</text>
            </svg>
        </div>
        <div class="kpi-sub">Auto-consommation (PV → Charge)</div>
        <div class="kpi-badge badge-up">Objectif: 70%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

# ============================================
# MIDDLE SECTION
# ============================================

left_col, right_col = st.columns([2.2, 1.2])

with left_col:
    # Flux d'energie
    st.markdown("""
    <div class="card">
        <div class="flex-between">
            <div class="card-title">FLUX D'ENERGIE EN TEMPS REEL</div>
            <div style="font-size: 0.7rem; color: #8b9eb0;">Vue: Schema ▾</div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1.5fr 1fr; gap: 1rem; align-items: center;">
            <div class="flow-node">
                <div style="font-size: 1.5rem;">☀️</div>
                <div class="flow-label">PANNEAUX PV</div>
                <div class="flow-value">2.45 kW</div>
                <div class="flow-sub">18.7 kWh aujourd'hui</div>
            </div>
            <div style="text-align: center;">
                <div class="flow-node" style="margin-bottom: 0.5rem;">
                    <div>⚡</div>
                    <div class="flow-label">ONDULEUR</div>
                    <div class="flow-value">97%</div>
                </div>
                <div style="margin: 0.5rem 0;">0.85 kW ↓</div>
                <div class="flow-node">
                    <div>🔋</div>
                    <div class="flow-label">BATTERIE</div>
                    <div class="flow-value">80%</div>
                    <div class="flow-sub">48.0 V | 40.0 A</div>
                    <div class="flow-sub">4.4 kWh stockés</div>
                </div>
            </div>
            <div>
                <div class="flow-node" style="margin-bottom: 0.5rem;">
                    <div>🏠</div>
                    <div class="flow-label">CHARGE</div>
                    <div class="flow-value">1.60 kW</div>
                    <div class="flow-sub">14.3 kWh aujourd'hui</div>
                </div>
                <div class="flow-node">
                    <div>🔌</div>
                    <div class="flow-label">RESEAU</div>
                    <div class="flow-value">-0.85 kW</div>
                    <div class="flow-sub">Importation</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Performance chart
    st.markdown('<div class="card"><div class="card-title">PERFORMANCE DU SYSTEME</div>', unsafe_allow_html=True)
    tabs = st.tabs(["Jour", "Semaine", "Mois", "Annee"])
    with tabs[0]:
        st.altair_chart(make_performance_chart(), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    # Repartition
    st.markdown("""
    <div class="card">
        <div class="card-title">REPARTITION ENERGETIQUE</div>
        <div class="flex-center" style="justify-content: center; gap: 1rem;">
            <svg width="120" height="120" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="#f8fafc"/>
                <path d="M50 5 A45 45 0 0 1 86.5 32.5 L50 50 Z" fill="#10b981"/>
                <path d="M86.5 32.5 A45 45 0 0 1 32.5 86.5 L50 50 Z" fill="#f59e0b"/>
                <path d="M32.5 86.5 A45 45 0 0 1 50 5 L50 50 Z" fill="#3b82f6"/>
                <circle cx="50" cy="50" r="25" fill="white"/>
            </svg>
            <div>
                <div style="font-size: 0.75rem;"><span style="color:#10b981;">●</span> Production PV (54%)</div>
                <div style="font-size: 0.75rem;"><span style="color:#f59e0b;">●</span> Consommation (28%)</div>
                <div style="font-size: 0.75rem;"><span style="color:#3b82f6;">●</span> Stockage (18%)</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Analyse quotidienne
    st.markdown('<div class="card"><div class="card-title">ANALYSE QUOTIDIENNE</div>', unsafe_allow_html=True)
    st.altair_chart(make_bar_chart(), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Appareils
    st.markdown('<div class="card"><div class="card-title">APPAREILS CONNECTES</div>', unsafe_allow_html=True)
    for device in devices:
        st.markdown(f"""
        <div class="device-row">
            <span class="device-name">{device['name']}</span>
            <span><span class="device-status">{device['status']}</span> <span class="device-value">{device['value']}</span></span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; margin-top: 0.75rem; padding: 0.5rem; background: #f8fafc; border-radius: 8px; font-size: 0.75rem; color: #3b82f6;">Voir tous les appareils ›</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# BOTTOM SECTION - BILAN
# ============================================

_, bilan_col = st.columns([2.2, 1.2])

with bilan_col:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">BILAN ENERGETIQUE <span style="font-size: 0.6rem;">(AUJOURD'HUI)</span></div>
        <div class="stat-row">
            <span class="stat-label">⚡ Energie produite</span>
            <span class="stat-value">{bilan['produite']}</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">🏠 Energie consommee</span>
            <span class="stat-value">{bilan['consommee']}</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">🔋 Energie stockee</span>
            <span class="stat-value">{bilan['stockee']}</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">🔌 Energie importee</span>
            <span class="stat-value">{bilan['importee']}</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">📤 Energie exportee</span>
            <span class="stat-value">{bilan['exportee']}</span>
        </div>
        <div style="background: #f0fdf4; border-radius: 8px; padding: 0.75rem; margin-top: 0.75rem; display: flex; justify-content: space-between;">
            <span style="font-size: 0.8rem; color: #10b981;">⟳ Auto-consommation</span>
            <span style="font-size: 1.5rem; font-weight: 700; color: #10b981;">72%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================

st.markdown("""
<div class="footer-stats">
    <div class="flex-center">
        <div style="width: 2rem; height: 2rem; background: #f0fdf4; border-radius: 50%; display: flex; align-items: center; justify-content: center;">✓</div>
        <div><strong>SYSTEME SAIN</strong><br><span style="font-size: 0.7rem; color: #8b9eb0;">Aucune alarme active</span></div>
    </div>
    <div class="footer-item">
        <div class="footer-label">Emissions CO2 evitees</div>
        <div class="footer-value">12.6 kg</div>
        <div class="footer-label">Aujourd'hui</div>
    </div>
    <div class="footer-item">
        <div class="footer-label">Equivalent arbres plantes</div>
        <div class="footer-value">0.6</div>
        <div class="footer-label">Aujourd'hui</div>
    </div>
    <div class="footer-item">
        <div class="footer-label">Economie realisee</div>
        <div class="footer-value">2.35 €</div>
        <div class="footer-label">Aujourd'hui</div>
    </div>
</div>
""", unsafe_allow_html=True)
