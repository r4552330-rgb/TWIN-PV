"""
Digital Twin — Smart Energy Dashboard
A futuristic real-time energy flow monitoring system
"""

import streamlit as st
import random
import time
import math

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Digital Twin · Smart Energy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# SIMULATE REAL-TIME DATA
# ─────────────────────────────────────────────────────────────
def get_energy_data():
    hour = (time.localtime().tm_hour + time.localtime().tm_min / 60)
    # Solar follows a bell curve peaking at noon
    solar_factor = max(0, math.sin(math.pi * (hour - 6) / 14)) if 6 <= hour <= 20 else 0
    pv_power     = round(solar_factor * 3.5 + random.uniform(-0.1, 0.1), 2)
    battery_pct  = random.randint(70, 95)
    battery_kwh  = round(battery_pct * 5.0 / 100, 1)
    load_power   = round(random.uniform(1.2, 2.4), 2)
    inverter_eff = random.randint(95, 99)
    inverter_out = round(pv_power * inverter_eff / 100, 2)
    grid_power   = round(load_power - inverter_out, 2)  # negative = export
    pv_to_bat    = round(max(0, inverter_out - load_power), 2)
    bat_to_load  = round(max(0, load_power - inverter_out - max(0, grid_power)), 2)
    co2_saved    = round(pv_power * 0.233, 1)
    trees        = round(co2_saved / 21.77, 1)
    savings      = round(pv_power * 0.18, 2)
    autoconsumption = round(min(100, (inverter_out / max(load_power, 0.01)) * 100), 1)

    return {
        "pv_power": pv_power,
        "pv_daily": round(pv_power * 8.2, 1),
        "inverter_eff": inverter_eff,
        "inverter_out": inverter_out,
        "battery_pct": battery_pct,
        "battery_kwh": battery_kwh,
        "load_power": load_power,
        "load_daily": round(load_power * 8.9, 1),
        "grid_power": grid_power,
        "pv_to_bat": pv_to_bat,
        "bat_to_load": bat_to_load,
        "co2_saved": co2_saved,
        "trees": trees,
        "savings": savings,
        "autoconsumption": autoconsumption,
        "pv_share": round(min(100, (pv_power / max(load_power, 0.01)) * 100 * 0.5), 1),
        "bat_share": round(bat_to_load / max(load_power, 0.01) * 100, 1),
        "grid_share": round(max(0, grid_power) / max(load_power, 0.01) * 100, 1),
    }

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS + ANIMATIONS
# ─────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;800&display=swap');

    /* ── ROOT VARS ── */
    :root {
        --bg:        #020617;
        --bg2:       #0a1628;
        --bg3:       #0f1f35;
        --green:     #00ff88;
        --green2:    #00cc6a;
        --yellow:    #ffd700;
        --yellow2:   #ffb800;
        --blue:      #00b4ff;
        --blue2:     #0080cc;
        --purple:    #c084fc;
        --purple2:   #9333ea;
        --red:       #ff4444;
        --text:      #e2e8f0;
        --muted:     #64748b;
        --card-bg:   rgba(10, 22, 40, 0.85);
        --card-border: rgba(0,255,136,0.15);
    }

    /* ── RESET ── */
    .stApp { background: var(--bg) !important; font-family: 'Exo 2', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 0.5rem 1rem !important; max-width: 100% !important; }
    section[data-testid="stSidebar"] { display: none; }

    /* ── GRID BACKGROUND ── */
    .stApp::before {
        content: '';
        position: fixed; inset: 0; z-index: 0; pointer-events: none;
        background-image:
            linear-gradient(rgba(0,255,136,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,255,136,0.03) 1px, transparent 1px);
        background-size: 40px 40px;
    }

    /* ── TOP HEADER BAR ── */
    .header-bar {
        display: flex; align-items: center; justify-content: space-between;
        background: linear-gradient(135deg, rgba(10,22,40,0.95), rgba(15,31,53,0.95));
        border: 1px solid rgba(0,255,136,0.2);
        border-radius: 12px; padding: 12px 24px; margin-bottom: 12px;
        backdrop-filter: blur(20px);
        box-shadow: 0 0 30px rgba(0,255,136,0.08), inset 0 1px 0 rgba(255,255,255,0.05);
    }
    .header-brand { display: flex; align-items: center; gap: 12px; }
    .brand-icon {
        width: 42px; height: 42px; background: linear-gradient(135deg, #00ff88, #00b4ff);
        border-radius: 10px; display: flex; align-items: center; justify-content: center;
        font-size: 22px; box-shadow: 0 0 20px rgba(0,255,136,0.4);
        animation: pulse-icon 2s ease-in-out infinite;
    }
    @keyframes pulse-icon {
        0%,100% { box-shadow: 0 0 20px rgba(0,255,136,0.4); }
        50%      { box-shadow: 0 0 35px rgba(0,255,136,0.7); }
    }
    .brand-title { font-family: 'Rajdhani', sans-serif; font-size: 22px; font-weight: 700; color: white; letter-spacing: 2px; }
    .brand-title span { color: var(--green); }
    .brand-sub { font-family: 'Share Tech Mono', monospace; font-size: 10px; color: var(--muted); letter-spacing: 1px; }

    .kpi-group { display: flex; gap: 20px; }
    .kpi-pill {
        display: flex; flex-direction: column; align-items: center;
        background: rgba(255,255,255,0.04); border-radius: 10px; padding: 6px 16px;
        border: 1px solid rgba(255,255,255,0.08);
        min-width: 90px;
    }
    .kpi-label { font-family: 'Share Tech Mono', monospace; font-size: 9px; color: var(--muted); letter-spacing: 1px; text-transform: uppercase; }
    .kpi-value { font-family: 'Rajdhani', sans-serif; font-size: 20px; font-weight: 700; line-height: 1.1; }
    .kpi-sub   { font-size: 9px; color: var(--muted); }
    .kv-green  { color: var(--green); text-shadow: 0 0 10px rgba(0,255,136,0.5); }
    .kv-yellow { color: var(--yellow); text-shadow: 0 0 10px rgba(255,215,0,0.5); }
    .kv-blue   { color: var(--blue);   text-shadow: 0 0 10px rgba(0,180,255,0.5); }
    .kv-purple { color: var(--purple); text-shadow: 0 0 10px rgba(192,132,252,0.5); }
    .kv-red    { color: var(--red);    text-shadow: 0 0 10px rgba(255,68,68,0.5); }

    .live-badge {
        display: flex; align-items: center; gap: 6px;
        background: rgba(0,255,136,0.1); border: 1px solid var(--green2);
        border-radius: 20px; padding: 4px 12px; color: var(--green);
        font-family: 'Share Tech Mono', monospace; font-size: 11px; letter-spacing: 2px;
    }
    .live-dot { width: 7px; height: 7px; background: var(--green); border-radius: 50%;
        animation: blink 1.2s ease-in-out infinite; }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

    /* ── COMPONENT CARDS ── */
    .energy-card {
        background: var(--card-bg);
        border-radius: 16px; padding: 16px;
        backdrop-filter: blur(20px);
        position: relative; overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .energy-card:hover { transform: translateY(-3px); }
    .energy-card::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: var(--accent, var(--green));
        box-shadow: 0 0 12px var(--accent, var(--green));
    }
    .card-pv     { border: 1px solid rgba(0,255,136,0.25);  --accent: var(--green);  box-shadow: 0 0 25px rgba(0,255,136,0.06); }
    .card-inv    { border: 1px solid rgba(0,180,255,0.25);  --accent: var(--blue);   box-shadow: 0 0 25px rgba(0,180,255,0.06); }
    .card-bat    { border: 1px solid rgba(0,180,255,0.25);  --accent: var(--blue);   box-shadow: 0 0 25px rgba(0,180,255,0.06); }
    .card-load   { border: 1px solid rgba(255,215,0,0.25);  --accent: var(--yellow); box-shadow: 0 0 25px rgba(255,215,0,0.06); }
    .card-grid   { border: 1px solid rgba(192,132,252,0.25); --accent: var(--purple); box-shadow: 0 0 25px rgba(192,132,252,0.06); }

    .card-icon { text-align: center; margin-bottom: 8px; }
    .card-name { font-family: 'Share Tech Mono', monospace; font-size: 10px; letter-spacing: 2px; color: var(--muted); text-align: center; text-transform: uppercase; margin-bottom: 4px; }
    .card-power { font-family: 'Rajdhani', sans-serif; font-size: 30px; font-weight: 800; text-align: center; line-height: 1; }
    .card-unit  { font-size: 14px; font-weight: 400; margin-left: 3px; }
    .card-meta  { font-family: 'Share Tech Mono', monospace; font-size: 10px; color: var(--muted); text-align: center; margin-top: 4px; }
    .card-status {
        display: inline-flex; align-items: center; gap: 5px;
        border-radius: 20px; padding: 3px 10px; font-size: 9px;
        font-family: 'Share Tech Mono', monospace; letter-spacing: 1px;
        margin: 6px auto 0; display: flex; justify-content: center;
    }
    .status-online  { background: rgba(0,255,136,0.12); color: var(--green); border: 1px solid rgba(0,255,136,0.3); }
    .status-charge  { background: rgba(0,180,255,0.12); color: var(--blue);   border: 1px solid rgba(0,180,255,0.3); }
    .status-active  { background: rgba(255,215,0,0.12); color: var(--yellow); border: 1px solid rgba(255,215,0,0.3); }
    .status-connected { background: rgba(192,132,252,0.12); color: var(--purple); border: 1px solid rgba(192,132,252,0.3); }
    .status-dot { width: 5px; height: 5px; border-radius: 50%; background: currentColor; animation: blink 1.5s infinite; }

    .bat-bar-wrap { background: rgba(255,255,255,0.08); border-radius: 4px; height: 6px; margin-top: 8px; overflow: hidden; }
    .bat-bar      { height: 100%; border-radius: 4px; background: linear-gradient(90deg, var(--blue2), var(--blue));
        box-shadow: 0 0 8px var(--blue); transition: width 0.8s ease; }

    /* ── SVG FLOW CANVAS ── */
    .flow-canvas { position: relative; width: 100%; }
    .flow-canvas svg { overflow: visible; }

    /* ── FLOW LINES ── */
    .flow-pv-inv   { stroke: var(--green);  fill: none; stroke-width: 2.5; stroke-linecap: round;
        filter: drop-shadow(0 0 4px var(--green)); }
    .flow-inv-load { stroke: var(--yellow); fill: none; stroke-width: 2.5; stroke-linecap: round;
        filter: drop-shadow(0 0 4px var(--yellow)); }
    .flow-inv-bat  { stroke: var(--blue);   fill: none; stroke-width: 2.5; stroke-linecap: round;
        filter: drop-shadow(0 0 4px var(--blue)); }
    .flow-grid-load { stroke: var(--purple); fill: none; stroke-width: 2.5; stroke-linecap: round;
        filter: drop-shadow(0 0 4px var(--purple)); }

    @keyframes dash-fwd { to { stroke-dashoffset: -40; } }
    @keyframes dash-rev { to { stroke-dashoffset:  40; } }
    .anim-fwd { animation: dash-fwd 1.2s linear infinite; }
    .anim-fast { animation: dash-fwd 0.6s linear infinite; }
    .anim-rev  { animation: dash-rev 1.2s linear infinite; }

    /* ── FLOW LABEL ── */
    .flow-label {
        font-family: 'Share Tech Mono', monospace; font-size: 10px;
        background: rgba(10,22,40,0.9); padding: 3px 8px; border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.1); color: white; pointer-events: none;
    }

    /* ── RIGHT PANELS ── */
    .panel-card {
        background: var(--card-bg); border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px; padding: 14px 16px; margin-bottom: 10px;
        backdrop-filter: blur(20px);
    }
    .panel-title { font-family: 'Rajdhani', sans-serif; font-size: 13px; font-weight: 600;
        color: var(--muted); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 10px; }

    /* Donut chart */
    .donut-wrap { display: flex; align-items: center; gap: 16px; }
    .donut-center { font-family: 'Rajdhani', sans-serif; font-size: 22px; font-weight: 800; color: white;
        position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); text-align: center; line-height: 1; }
    .donut-center small { display: block; font-size: 9px; color: var(--muted); font-weight: 400; }
    .donut-svg-wrap { position: relative; width: 100px; height: 100px; flex-shrink: 0; }
    .legend-item { display: flex; align-items: center; gap: 6px; margin-bottom: 6px; }
    .legend-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
    .legend-label { font-family: 'Share Tech Mono', monospace; font-size: 10px; color: var(--muted); flex: 1; }
    .legend-pct   { font-family: 'Rajdhani', sans-serif; font-size: 13px; font-weight: 700; color: white; }

    /* Status list */
    .status-row { display: flex; align-items: center; justify-content: space-between;
        padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .status-row:last-child { border-bottom: none; }
    .status-name { font-family: 'Share Tech Mono', monospace; font-size: 10px; color: var(--muted); display: flex; align-items: center; gap: 6px; }
    .status-ok   { font-family: 'Share Tech Mono', monospace; font-size: 10px; color: var(--green); }

    /* Mini chart */
    .mini-chart-wrap { height: 80px; position: relative; }

    /* ── BOTTOM STATS ── */
    .bottom-bar {
        display: flex; gap: 10px; margin-top: 10px;
    }
    .stat-card {
        flex: 1; background: var(--card-bg); border-radius: 12px; padding: 12px 16px;
        border: 1px solid rgba(255,255,255,0.07); display: flex; align-items: center; gap: 12px;
        backdrop-filter: blur(20px);
    }
    .stat-icon { font-size: 24px; }
    .stat-label { font-family: 'Share Tech Mono', monospace; font-size: 9px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }
    .stat-value { font-family: 'Rajdhani', sans-serif; font-size: 20px; font-weight: 700; color: white; line-height: 1.1; }
    .stat-sub   { font-size: 10px; color: var(--muted); }

    /* Radial gauge */
    .gauge-wrap { display: flex; flex-direction: column; align-items: center; }
    .gauge-label { font-family: 'Share Tech Mono', monospace; font-size: 9px; color: var(--muted); letter-spacing: 1px; margin-top: 4px; }

    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# SVG ICONS
# ─────────────────────────────────────────────────────────────
def svg_solar(size=52):
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg"
        style="filter:drop-shadow(0 0 10px #00ff88) drop-shadow(0 0 20px #00ff8844)">
      <rect x="4" y="16" width="44" height="28" rx="3" fill="#011a10" stroke="#00ff88" stroke-width="1.5"/>
      <!-- grid lines -->
      <line x1="19" y1="16" x2="19" y2="44" stroke="#00ff88" stroke-width="0.8" opacity="0.5"/>
      <line x1="33" y1="16" x2="33" y2="44" stroke="#00ff88" stroke-width="0.8" opacity="0.5"/>
      <line x1="4"  y1="26" x2="48" y2="26" stroke="#00ff88" stroke-width="0.8" opacity="0.5"/>
      <line x1="4"  y1="35" x2="48" y2="35" stroke="#00ff88" stroke-width="0.8" opacity="0.5"/>
      <!-- cells fill -->
      <rect x="5"  y="17" width="13" height="8"  rx="1" fill="rgba(0,255,136,0.08)"/>
      <rect x="20" y="17" width="12" height="8"  rx="1" fill="rgba(0,255,136,0.12)"/>
      <rect x="34" y="17" width="13" height="8"  rx="1" fill="rgba(0,255,136,0.08)"/>
      <rect x="5"  y="27" width="13" height="8"  rx="1" fill="rgba(0,255,136,0.12)"/>
      <rect x="20" y="27" width="12" height="8"  rx="1" fill="rgba(0,255,136,0.16)"/>
      <rect x="34" y="27" width="13" height="8"  rx="1" fill="rgba(0,255,136,0.10)"/>
      <rect x="5"  y="36" width="13" height="7"  rx="1" fill="rgba(0,255,136,0.08)"/>
      <rect x="20" y="36" width="12" height="7"  rx="1" fill="rgba(0,255,136,0.10)"/>
      <rect x="34" y="36" width="13" height="7"  rx="1" fill="rgba(0,255,136,0.06)"/>
      <!-- mount -->
      <line x1="19" y1="44" x2="15" y2="50" stroke="#00ff88" stroke-width="1.5"/>
      <line x1="33" y1="44" x2="37" y2="50" stroke="#00ff88" stroke-width="1.5"/>
      <!-- sun -->
      <circle cx="40" cy="9" r="5" fill="#ffd700" opacity="0.9"
        style="filter:drop-shadow(0 0 6px #ffd700)"/>
      <line x1="40" y1="2"  x2="40" y2="0"  stroke="#ffd700" stroke-width="1.2" stroke-linecap="round"/>
      <line x1="44" y1="5"  x2="46" y2="3"  stroke="#ffd700" stroke-width="1.2" stroke-linecap="round"/>
      <line x1="46" y1="9"  x2="48" y2="9"  stroke="#ffd700" stroke-width="1.2" stroke-linecap="round"/>
      <line x1="36" y1="5"  x2="34" y2="3"  stroke="#ffd700" stroke-width="1.2" stroke-linecap="round"/>
    </svg>"""

def svg_inverter(size=52):
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg"
        style="filter:drop-shadow(0 0 10px #00b4ff) drop-shadow(0 0 20px #00b4ff44)">
      <rect x="6" y="8" width="40" height="36" rx="6" fill="#001428" stroke="#00b4ff" stroke-width="1.5"/>
      <!-- bolt -->
      <polygon points="30,12 20,28 26,28 22,40 32,24 26,24" fill="#00b4ff"
        style="filter:drop-shadow(0 0 6px #00b4ff)"/>
      <!-- indicator dots -->
      <circle cx="12" cy="14" r="2" fill="#00ff88" style="animation:blink 1.5s infinite"/>
      <circle cx="18" cy="14" r="2" fill="#ffd700" opacity="0.6"/>
      <!-- wave lines -->
      <path d="M8 38 Q10 34 12 38 Q14 42 16 38 Q18 34 20 38" stroke="#00b4ff" stroke-width="1" fill="none" opacity="0.5"/>
    </svg>"""

def svg_battery(pct=82, size=52):
    fill_w = int(30 * pct / 100)
    col = "#00ff88" if pct > 50 else "#ffd700" if pct > 20 else "#ff4444"
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg"
        style="filter:drop-shadow(0 0 10px {col}) drop-shadow(0 0 20px {col}44)">
      <!-- body -->
      <rect x="5" y="13" width="38" height="26" rx="5" fill="#001428" stroke="{col}" stroke-width="1.5"/>
      <!-- terminal -->
      <rect x="43" y="20" width="5" height="12" rx="2" fill="{col}" opacity="0.6"/>
      <!-- fill -->
      <rect x="8" y="16" width="{fill_w}" height="20" rx="3" fill="{col}"
        style="filter:drop-shadow(0 0 4px {col})"/>
      <!-- segments -->
      <line x1="18" y1="16" x2="18" y2="36" stroke="rgba(0,0,0,0.3)" stroke-width="1.5"/>
      <line x1="28" y1="16" x2="28" y2="36" stroke="rgba(0,0,0,0.3)" stroke-width="1.5"/>
      <!-- pct text -->
      <text x="26" y="30" text-anchor="middle" fill="white" font-size="9" font-family="Share Tech Mono"
        font-weight="bold" style="filter:drop-shadow(0 0 3px black)">{pct}%</text>
    </svg>"""

def svg_house(size=52):
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg"
        style="filter:drop-shadow(0 0 10px #ffd700) drop-shadow(0 0 20px #ffd70044)">
      <!-- roof -->
      <polygon points="26,6 46,24 6,24" fill="#1a1000" stroke="#ffd700" stroke-width="1.5" stroke-linejoin="round"/>
      <!-- body -->
      <rect x="10" y="24" width="32" height="22" rx="2" fill="#1a1000" stroke="#ffd700" stroke-width="1.5"/>
      <!-- door -->
      <rect x="20" y="33" width="12" height="13" rx="2" fill="#ffd700" opacity="0.15" stroke="#ffd700" stroke-width="1"/>
      <circle cx="30" cy="40" r="1.2" fill="#ffd700"/>
      <!-- windows -->
      <rect x="12" y="27" width="7" height="6" rx="1" fill="#ffd700" opacity="0.25" stroke="#ffd700" stroke-width="0.8"/>
      <rect x="33" y="27" width="7" height="6" rx="1" fill="#ffd700" opacity="0.25" stroke="#ffd700" stroke-width="0.8"/>
      <!-- window cross -->
      <line x1="15.5" y1="27" x2="15.5" y2="33" stroke="#ffd700" stroke-width="0.6" opacity="0.5"/>
      <line x1="12"   y1="30" x2="19"   y2="30" stroke="#ffd700" stroke-width="0.6" opacity="0.5"/>
      <line x1="36.5" y1="27" x2="36.5" y2="33" stroke="#ffd700" stroke-width="0.6" opacity="0.5"/>
      <line x1="33"   y1="30" x2="40"   y2="30" stroke="#ffd700" stroke-width="0.6" opacity="0.5"/>
    </svg>"""

def svg_grid(size=52):
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg"
        style="filter:drop-shadow(0 0 10px #c084fc) drop-shadow(0 0 20px #c084fc44)">
      <!-- tower -->
      <line x1="26" y1="4"  x2="26" y2="48" stroke="#c084fc" stroke-width="1.5"/>
      <line x1="14" y1="16" x2="38" y2="16" stroke="#c084fc" stroke-width="1.5"/>
      <line x1="16" y1="28" x2="36" y2="28" stroke="#c084fc" stroke-width="1.5"/>
      <!-- diagonals upper -->
      <line x1="26" y1="4" x2="14" y2="16" stroke="#c084fc" stroke-width="1"/>
      <line x1="26" y1="4" x2="38" y2="16" stroke="#c084fc" stroke-width="1"/>
      <!-- diagonals lower -->
      <line x1="14" y1="16" x2="16" y2="28" stroke="#c084fc" stroke-width="1"/>
      <line x1="38" y1="16" x2="36" y2="28" stroke="#c084fc" stroke-width="1"/>
      <!-- legs -->
      <line x1="16" y1="28" x2="10" y2="48" stroke="#c084fc" stroke-width="1.5"/>
      <line x1="36" y1="28" x2="42" y2="48" stroke="#c084fc" stroke-width="1.5"/>
      <line x1="16" y1="28" x2="20" y2="48" stroke="#c084fc" stroke-width="1"/>
      <line x1="36" y1="28" x2="32" y2="48" stroke="#c084fc" stroke-width="1"/>
      <!-- wires -->
      <path d="M14 16 Q10 12 6  14" stroke="#c084fc" stroke-width="1" fill="none" opacity="0.6"/>
      <path d="M38 16 Q42 12 46 14" stroke="#c084fc" stroke-width="1" fill="none" opacity="0.6"/>
      <!-- insulators -->
      <circle cx="14" cy="16" r="2" fill="#c084fc" opacity="0.8"/>
      <circle cx="38" cy="16" r="2" fill="#c084fc" opacity="0.8"/>
    </svg>"""


# ─────────────────────────────────────────────────────────────
# SVG FLOW DIAGRAM (main center piece)
# ─────────────────────────────────────────────────────────────
def build_flow_svg(d):
    pv_active   = d["pv_power"] > 0.05
    bat_active  = d["pv_to_bat"] > 0.05
    grid_import = d["grid_power"] > 0.05
    grid_export = d["grid_power"] < -0.05

    # Animation speed based on power
    spd_pv   = max(0.4, 1.5 - d["pv_power"] * 0.2)
    spd_load = max(0.4, 1.5 - d["load_power"] * 0.2)
    spd_bat  = max(0.5, 1.5 - d["pv_to_bat"] * 0.3)
    spd_grid = 0.8

    def flow_style(color, speed, reverse=False):
        anim = f"dash-rev {speed}s linear infinite" if reverse else f"dash-fwd {speed}s linear infinite"
        return (f"stroke:{color};fill:none;stroke-width:2.5;stroke-linecap:round;"
                f"stroke-dasharray:8,6;"
                f"filter:drop-shadow(0 0 4px {color});"
                f"animation:{anim};")

    # Coordinates (SVG 700×320)
    # PV=left, INV=center, LOAD=right, BAT=bottom-center, GRID=bottom-right
    PV   = (105, 120)
    INV  = (340, 120)
    LOAD = (580, 120)
    BAT  = (340, 270)
    GRID = (580, 270)

    pv_dash   = flow_style("#00ff88", spd_pv)   if pv_active  else "stroke:#00ff8820;fill:none;stroke-width:1.5;stroke-dasharray:6,8;"
    load_dash = flow_style("#ffd700", spd_load)  if pv_active  else "stroke:#ffd70020;fill:none;stroke-width:1.5;stroke-dasharray:6,8;"
    bat_dash  = flow_style("#00b4ff", spd_bat)   if bat_active else "stroke:#00b4ff20;fill:none;stroke-width:1.5;stroke-dasharray:6,8;"
    grid_dash = flow_style("#c084fc", spd_grid, reverse=grid_export) if (grid_import or grid_export) else "stroke:#c084fc20;fill:none;stroke-width:1.5;stroke-dasharray:6,8;"

    # Curved paths
    pv_path   = f"M{PV[0]+55},{PV[1]} C{PV[0]+120},{PV[1]} {INV[0]-100},{INV[1]} {INV[0]-50},{INV[1]}"
    load_path = f"M{INV[0]+50},{INV[1]} C{INV[0]+100},{INV[1]} {LOAD[0]-100},{LOAD[1]} {LOAD[0]-55},{LOAD[1]}"
    bat_path  = f"M{INV[0]},{INV[1]+50} C{INV[0]},{INV[1]+110} {BAT[0]},{BAT[1]-90} {BAT[0]},{BAT[1]-50}"
    grid_path = f"M{GRID[0]},{GRID[1]-50} C{GRID[0]},{GRID[1]-100} {LOAD[0]},{LOAD[1]+80} {LOAD[0]},{LOAD[1]+50}"

    # Flow power labels mid-path
    label_pv   = ((PV[0]+55 + INV[0]-50)//2, PV[1]-14)
    label_load = ((INV[0]+50 + LOAD[0]-55)//2, INV[1]-14)
    label_bat  = (INV[0]+18, (INV[1]+50 + BAT[1]-50)//2)
    label_grid = (GRID[0]+18, (GRID[1]-50 + LOAD[1]+50)//2)

    return f"""
    <style>
    @keyframes dash-fwd {{ to {{ stroke-dashoffset: -28; }} }}
    @keyframes dash-rev {{ to {{ stroke-dashoffset:  28; }} }}
    </style>
    <svg viewBox="0 0 700 360" xmlns="http://www.w3.org/2000/svg"
         style="width:100%;height:100%;overflow:visible">

      <!-- ── BACKGROUND GLOW NODES ── -->
      <circle cx="{PV[0]}"   cy="{PV[1]}"   r="68" fill="rgba(0,255,136,0.04)"  stroke="rgba(0,255,136,0.12)"  stroke-width="1"/>
      <circle cx="{INV[0]}"  cy="{INV[1]}"  r="68" fill="rgba(0,180,255,0.04)"  stroke="rgba(0,180,255,0.12)"  stroke-width="1"/>
      <circle cx="{LOAD[0]}" cy="{LOAD[1]}" r="68" fill="rgba(255,215,0,0.04)"  stroke="rgba(255,215,0,0.12)"  stroke-width="1"/>
      <circle cx="{BAT[0]}"  cy="{BAT[1]}"  r="68" fill="rgba(0,180,255,0.04)"  stroke="rgba(0,180,255,0.12)"  stroke-width="1"/>
      <circle cx="{GRID[0]}" cy="{GRID[1]}" r="68" fill="rgba(192,132,252,0.04)" stroke="rgba(192,132,252,0.12)" stroke-width="1"/>

      <!-- ── FLOW LINES ── -->
      <path d="{pv_path}"   style="{pv_dash}"/>
      <path d="{load_path}" style="{load_dash}"/>
      <path d="{bat_path}"  style="{bat_dash}"/>
      <path d="{grid_path}" style="{grid_dash}"/>

      <!-- ── POWER LABELS ── -->
      {"" if not pv_active else f'<rect x="{label_pv[0]-22}" y="{label_pv[1]-10}" width="50" height="18" rx="9" fill="rgba(10,22,40,0.92)" stroke="rgba(0,255,136,0.4)" stroke-width="1"/><text x="{label_pv[0]+3}" y="{label_pv[1]+3}" text-anchor="middle" fill="#00ff88" font-size="9" font-family="Share Tech Mono">{d["pv_power"]}kW</text>'}
      {"" if not pv_active else f'<rect x="{label_load[0]-22}" y="{label_load[1]-10}" width="54" height="18" rx="9" fill="rgba(10,22,40,0.92)" stroke="rgba(255,215,0,0.4)" stroke-width="1"/><text x="{label_load[0]+5}" y="{label_load[1]+3}" text-anchor="middle" fill="#ffd700" font-size="9" font-family="Share Tech Mono">{d["load_power"]}kW</text>'}
      {"" if not bat_active else f'<rect x="{label_bat[0]}" y="{label_bat[1]-9}" width="54" height="18" rx="9" fill="rgba(10,22,40,0.92)" stroke="rgba(0,180,255,0.4)" stroke-width="1"/><text x="{label_bat[0]+27}" y="{label_bat[1]+4}" text-anchor="middle" fill="#00b4ff" font-size="9" font-family="Share Tech Mono">{d["pv_to_bat"]}kW</text>'}
      {"" if not (grid_import or grid_export) else f'<rect x="{label_grid[0]}" y="{label_grid[1]-9}" width="58" height="18" rx="9" fill="rgba(10,22,40,0.92)" stroke="rgba(192,132,252,0.4)" stroke-width="1"/><text x="{label_grid[0]+29}" y="{label_grid[1]+4}" text-anchor="middle" fill="#c084fc" font-size="9" font-family="Share Tech Mono">{abs(d["grid_power"])}kW</text>'}

    </svg>
    """


# ─────────────────────────────────────────────────────────────
# DONUT CHART (SVG)
# ─────────────────────────────────────────────────────────────
def donut_svg(pv_pct, conso_pct, bat_pct, grid_pct, total_kw):
    r = 44; cx = cy = 50; circ = 2 * 3.14159 * r
    def arc(pct, offset, color):
        dash = circ * pct / 100
        gap  = circ - dash
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="10" stroke-dasharray="{dash:.1f} {gap:.1f}" stroke-dashoffset="{-offset:.1f}" style="filter:drop-shadow(0 0 4px {color})" transform="rotate(-90 50 50)"/>'

    o1 = 0
    o2 = circ * pv_pct / 100
    o3 = o2 + circ * conso_pct / 100
    o4 = o3 + circ * bat_pct / 100

    return f"""
    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" width="100" height="100">
      <circle cx="50" cy="50" r="44" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="10"/>
      {arc(pv_pct,    o1, "#00ff88")}
      {arc(conso_pct, o2, "#ffd700")}
      {arc(bat_pct,   o3, "#00b4ff")}
      {arc(grid_pct,  o4, "#c084fc")}
      <text x="50" y="47" text-anchor="middle" fill="white" font-size="14" font-family="Rajdhani" font-weight="800">{total_kw}</text>
      <text x="50" y="58" text-anchor="middle" fill="#64748b" font-size="7" font-family="Share Tech Mono">kW</text>
    </svg>"""


# ─────────────────────────────────────────────────────────────
# MINI SPARKLINE (SVG)
# ─────────────────────────────────────────────────────────────
def mini_sparkline(history_pv, history_load):
    if len(history_pv) < 2:
        return "<svg width='100%' height='60'></svg>"
    w, h = 280, 60
    max_v = max(max(history_pv), max(history_load), 0.1)
    n = len(history_pv)
    def pts(vals, color):
        coords = " ".join(
            f"{int(i*(w-10)/(n-1))+5},{int(h - 4 - vals[i]/max_v*(h-8))}"
            for i in range(n)
        )
        return f'<polyline points="{coords}" stroke="{color}" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 0 3px {color})"/>'
    return f"""<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:60px">
      <rect width="{w}" height="{h}" fill="rgba(0,0,0,0.2)" rx="6"/>
      {pts(history_pv, '#00ff88')}
      {pts(history_load, '#ffd700')}
    </svg>"""


# ─────────────────────────────────────────────────────────────
# RADIAL GAUGE (SVG)
# ─────────────────────────────────────────────────────────────
def radial_gauge(pct, color="#00ff88", size=80):
    r = 30; circ = 2 * 3.14159 * r
    dash = circ * pct / 100
    gap  = circ - dash
    return f"""<svg viewBox="0 0 80 80" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
      <circle cx="40" cy="40" r="30" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="8"/>
      <circle cx="40" cy="40" r="30" fill="none" stroke="{color}" stroke-width="8"
        stroke-dasharray="{dash:.1f} {gap:.1f}" stroke-dashoffset="{circ*0.25:.1f}"
        stroke-linecap="round" transform="rotate(-90 40 40)"
        style="filter:drop-shadow(0 0 5px {color})"/>
      <text x="40" y="44" text-anchor="middle" fill="white" font-size="13" font-family="Rajdhani" font-weight="800">{pct}%</text>
    </svg>"""


# ─────────────────────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────────────────────
inject_css()

# History for sparkline
if "history_pv"   not in st.session_state: st.session_state.history_pv   = []
if "history_load" not in st.session_state: st.session_state.history_load = []

d = get_energy_data()
st.session_state.history_pv.append(d["pv_power"])
st.session_state.history_load.append(d["load_power"])
if len(st.session_state.history_pv) > 30:
    st.session_state.history_pv   = st.session_state.history_pv[-30:]
    st.session_state.history_load = st.session_state.history_load[-30:]

now = time.strftime("%H:%M:%S")
date_str = time.strftime("%d %b %Y")

# ── HEADER BAR ──
grid_color = "kv-purple" if d["grid_power"] > 0 else "kv-green"
grid_label = f"{d['grid_power']:+.2f}"

st.markdown(f"""
<div class="header-bar">
  <div class="header-brand">
    <div class="brand-icon">⚡</div>
    <div>
      <div class="brand-title">DIGITAL TWIN — <span>SMART ENERGY</span></div>
      <div class="brand-sub">Surveillance &amp; Optimisation en temps réel</div>
    </div>
  </div>

  <div class="kpi-group">
    <div class="kpi-pill">
      <div class="kpi-label">⬆ Production PV</div>
      <div class="kpi-value kv-green">{d['pv_power']}<span style="font-size:12px"> kW</span></div>
      <div class="kpi-sub">{d['pv_daily']} kWh/jour</div>
    </div>
    <div class="kpi-pill">
      <div class="kpi-label">🔋 Batterie</div>
      <div class="kpi-value kv-blue">{d['battery_pct']}<span style="font-size:12px">%</span></div>
      <div class="kpi-sub">{d['battery_kwh']} kWh</div>
    </div>
    <div class="kpi-pill">
      <div class="kpi-label">🏠 Consommation</div>
      <div class="kpi-value kv-yellow">{d['load_power']}<span style="font-size:12px"> kW</span></div>
      <div class="kpi-sub">{d['load_daily']} kWh/jour</div>
    </div>
    <div class="kpi-pill">
      <div class="kpi-label">⚡ Réseau</div>
      <div class="kpi-value {grid_color}">{grid_label}<span style="font-size:12px"> kW</span></div>
      <div class="kpi-sub">{"Importation" if d['grid_power']>0 else "Exportation"}</div>
    </div>
  </div>

  <div style="text-align:right">
    <div style="font-family:'Share Tech Mono',monospace;font-size:18px;color:white;font-weight:bold">{now}</div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:10px;color:#64748b">{date_str}</div>
    <div class="live-badge" style="margin-top:6px"><div class="live-dot"></div>LIVE</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── MAIN LAYOUT ──
col_main, col_right = st.columns([3, 1], gap="small")

with col_main:
    # ── FLOW SVG ──
    st.markdown(build_flow_svg(d), unsafe_allow_html=True)

    # ── COMPONENT CARDS ──
    c1, c2, c3, c4, c5 = st.columns(5, gap="small")

    with c1:
        st.markdown(f"""
        <div class="energy-card card-pv">
          <div class="card-icon">{svg_solar(46)}</div>
          <div class="card-name">Panneaux PV</div>
          <div class="card-power" style="color:#00ff88;text-shadow:0 0 12px #00ff8877">
            {d['pv_power']}<span class="card-unit">kW</span>
          </div>
          <div class="card-meta">{d['pv_daily']} kWh/jour</div>
          <div class="card-status status-online"><div class="status-dot"></div>EN LIGNE</div>
          <div style="margin-top:8px;padding:5px 6px;background:rgba(0,255,136,0.06);border-radius:6px">
            <div style="display:flex;justify-content:space-between;font-family:'Share Tech Mono',monospace;font-size:9px;color:#64748b;margin-bottom:3px">
              <span>Puissance</span><span style="color:#00ff88">{d['pv_power']} kW</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-family:'Share Tech Mono',monospace;font-size:9px;color:#64748b">
              <span>Irradiation</span><span style="color:#ffd700">800 W/m²</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="energy-card card-inv">
          <div class="card-icon">{svg_inverter(46)}</div>
          <div class="card-name">Onduleur</div>
          <div class="card-power" style="color:#00b4ff;text-shadow:0 0 12px #00b4ff77">
            {d['inverter_eff']}<span class="card-unit">%</span>
          </div>
          <div class="card-meta">{d['inverter_out']} kW out</div>
          <div class="card-status status-charge"><div class="status-dot"></div>EN LIGNE</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="energy-card card-bat">
          <div class="card-icon">{svg_battery(d['battery_pct'], 46)}</div>
          <div class="card-name">Batterie</div>
          <div class="card-power" style="color:#00b4ff;text-shadow:0 0 12px #00b4ff77">
            {d['battery_pct']}<span class="card-unit">%</span>
          </div>
          <div class="card-meta">{d['battery_kwh']} kWh / 48V</div>
          <div class="bat-bar-wrap"><div class="bat-bar" style="width:{d['battery_pct']}%"></div></div>
          <div class="card-status status-charge" style="margin-top:6px"><div class="status-dot"></div>CHARGE</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="energy-card card-load">
          <div class="card-icon">{svg_house(46)}</div>
          <div class="card-name">Charge (Maison)</div>
          <div class="card-power" style="color:#ffd700;text-shadow:0 0 12px #ffd70077">
            {d['load_power']}<span class="card-unit">kW</span>
          </div>
          <div class="card-meta">{d['load_daily']} kWh/jour</div>
          <div class="card-status status-active"><div class="status-dot"></div>ACTIF</div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        gval = f"{d['grid_power']:+.2f}"
        glab = "Importation" if d['grid_power'] > 0 else "Exportation"
        gcol = "#c084fc"
        st.markdown(f"""
        <div class="energy-card card-grid">
          <div class="card-icon">{svg_grid(46)}</div>
          <div class="card-name">Réseau</div>
          <div class="card-power" style="color:{gcol};text-shadow:0 0 12px {gcol}77">
            {gval}<span class="card-unit">kW</span>
          </div>
          <div class="card-meta">{glab}</div>
          <div class="card-status status-connected"><div class="status-dot"></div>CONNECTÉ</div>
        </div>
        """, unsafe_allow_html=True)

    # ── BOTTOM STATS ──
    st.markdown(f"""
    <div class="bottom-bar">
      <div class="stat-card">
        <div class="stat-icon">🌱</div>
        <div>
          <div class="stat-label">Émission CO₂ évitée</div>
          <div class="stat-value">{d['co2_saved']} <span style="font-size:12px;color:#64748b">kg</span></div>
          <div class="stat-sub">Aujourd'hui</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🌲</div>
        <div>
          <div class="stat-label">Équivalent arbres plantés</div>
          <div class="stat-value">{d['trees']}</div>
          <div class="stat-sub">Aujourd'hui</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">💰</div>
        <div>
          <div class="stat-label">Économie réalisée</div>
          <div class="stat-value">{d['savings']} <span style="font-size:12px;color:#64748b">€</span></div>
          <div class="stat-sub">Aujourd'hui</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="font-size:14px">📡</div>
        <div>
          <div class="stat-label">Mode Autonome</div>
          <div class="stat-value" style="color:#00ff88">Activé</div>
          <div class="stat-sub">Système actif</div>
        </div>
      </div>
      <div class="stat-card" style="align-items:center;justify-content:center;flex-direction:column;gap:4px">
        {radial_gauge(int(d['autoconsumption']), '#00ff88', 70)}
        <div style="font-family:'Share Tech Mono',monospace;font-size:9px;color:#64748b;letter-spacing:1px">AUTO-CONSO</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    # ── ENERGY DISTRIBUTION ──
    total_kw = round(d['pv_power'] + d['load_power'] + abs(d['grid_power']), 2)
    pv_s   = round(d['pv_power']   / max(total_kw,0.01) * 100, 1)
    co_s   = round(d['load_power'] / max(total_kw,0.01) * 100, 1)
    ba_s   = round(d['pv_to_bat']  / max(total_kw,0.01) * 100, 1)
    gr_s   = round(abs(d['grid_power']) / max(total_kw,0.01) * 100, 1)

    st.markdown(f"""
    <div class="panel-card">
      <div class="panel-title">Répartition Énergétique</div>
      <div class="donut-wrap">
        <div class="donut-svg-wrap">
          {donut_svg(pv_s, co_s, ba_s, gr_s, total_kw)}
        </div>
        <div style="flex:1">
          <div class="legend-item">
            <div class="legend-dot" style="background:#00ff88;box-shadow:0 0 6px #00ff88"></div>
            <div class="legend-label">Production PV</div>
            <div class="legend-pct">{pv_s}%</div>
          </div>
          <div class="legend-item">
            <div class="legend-dot" style="background:#ffd700;box-shadow:0 0 6px #ffd700"></div>
            <div class="legend-label">Consommation</div>
            <div class="legend-pct">{co_s}%</div>
          </div>
          <div class="legend-item">
            <div class="legend-dot" style="background:#00b4ff;box-shadow:0 0 6px #00b4ff"></div>
            <div class="legend-label">Batterie</div>
            <div class="legend-pct">{ba_s}%</div>
          </div>
          <div class="legend-item">
            <div class="legend-dot" style="background:#c084fc;box-shadow:0 0 6px #c084fc"></div>
            <div class="legend-label">Réseau</div>
            <div class="legend-pct">{gr_s}%</div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── MINI SPARKLINE ──
    spark = mini_sparkline(st.session_state.history_pv, st.session_state.history_load)
    st.markdown(f"""
    <div class="panel-card">
      <div class="panel-title">Analyse en Direct</div>
      <div style="display:flex;gap:12px;margin-bottom:6px">
        <div style="display:flex;align-items:center;gap:4px">
          <div style="width:10px;height:2px;background:#00ff88;border-radius:2px"></div>
          <span style="font-family:'Share Tech Mono',monospace;font-size:9px;color:#64748b">PV</span>
        </div>
        <div style="display:flex;align-items:center;gap:4px">
          <div style="width:10px;height:2px;background:#ffd700;border-radius:2px"></div>
          <span style="font-family:'Share Tech Mono',monospace;font-size:9px;color:#64748b">Conso</span>
        </div>
      </div>
      {spark}
    </div>
    """, unsafe_allow_html=True)

    # ── SYSTEM STATUS ──
    st.markdown(f"""
    <div class="panel-card">
      <div class="panel-title">Statut Système</div>
      <div style="display:flex;align-items:center;gap:8px;padding:8px;background:rgba(0,255,136,0.06);border-radius:8px;margin-bottom:10px;border:1px solid rgba(0,255,136,0.15)">
        <span style="font-size:18px">🛡️</span>
        <div>
          <div style="font-family:'Rajdhani',sans-serif;font-size:13px;color:#00ff88;font-weight:600">Système sain</div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:9px;color:#64748b">Aucune alarme détectée</div>
        </div>
      </div>
      <div class="status-row">
        <div class="status-name">⚡ Onduleur</div>
        <div class="status-ok">En ligne</div>
      </div>
      <div class="status-row">
        <div class="status-name">🔋 Batterie</div>
        <div class="status-ok">En ligne</div>
      </div>
      <div class="status-row">
        <div class="status-name">☀️ Panneaux PV</div>
        <div class="status-ok">En ligne</div>
      </div>
      <div class="status-row">
        <div class="status-name">⚡ Réseau</div>
        <div class="status-ok">Connecté</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── WEATHER ──
    st.markdown(f"""
    <div class="panel-card">
      <div class="panel-title">Météo Locale</div>
      <div style="display:flex;align-items:center;gap:14px">
        <span style="font-size:32px">☀️</span>
        <div>
          <div style="font-family:'Rajdhani',sans-serif;font-size:26px;font-weight:800;color:white">27°C</div>
          <div style="font-family:'Share Tech Mono',monospace;font-size:9px;color:#64748b">Ensoleillé</div>
        </div>
      </div>
      <div style="display:flex;gap:12px;margin-top:10px">
        <div style="font-family:'Share Tech Mono',monospace;font-size:9px;color:#64748b">
          ☀ Irradiation<br><span style="color:#ffd700">800 W/m²</span>
        </div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:9px;color:#64748b">
          💨 Vent<br><span style="color:#00b4ff">12 km/h</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# AUTO-REFRESH (every 3 seconds)
# ─────────────────────────────────────────────────────────────
st.markdown("""
<script>
setTimeout(function(){ window.location.reload(); }, 3000);
</script>
""", unsafe_allow_html=True)

time.sleep(0.05)
st.rerun()
