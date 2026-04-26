import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Digital Twin – Smart Energy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Exo+2:wght@300;400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"]>.main {
  background:#080e1a !important; color:#e0e8f8 !important;
  font-family:'Exo 2',sans-serif !important;
}
[data-testid="stHeader"]{ background:transparent !important; }
section[data-testid="stSidebar"]{
  background:#0b1220 !important; border-right:1px solid #162035 !important;
}
#MainMenu,footer,[data-testid="stToolbar"]{ visibility:hidden; }
.block-container{ padding:0.6rem 1rem 0.5rem !important; }

.nav-logo{ display:flex;align-items:center;gap:10px;padding:14px 4px 20px; }
.nav-logo-icon{ width:38px;height:38px;border-radius:9px;background:linear-gradient(135deg,#0050cc,#00c8a0);display:flex;align-items:center;justify-content:center;font-size:20px; }
.nav-logo-text{ font-family:'Rajdhani',sans-serif;font-weight:700;font-size:15px;color:#e0e8f8;line-height:1.2; }
.nav-logo-sub{ font-size:10px;color:#5070a0;letter-spacing:1px; }
.nav-item{ display:flex;align-items:center;gap:10px;padding:9px 12px;margin:2px 0;border-radius:8px;font-size:13.5px;color:#7090b8;cursor:pointer;border-left:3px solid transparent; }
.nav-item.active{ background:linear-gradient(90deg,#182f55,#0e1f38);color:#3de8c0;border-left:3px solid #3de8c0;font-weight:600; }
.nav-sep{ border:none;border-top:1px solid #162035;margin:10px 0; }

.topbar{ background:linear-gradient(90deg,#0c1828,#0e1f35);border:1px solid #162035;border-radius:10px;padding:8px 18px;display:flex;align-items:center;gap:20px;margin-bottom:10px; }
.tb-logo{ font-family:'Rajdhani',sans-serif;font-weight:700;font-size:17px;color:#e0e8f8; }
.tb-sub{ font-size:10px;color:#5070a0; }
.tb-sep{ width:1px;height:30px;background:#162035;flex-shrink:0; }
.tb-item{ font-size:10px;color:#5070a0;line-height:1.8; }
.tb-val-green{ color:#3de8c0;font-weight:700;font-size:12px; }
.tb-val-red{ color:#f0406a;font-weight:700;font-size:12px; }
.tb-dot-g{ display:inline-block;width:7px;height:7px;border-radius:50%;background:#3de8c0;box-shadow:0 0 5px #3de8c0;margin-right:4px; }
.tb-dot-r{ display:inline-block;width:7px;height:7px;border-radius:50%;background:#f0406a;box-shadow:0 0 5px #f0406a;margin-right:4px; }
.tb-right{ margin-left:auto;display:flex;align-items:center;gap:16px;font-size:12px;color:#7090b8; }

.kpi{ background:linear-gradient(135deg,#0d1b30,#0a1524);border:1px solid #162035;border-radius:11px;padding:12px 14px;position:relative;overflow:hidden; }
.kpi::before{ content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--ac,#3de8c0); }
.kpi-lbl{ font-size:10px;color:#5070a0;text-transform:uppercase;letter-spacing:1.2px;margin-bottom:4px; }
.kpi-val{ font-family:'Rajdhani',sans-serif;font-size:2.1rem;font-weight:700;line-height:1; }
.kpi-s{ font-size:10.5px;color:#7090b8;margin-top:3px; }
.badge-g{ color:#3de8c0;font-size:10.5px;font-weight:600; }
.badge-r{ color:#f0406a;font-size:10.5px;font-weight:600; }

.scard{ background:linear-gradient(135deg,#0d1b30,#0a1524);border:1px solid #162035;border-radius:11px;padding:14px;margin-bottom:10px; }
.stitle{ font-family:'Rajdhani',sans-serif;font-size:12px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:#5070a0;margin-bottom:10px; }

.fnode{ border-radius:11px;padding:14px 12px;text-align:center;border:1px solid var(--bc,#1a3055);background:var(--bg,#0a1830); }
.fnode-lbl{ font-size:10px;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px; }
.fnode-val{ font-family:'Rajdhani',sans-serif;font-size:1.9rem;font-weight:700; }

.brow{ display:flex;justify-content:space-between;align-items:center;padding:7px 0;border-bottom:1px solid #101e30;font-size:13px; }
.brow:last-child{ border-bottom:none; }
.bval{ font-family:'Rajdhani',sans-serif;font-size:1rem;font-weight:600; }

.drow{ display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid #101e30;font-size:12.5px; }
.drow:last-child{ border-bottom:none; }
.donline{ color:#3de8c0;font-size:11px; }
.dval{ font-family:'Rajdhani',sans-serif;font-size:12px; }

.fbar{ background:linear-gradient(90deg,#0c1828,#0e1f35);border:1px solid #162035;border-radius:11px;display:flex;align-items:center;justify-content:space-between;padding:12px 24px;margin-top:10px; }
.fbar-item{ text-align:center; }
.fbar-lbl{ font-size:10px;color:#5070a0;text-transform:uppercase;letter-spacing:1px;margin-bottom:2px; }
.fbar-val{ font-family:'Rajdhani',sans-serif;font-size:1.6rem;font-weight:700; }
.fbar-sub{ font-size:10px;color:#5070a0; }
.sys-ok{ display:flex;align-items:center;gap:10px; }
.sys-icon{ width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#006633,#003318);border:1px solid #00aa55;display:flex;align-items:center;justify-content:center;font-size:16px; }
.sys-lbl{ font-family:'Rajdhani',sans-serif;font-size:13px;font-weight:700;color:#3de8c0; }
.sys-sub{ font-size:10px;color:#5070a0; }

/* donut svg */
.donut-wrap{ position:relative;width:120px;height:120px;margin:0 auto; }
</style>
""", unsafe_allow_html=True)

# ── DATA ────────────────────────────────────────────────────────────────────────
np.random.seed(42)
hours = pd.date_range("2024-05-19 00:00", periods=24, freq="h")
prod  = np.clip(np.sin(np.linspace(0, np.pi, 24)) * 2.8 + np.random.normal(0, .08, 24), 0, None)
cons  = np.clip(0.9 + np.random.normal(0, .12, 24), 0.4, 2.0)
stor  = np.sin(np.linspace(0, 2*np.pi, 24)) * .45
net   = cons - prod

def make_sparkline(y, color):
    df = pd.DataFrame({"x": list(range(len(y))), "y": y})
    return (alt.Chart(df).mark_area(
        line={"color": color, "strokeWidth": 2},
        color=alt.Gradient("linear",
            stops=[alt.GradientStop(color=color+"55", offset=0),
                   alt.GradientStop(color=color+"00", offset=1)],
            x1=1, x2=1, y1=1, y2=0),
    ).encode(
        x=alt.X("x:Q", axis=None),
        y=alt.Y("y:Q", axis=None),
    ).properties(height=50, background="transparent")
    .configure_view(strokeWidth=0))

def make_perf_chart(hours, prod, cons, stor, net):
    df = pd.DataFrame({
        "Heure": list(hours)*4,
        "kW": list(prod)+list(cons)+list(stor)+list(net),
        "Série": (["Production PV"]*24 + ["Consommation"]*24 +
                  ["Stockage"]*24 + ["Réseau"]*24),
    })
    color_scale = alt.Scale(domain=["Production PV","Consommation","Stockage","Réseau"],
                            range=["#3de8c0","#ffd060","#60b4ff","#b060ff"])
    return (alt.Chart(df).mark_line(strokeWidth=2).encode(
        x=alt.X("Heure:T", axis=alt.Axis(format="%H:%M", labelColor="#5070a0",
                                          tickColor="#5070a0", domainColor="#162035",
                                          gridColor="#0e1e30", labelFontSize=9)),
        y=alt.Y("kW:Q", axis=alt.Axis(labelColor="#5070a0", tickColor="#5070a0",
                                       domainColor="#162035", gridColor="#0e1e30",
                                       labelFontSize=9, title="kW",
                                       titleColor="#5070a0", titleFontSize=9)),
        color=alt.Color("Série:N", scale=color_scale,
                        legend=alt.Legend(orient="bottom", labelColor="#7090b8",
                                          titleColor="#5070a0", labelFontSize=9,
                                          symbolStrokeWidth=2, rowPadding=2)),
    ).properties(height=185, background="transparent")
    .configure_view(strokeWidth=0)
    .configure_axis(gridOpacity=0.4))

def make_bar_chart(hours, prod, cons):
    df = pd.DataFrame({
        "Heure": list(range(24))*2,
        "kWh": list(prod)+list(cons),
        "Série": ["Production"]*24 + ["Consommation"]*24,
    })
    color_scale = alt.Scale(domain=["Production","Consommation"],
                            range=["#3de8c0","#ffd060"])
    return (alt.Chart(df).mark_bar(opacity=0.9).encode(
        x=alt.X("Heure:O", axis=alt.Axis(labelColor="#5070a0", tickColor="#5070a0",
                                          domainColor="#162035", gridColor="#0e1e30",
                                          labelFontSize=8, values=[0,6,12,18,23])),
        y=alt.Y("kWh:Q", axis=alt.Axis(labelColor="#5070a0", gridColor="#0e1e30",
                                        labelFontSize=8, title="kWh",
                                        titleColor="#5070a0", titleFontSize=8)),
        color=alt.Color("Série:N", scale=color_scale,
                        legend=alt.Legend(orient="top", labelColor="#7090b8",
                                          labelFontSize=9, symbolStrokeWidth=2)),
        xOffset="Série:N",
    ).properties(height=140, background="transparent")
    .configure_view(strokeWidth=0))

def donut_svg(pct, color="#3de8c0", size=110):
    r = 40; cx = cy = size//2
    circ = 2 * 3.14159 * r
    dash = circ * pct / 100
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#0e1e30" stroke-width="14"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="14"
        stroke-dasharray="{dash:.1f} {circ:.1f}"
        stroke-linecap="round"
        transform="rotate(-90 {cx} {cy})"/>
      <text x="{cx}" y="{cy+2}" text-anchor="middle" dominant-baseline="middle"
        fill="{color}" font-family="Rajdhani,sans-serif" font-size="18" font-weight="700">{pct}%</text>
    </svg>"""

def pie_svg(values, colors, labels, size=160):
    total = sum(values)
    cx = cy = size // 2
    r = 55; inner_r = 33
    svg = f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
    svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#0e1e30"/>'
    angle = -90
    for i, (v, c) in enumerate(zip(values, colors)):
        sweep = v / total * 360
        a1 = angle * 3.14159 / 180
        a2 = (angle + sweep) * 3.14159 / 180
        x1 = cx + r * np.cos(a1); y1 = cy + r * np.sin(a1)
        x2 = cx + r * np.cos(a2); y2 = cy + r * np.sin(a2)
        large = 1 if sweep > 180 else 0
        xi1 = cx + inner_r * np.cos(a1); yi1 = cy + inner_r * np.sin(a1)
        xi2 = cx + inner_r * np.cos(a2); yi2 = cy + inner_r * np.sin(a2)
        svg += f'<path d="M {xi1:.1f} {yi1:.1f} L {x1:.1f} {y1:.1f} A {r} {r} 0 {large} 1 {x2:.1f} {y2:.1f} L {xi2:.1f} {yi2:.1f} A {inner_r} {inner_r} 0 {large} 0 {xi1:.1f} {yi1:.1f} Z" fill="{c}" stroke="#080e1a" stroke-width="2"/>'
        angle += sweep
    svg += f'<text x="{cx}" y="{cy-4}" text-anchor="middle" fill="#e0e8f8" font-family="Rajdhani,sans-serif" font-size="15" font-weight="700">18.7</text>'
    svg += f'<text x="{cx}" y="{cy+12}" text-anchor="middle" fill="#7090b8" font-family="Exo 2,sans-serif" font-size="9">kWh</text>'
    svg += '</svg>'
    return svg

# ── SIDEBAR ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="nav-logo">
      <div class="nav-logo-icon">⚡</div>
      <div><div class="nav-logo-text">DIGITAL TWIN</div><div class="nav-logo-sub">SMART ENERGY</div></div>
    </div>""", unsafe_allow_html=True)
    for icon, label, active in [
        ("⊞","Aperçu",True),("⚡","Flux d'énergie",False),("📱","Appareils",False),
        ("🔋","Stockage",False),("📈","Historique",False),
        ("🔬","Analyses",False),("🔔","Alarmes",False),("🎭","Scénarios",False),
    ]:
        cls = "nav-item active" if active else "nav-item"
        st.markdown(f'<div class="{cls}">{icon}&nbsp;&nbsp;{label}</div>', unsafe_allow_html=True)
    st.markdown("<hr class='nav-sep'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:10px;color:#5070a0;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px">Météo Actuelle</div>
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
      <div style="font-size:32px">🌤</div>
      <div><div style="font-family:'Rajdhani',sans-serif;font-size:2.2rem;font-weight:700;color:#ffd060">27°C</div>
      <div style="font-size:12px;color:#8aa0c0">Ensoleillé</div></div>
    </div>
    <div style="font-size:11.5px;color:#6080a0;padding:3px 0">☀️ Irradiation solaire &nbsp;<span style="color:#c0d4f0">800 W/m²</span></div>
    <div style="font-size:11.5px;color:#6080a0;padding:3px 0">💧 Humidité &nbsp;<span style="color:#c0d4f0">45 %</span></div>
    <div style="font-size:11.5px;color:#6080a0;padding:3px 0">💨 Vent &nbsp;<span style="color:#c0d4f0">12 km/h</span></div>
    <div style="display:flex;margin-top:10px">
      <div style="flex:1;text-align:center;font-size:10px"><div style="color:#5070a0">MAR</div><div>🌤</div><div style="color:#c0d4f0">28/16°</div></div>
      <div style="flex:1;text-align:center;font-size:10px"><div style="color:#5070a0">MER</div><div>☀️</div><div style="color:#c0d4f0">27/15°</div></div>
      <div style="flex:1;text-align:center;font-size:10px"><div style="color:#5070a0">JEU</div><div>🌤</div><div style="color:#c0d4f0">26/14°</div></div>
    </div>""", unsafe_allow_html=True)

# ── TOP BAR ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div><div class="tb-logo">⚡ DIGITAL TWIN – SMART ENERGY</div><div class="tb-sub">Surveillance &amp; Optimisation en temps réel</div></div>
  <div class="tb-sep"></div>
  <div class="tb-item">Mode de fonctionnement<br><span class="tb-dot-g"></span><span class="tb-val-green">AUTONOME</span></div>
  <div class="tb-sep"></div>
  <div class="tb-item">Statut système<br><span class="tb-dot-g"></span><span class="tb-val-green">NORMAL</span></div>
  <div class="tb-sep"></div>
  <div class="tb-item">Dernière mise à jour<br><span class="tb-dot-r"></span><span class="tb-val-red">10:24:35 &nbsp;LIVE</span></div>
  <div class="tb-right">📅 19 Mai 2024 &nbsp;&nbsp; 🕐 10:24 &nbsp;&nbsp; 🔔 &nbsp; ⚙</div>
</div>""", unsafe_allow_html=True)

# ── KPI ROW ──────────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns([1,1,1,1,0.85])

with c1:
    st.markdown("""<div class="kpi" style="--ac:#3de8c0">
      <div class="kpi-lbl">☀️ Production PV</div>
      <div class="kpi-val" style="color:#3de8c0">2.45 <span style="font-size:1rem">kW</span></div>
      <div class="kpi-s">Aujourd'hui : 18.7 kWh</div>
      <div class="badge-g">▲ +12% vs hier</div>
    </div>""", unsafe_allow_html=True)
    st.altair_chart(make_sparkline(prod, "#3de8c0"), use_container_width=True)

with c2:
    st.markdown("""<div class="kpi" style="--ac:#60b4ff">
      <div class="kpi-lbl">🔋 Batterie</div>
      <div class="kpi-val" style="color:#60b4ff">80 <span style="font-size:1rem">%</span></div>
      <div class="kpi-s">48.0 V &nbsp;|&nbsp; 40.0 A</div>
      <div class="kpi-s">Énergie stockée : 4.4 kWh</div>
      <div style="background:#0e1e30;border-radius:4px;height:6px;margin-top:6px">
        <div style="background:#60b4ff;width:80%;height:6px;border-radius:4px"></div>
      </div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown("""<div class="kpi" style="--ac:#ffd060">
      <div class="kpi-lbl">🏠 Consommation</div>
      <div class="kpi-val" style="color:#ffd060">1.60 <span style="font-size:1rem">kW</span></div>
      <div class="kpi-s">Aujourd'hui : 14.3 kWh</div>
      <div class="badge-g">▲ +8% vs hier</div>
    </div>""", unsafe_allow_html=True)
    st.altair_chart(make_sparkline(cons, "#ffd060"), use_container_width=True)

with c4:
    st.markdown("""<div class="kpi" style="--ac:#b060ff">
      <div class="kpi-lbl">🔌 Réseau</div>
      <div class="kpi-val" style="color:#b060ff">-0.85 <span style="font-size:1rem">kW</span></div>
      <div class="kpi-s">Importation</div>
      <div class="badge-r">▲ +0.2 kW vs hier</div>
    </div>""", unsafe_allow_html=True)
    st.altair_chart(make_sparkline(net, "#b060ff"), use_container_width=True)

with c5:
    st.markdown("""<div class="kpi" style="--ac:#3de8c0;padding-bottom:6px">
      <div class="kpi-lbl">Autonomie</div>
      <div style="font-size:10px;color:#5070a0">Auto-consommation (PV → Charge)</div>
    </div>""", unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center;margin-top:4px">{donut_svg(72)}</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;font-size:10.5px;color:#3de8c0;margin-top:2px">✅ Objectif : 70%</div>', unsafe_allow_html=True)

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ── MIDDLE ROW ───────────────────────────────────────────────────────────────────
left, right = st.columns([2.25, 1])

with left:
    st.markdown("""
    <div class="scard">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
        <div class="stitle" style="margin-bottom:0">⚡ FLUX D'ÉNERGIE EN TEMPS RÉEL</div>
        <div style="font-size:10.5px;color:#5070a0">
          <span style="color:#3de8c0">━</span> Production &nbsp;
          <span style="color:#ffd060">━</span> Consommation &nbsp;
          <span style="color:#60b4ff">━</span> Stockage &nbsp;
          <span style="color:#b060ff">━</span> Réseau &nbsp;&nbsp; Vue : Schéma ▾
        </div>
      </div>
      <div style="display:grid;grid-template-columns:185px 1fr 210px;gap:12px;align-items:center">

        <div class="fnode" style="--bc:#1a4030;--bg:#081810">
          <div style="font-size:28px;margin-bottom:4px">☀️</div>
          <div class="fnode-lbl" style="color:#3de8c0">PANNEAUX PV</div>
          <div class="fnode-val" style="color:#3de8c0">2.45 kW</div>
          <div style="font-size:10px;color:#3de8c0;margin-top:3px">18.7 kWh aujourd'hui</div>
        </div>

        <div style="display:flex;flex-direction:column;align-items:center;gap:6px">
          <div style="font-size:10px;color:#3de8c0;display:flex;align-items:center;gap:4px">
            2.45 kW &nbsp;<span style="font-size:22px;letter-spacing:-4px">⟶⟶⟶</span>
          </div>
          <div class="fnode" style="--bc:#1a304a;--bg:#081828;width:115px">
            <div style="font-size:20px">⚡</div>
            <div class="fnode-lbl" style="color:#60b4ff">ONDULEUR</div>
            <div class="fnode-val" style="color:#60b4ff;font-size:1.5rem">97%</div>
          </div>
          <div style="text-align:center;font-size:10px;color:#60b4ff">0.85 kW<br><span style="font-size:18px">⬇</span></div>
          <div class="fnode" style="--bc:#1a304a;--bg:#081828;width:145px">
            <div style="font-size:16px">🔋</div>
            <div class="fnode-lbl" style="color:#60b4ff">BATTERIE</div>
            <div class="fnode-val" style="color:#60b4ff;font-size:1.4rem">80%</div>
            <div style="font-size:9px;color:#7090b8">48.0 V &nbsp; 40.0 A</div>
            <div style="font-size:9px;color:#3de8c0;margin-top:2px">4.4 kWh stockés</div>
          </div>
        </div>

        <div style="display:flex;flex-direction:column;gap:10px">
          <div style="display:flex;align-items:center;gap:6px">
            <div style="font-size:10px;color:#ffd060;white-space:nowrap;text-align:center">1.60 kW<br><span style="font-size:18px">⟶</span></div>
            <div class="fnode" style="--bc:#3a2800;--bg:#1a1200;flex:1">
              <div style="font-size:20px">🏠</div>
              <div class="fnode-lbl" style="color:#ffd060">CHARGE</div>
              <div class="fnode-val" style="color:#ffd060;font-size:1.4rem">1.60 kW</div>
              <div style="font-size:9px;color:#ffd060">14.3 kWh aujourd'hui</div>
            </div>
          </div>
          <div style="display:flex;align-items:center;gap:6px">
            <div style="font-size:10px;color:#b060ff;white-space:nowrap;text-align:center">0.85 kW<br><span style="font-size:18px">⟶</span></div>
            <div class="fnode" style="--bc:#2a1050;--bg:#120820;flex:1">
              <div style="font-size:20px">🔌</div>
              <div class="fnode-lbl" style="color:#b060ff">RÉSEAU</div>
              <div class="fnode-val" style="color:#b060ff;font-size:1.4rem">-0.85 kW</div>
              <div style="font-size:9px;color:#b060ff">Importation</div>
            </div>
          </div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="scard">', unsafe_allow_html=True)
    st.markdown('<div class="stitle">📈 PERFORMANCE DU SYSTÈME</div>', unsafe_allow_html=True)
    tc1,tc2,tc3,tc4 = st.columns(4)
    for col, label in zip([tc1,tc2,tc3,tc4],["Jour","Semaine","Mois","Année"]):
        bg = "background:#1a3050;color:#60b4ff;border:1px solid #264060" if label=="Jour" else "color:#5070a0"
        col.markdown(f'<div style="text-align:center;padding:3px 8px;border-radius:5px;font-size:11px;{bg}">{label}</div>', unsafe_allow_html=True)
    st.altair_chart(make_perf_chart(hours, prod, cons, stor, net), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    # RÉPARTITION
    st.markdown('<div class="scard">', unsafe_allow_html=True)
    st.markdown('<div class="stitle">🥧 RÉPARTITION ÉNERGÉTIQUE</div>', unsafe_allow_html=True)
    pie_html = pie_svg([54,28,18], ["#3de8c0","#ffd060","#60b4ff"],
                       ["Production PV","Consommation","Stockage"])
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px">
      {pie_html}
      <div style="font-size:11px;line-height:2">
        <div><span style="color:#3de8c0">●</span> Production PV (54%)</div>
        <div><span style="color:#ffd060">●</span> Consommation (28%)</div>
        <div><span style="color:#60b4ff">●</span> Stockage (18%)</div>
      </div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ANALYSE QUOTIDIENNE
    st.markdown('<div class="scard">', unsafe_allow_html=True)
    st.markdown('<div class="stitle">📊 ANALYSE QUOTIDIENNE</div>', unsafe_allow_html=True)
    st.altair_chart(make_bar_chart(hours, prod, cons), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # APPAREILS
    st.markdown("""
    <div class="scard">
      <div class="stitle">📱 APPAREILS CONNECTÉS</div>
      <div class="drow"><span>⚡ Onduleur</span><span><span class="donline">En ligne</span>&nbsp;<span class="dval" style="color:#60b4ff">2.45 kW</span></span></div>
      <div class="drow"><span>🔋 Batterie</span><span><span class="donline">En ligne</span>&nbsp;<span class="dval" style="color:#60b4ff">0.85 kW</span></span></div>
      <div class="drow"><span>📊 Smart Meter</span><span><span class="donline">En ligne</span>&nbsp;<span class="dval" style="color:#b060ff">-0.85 kW</span></span></div>
      <div class="drow"><span>☀️ Panneaux PV</span><span><span class="donline">En ligne</span>&nbsp;<span class="dval" style="color:#3de8c0">2.45 kW</span></span></div>
      <div class="drow"><span>🏠 Charge Principale</span><span><span class="donline">En ligne</span>&nbsp;<span class="dval" style="color:#ffd060">1.60 kW</span></span></div>
      <div style="margin-top:10px;background:#0e1e30;border-radius:6px;padding:7px;text-align:center;font-size:11px;color:#60b4ff">Voir tous les appareils &nbsp;›</div>
    </div>""", unsafe_allow_html=True)

# ── BILAN ────────────────────────────────────────────────────────────────────────
_, bcol = st.columns([2.25, 1])
with bcol:
    st.markdown("""
    <div class="scard">
      <div class="stitle">💰 BILAN ÉNERGÉTIQUE <span style="font-size:9px;color:#5070a0">(AUJOURD'HUI)</span></div>
      <div class="brow"><span style="color:#3de8c0">⚡ Énergie produite</span><span class="bval" style="color:#3de8c0">18.7 kWh</span></div>
      <div class="brow"><span style="color:#ffd060">🏠 Énergie consommée</span><span class="bval" style="color:#ffd060">14.3 kWh</span></div>
      <div class="brow"><span style="color:#60b4ff">🔋 Énergie stockée</span><span class="bval" style="color:#60b4ff">4.4 kWh</span></div>
      <div class="brow"><span style="color:#b060ff">🔌 Énergie importée</span><span class="bval" style="color:#b060ff">2.1 kWh</span></div>
      <div class="brow"><span style="color:#7090b8">📤 Énergie exportée</span><span class="bval" style="color:#7090b8">0.0 kWh</span></div>
      <div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px;background:#081c10;border:1px solid #1a4028;border-radius:8px;padding:9px 14px">
        <span style="font-size:12px;color:#3de8c0">⟳ Auto-consommation</span>
        <span style="font-family:'Rajdhani',sans-serif;font-size:2rem;font-weight:700;color:#3de8c0">72%</span>
      </div>
    </div>""", unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="fbar">
  <div class="sys-ok">
    <div class="sys-icon">✅</div>
    <div><div class="sys-lbl">SYSTÈME SAIN</div><div class="sys-sub">Aucune alarme active</div></div>
  </div>
  <div class="fbar-item">
    <div class="fbar-lbl">🌿 Émissions CO₂ évitées</div>
    <div class="fbar-val" style="color:#3de8c0">12.6 <span style="font-size:1rem">kg</span></div>
    <div class="fbar-sub">Aujourd'hui</div>
  </div>
  <div class="fbar-item">
    <div class="fbar-lbl">🌳 Équivalent arbres plantés</div>
    <div class="fbar-val" style="color:#3de8c0">0.6</div>
    <div class="fbar-sub">Aujourd'hui</div>
  </div>
  <div class="fbar-item">
    <div class="fbar-lbl">💰 Économie réalisée</div>
    <div class="fbar-val" style="color:#ffd060">2.35 <span style="font-size:1rem">€</span></div>
    <div class="fbar-sub">Aujourd'hui</div>
  </div>
</div>""", unsafe_allow_html=True)
