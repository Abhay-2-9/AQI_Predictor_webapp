import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AQI Predictor — India",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL STYLES
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* ── Unique warm-amber gradient mesh background ── */
  .stApp {
    background:
      radial-gradient(ellipse 65% 55% at 8% 5%,  rgba(251,191, 36,0.09) 0%, transparent 100%),
      radial-gradient(ellipse 50% 60% at 92% 95%, rgba(  5,150,105,0.07) 0%, transparent 100%),
      radial-gradient(ellipse 40% 40% at 55% 45%, rgba(180, 83,  9,0.04) 0%, transparent 100%),
      #13100d;
    color: #e8e0d4;
  }

  /* Hide Streamlit top bar */
  header[data-testid="stHeader"] { background: transparent !important; }
  #MainMenu, footer { visibility: hidden; }

  /* Container */
  .block-container {
    padding: 4rem 2.5rem 3rem 2.5rem !important;
    max-width: 1300px;
  }

  /* ── Section label (replaces .card-title) ── */
  .sec-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: #6b5e4e;
    margin-bottom: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }
  .sec-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, rgba(245,158,11,0.2), transparent);
    margin-left: 0.5rem;
  }

  /* ── Section divider ── */
  .sec-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 1.4rem 0;
  }

  /* Pollutant hint */
  .poll-hint {
    font-size: 0.7rem;
    color: #4a3f30;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 0.15rem;
  }

  /* AQI result card */
  .result-card {
    border-radius: 18px;
    padding: 2.5rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  .aqi-number {
    font-size: 5.5rem;
    font-weight: 900;
    line-height: 1;
    letter-spacing: -0.03em;
  }
  .aqi-cat {
    font-size: 1.6rem;
    font-weight: 700;
    margin-top: 0.4rem;
    letter-spacing: 0.02em;
  }
  .aqi-range {
    font-size: 0.8rem;
    opacity: 0.6;
    margin-top: 0.3rem;
    font-family: 'JetBrains Mono', monospace;
  }

  /* Advisory box */
  .advisory {
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    font-size: 0.88rem;
    line-height: 1.55;
    border-left: 4px solid;
  }

  /* Scale bar segment */
  .scale-seg {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    margin: 3px;
    letter-spacing: 0.03em;
    opacity: 0.5;
  }
  .scale-seg.active { opacity: 1; transform: scale(1.08); }

  /* Sensor status pills */
  .sensor-pill {
    display: inline-block;
    padding: 3px 9px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
    margin: 2px;
  }
  .sensor-on  { background: #052e16; color: #4ade80; border: 1px solid #166534; }
  .sensor-off { background: #1c1512; color: #57534e; border: 1px solid #292118;
                text-decoration: line-through; }

  /* Mini metric */
  .mini-metric {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 0.85rem 1rem;
    text-align: center;
  }
  .mini-metric .val {
    font-size: 1.6rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
  }
  .mini-metric .lbl {
    font-size: 0.66rem;
    color: #6b5e4e;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.15rem;
  }

  /* ── Widget overrides ── */
  .stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border-color: rgba(255,255,255,0.1) !important;
    color: #e8e0d4 !important;
    border-radius: 8px !important;
  }
  .stNumberInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border-color: rgba(255,255,255,0.1) !important;
    color: #e8e0d4 !important;
    border-radius: 8px !important;
  }
  .stCheckbox label { color: #7c6f5e !important; font-size: 0.82rem !important; }

  /* Predict button */
  .stButton > button {
    background: linear-gradient(135deg, #d97706, #b45309) !important;
    color: #fff8ed !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.7rem 2rem !important;
    letter-spacing: 0.02em !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
  }
  .stButton > button:hover { opacity: 0.88 !important; }

  hr { border-color: rgba(255,255,255,0.06); margin: 1.2rem 0; }
  .stSlider > div { padding: 0 !important; }

  /* Expander */
  .streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 8px !important;
    color: #7c6f5e !important;
    font-size: 0.8rem !important;
  }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
MONTHS = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",
          7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}

SEASON_MAP = {12:"Winter",1:"Winter",2:"Winter",
              3:"Summer",4:"Summer",5:"Summer",
              6:"Monsoon",7:"Monsoon",8:"Monsoon",9:"Monsoon",
              10:"Post-Monsoon",11:"Post-Monsoon"}

SEASON_ICONS = {"Winter":"❄️","Summer":"☀️","Monsoon":"🌧️","Post-Monsoon":"🍂"}

CPCB = {
    "Good":         {"range":(0,50),    "color":"#22c55e","bg":"#052e16","border":"#166534","icon":"😊",
                     "advice":"Air is clean. No restrictions — enjoy your day outdoors freely.",
                     "outdoor":"Safe to go outside. Great day for exercise, cycling, or a walk."},
    "Satisfactory": {"range":(51,100),  "color":"#86efac","bg":"#052e16","border":"#166534","icon":"🙂",
                     "advice":"Acceptable air quality. Minor discomfort only for highly sensitive individuals.",
                     "outdoor":"Generally safe outdoors. Very sensitive individuals (severe asthma) may want to limit prolonged exertion."},
    "Moderate":     {"range":(101,200), "color":"#fbbf24","bg":"#1c1506","border":"#92400e","icon":"😐",
                     "advice":"Breathing discomfort for sensitive groups — people with asthma, heart disease, children, and the elderly.",
                     "outdoor":"Healthy adults can go out. Sensitive groups should reduce outdoor time and avoid heavy exercise."},
    "Poor":         {"range":(201,300), "color":"#f97316","bg":"#1c0d05","border":"#9a3412","icon":"😷",
                     "advice":"Breathing discomfort for most people on prolonged exposure. Increased risk for sensitive groups.",
                     "outdoor":"Limit outdoor activities. Wear an N95 mask if going out. Avoid running, cycling, or sports."},
    "Very Poor":    {"range":(301,400), "color":"#ef4444","bg":"#1c0505","border":"#991b1b","icon":"🚫",
                     "advice":"Respiratory illness likely on prolonged exposure. Even healthy people face risk.",
                     "outdoor":"Avoid going outside. Keep windows and doors closed. Use air purifier indoors if possible."},
    "Severe":       {"range":(401,9999),"color":"#a855f7","bg":"#160b1c","border":"#6b21a8","icon":"☠️",
                     "advice":"Health emergency. Serious impact on healthy people; severe risk for those with existing conditions.",
                     "outdoor":"Stay indoors. Avoid all outdoor exposure. Seek medical attention if you experience breathing difficulty."},
}

POLLUTANT_META = {
    "PM2.5":  {"unit":"µg/m³","desc":"Fine particles (main AQI driver)","max":310.0,"step":0.5},
    "PM10":   {"unit":"µg/m³","desc":"Coarse particles","max":450.0,"step":1.0},
    "NO":     {"unit":"µg/m³","desc":"Nitric oxide","max":115.0,"step":0.5},
    "NO2":    {"unit":"µg/m³","desc":"Nitrogen dioxide","max":120.0,"step":0.5},
    "NOx":    {"unit":"µg/m³","desc":"Total nitrogen oxides","max":155.0,"step":0.5},
    "NH3":    {"unit":"µg/m³","desc":"Ammonia","max":135.0,"step":0.5},
    "CO":     {"unit":"mg/m³","desc":"Carbon monoxide (mg/m³, not µg)","max":36.0,"step":0.05},
    "SO2":    {"unit":"µg/m³","desc":"Sulfur dioxide","max":101.0,"step":0.5},
    "O3":     {"unit":"µg/m³","desc":"Ground-level ozone","max":106.0,"step":0.5},
    "Benzene":{"unit":"µg/m³","desc":"VOC from fuel/vehicles","max":29.0,"step":0.1},
    "Toluene":{"unit":"µg/m³","desc":"VOC from paint/solvents","max":77.0,"step":0.5},
}

PRIMARY_POLLUTANTS   = ["PM2.5","PM10","CO","NO2","SO2","O3"]
SECONDARY_POLLUTANTS = ["NO","NOx","NH3","Benzene","Toluene"]

# ─────────────────────────────────────────────────────────────────────────────
#  LOAD ARTIFACTS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    path = os.path.join(os.path.dirname(__file__), "aqi_artifacts.pkl")
    with open(path, "rb") as f:
        return pickle.load(f)

artifacts       = load_artifacts()
model           = artifacts["model"]
encoder         = artifacts["encoder"]
oe              = artifacts["oe"]
winsor_bounds   = artifacts["winsor_bounds"]
city_median     = artifacts["city_median"]
city_aqi_mean   = artifacts["city_aqi_mean"]
city_season_aqi = artifacts["city_season_aqi"]
CITIES          = artifacts["cities"]
FEATURE_COLS    = artifacts["feature_cols"]
POLLUTANT_COLS  = artifacts["pollutant_cols"]
city_swap       = artifacts["city_swap"]

# ─────────────────────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def get_category(aqi_val):
    for cat, info in CPCB.items():
        lo, hi = info["range"]
        if lo <= aqi_val <= hi:
            return cat, info
    return "Severe", CPCB["Severe"]

def predict_aqi(city, month, pollutant_vals: dict) -> float:
    season_str  = SEASON_MAP[month]
    city_enc    = city_swap.get(city, city)
    season_df   = pd.DataFrame([[season_str]], columns=["Season"])
    season_enc  = float(oe.transform(season_df)[0][0])
    row = {"City": city_enc}
    for col in POLLUTANT_COLS:
        val = pollutant_vals.get(col, np.nan)
        if val is None or (isinstance(val, float) and np.isnan(val)):
            row[col] = np.nan
        else:
            lo, hi = winsor_bounds[col]
            row[col] = float(np.clip(val, lo, hi))
    row["Month"]  = month
    row["Season"] = season_enc
    df_row = pd.DataFrame([row], columns=FEATURE_COLS)
    df_row[["City","Month"]] = encoder.transform(df_row[["City","Month"]])
    return float(model.predict(df_row)[0])

def get_city_typical(city, pollutant):
    try:
        val = city_median.loc[city, pollutant]
        return None if pd.isna(val) else round(float(val), 2)
    except Exception:
        return None

def get_hist_aqi(city, season_str):
    try:
        val = city_season_aqi.loc[city, season_str]
        return round(float(val), 0) if not pd.isna(val) else None
    except Exception:
        return None

# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "result"   not in st.session_state: st.session_state.result   = None
if "autofill" not in st.session_state: st.session_state.autofill = False

# Pre-initialise every number_input key to 0.0 on first load.
# This lets us drop the value= param from number_input entirely,
# avoiding the Streamlit conflict error when session state and value= disagree.
for _p in PRIMARY_POLLUTANTS + SECONDARY_POLLUTANTS:
    if f"inp_{_p}" not in st.session_state:
        st.session_state[f"inp_{_p}"] = 0.0

# ── Handle autofill BEFORE widgets render ──────────────────────────────────
# We write directly into the widget session-state keys (inp_<poll>).
# Streamlit picks these up when number_input renders — this is the only
# reliable way to programmatically update already-rendered number inputs.
if st.session_state.autofill:
    _city_for_fill = st.session_state.get("city_select", "Delhi")
    for _poll in PRIMARY_POLLUTANTS + SECONDARY_POLLUTANTS:
        _typical = get_city_typical(_city_for_fill, _poll)
        if _typical is not None:
            st.session_state[f"inp_{_poll}"] = float(_typical)
    st.session_state.autofill = False

# ─────────────────────────────────────────────────────────────────────────────
#  HEADER  (self-contained HTML — no Streamlit widgets inside)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:2.2rem;">
  <div style="font-size:0.68rem;letter-spacing:0.14em;text-transform:uppercase;
              color:#6b5e4e;font-weight:600;margin-bottom:0.6rem;">
    CPCB India Standard &nbsp;·&nbsp; XGBoost &nbsp;·&nbsp; R² 0.925
  </div>
  <div style="display:flex;align-items:center;gap:0.9rem;margin-bottom:0.5rem;">
    <div style="width:42px;height:42px;border-radius:12px;flex-shrink:0;
                background:linear-gradient(135deg,#d97706,#059669);
                display:flex;align-items:center;justify-content:center;
                font-size:1.3rem;box-shadow:0 4px 16px rgba(217,119,6,0.35);">
      🍃
    </div>
    <h1 style="font-size:2.3rem;font-weight:900;letter-spacing:-0.03em;
               margin:0;color:#f0e8d8;line-height:1;">
      India AQI Predictor
    </h1>
  </div>
  <p style="color:#6b5e4e;margin:0;font-size:0.92rem;padding-left:51px;">
    Pick your city, month, and pollutant readings.
    Mark any sensor <span style="color:#a8906e;font-weight:600;">unknown</span>
    — the model still predicts using NaN routing.
  </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  LAYOUT — two columns
# ─────────────────────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1, 1.55], gap="large")

# ══════════════════════════════════════════════════════
#  LEFT — Location & Time
# ══════════════════════════════════════════════════════
with left_col:

    # ── Section: Location ────────────────────────────
    st.markdown('<div class="sec-label">📍 Location & Time</div>', unsafe_allow_html=True)

    city = st.selectbox("City", CITIES, index=CITIES.index("Delhi"), key="city_select")
    month_num = st.selectbox("Month", list(MONTHS.keys()),
                             format_func=lambda x: MONTHS[x],
                             index=5, key="month_select")
    season_str = SEASON_MAP[month_num]

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:0.6rem;margin-top:0.5rem;">
      <span style="font-size:0.76rem;color:#6b5e4e;">Season auto-detected:</span>
      <span style="background:rgba(245,158,11,0.12);border:1px solid rgba(245,158,11,0.25);
                   border-radius:20px;padding:3px 12px;font-size:0.8rem;
                   font-weight:600;color:#f59e0b;">
        {SEASON_ICONS[season_str]}&nbsp;{season_str}
      </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="sec-divider">', unsafe_allow_html=True)

    # ── Section: Historical Context ──────────────────
    st.markdown('<div class="sec-label">📊 Historical Context (2015–2020)</div>',
                unsafe_allow_html=True)

    hist_aqi  = get_hist_aqi(city, season_str)
    city_mean = float(city_aqi_mean.get(city, 0))
    _, cat_info_hist = get_category(hist_aqi or city_mean)
    _, cat_info_city = get_category(city_mean)

    c1, c2 = st.columns(2)
    c1.markdown(f"""
    <div class="mini-metric">
      <div class="val" style="color:{cat_info_hist['color']};">
        {int(hist_aqi) if hist_aqi else '—'}
      </div>
      <div class="lbl">Typical {season_str[:3]} AQI</div>
    </div>""", unsafe_allow_html=True)
    c2.markdown(f"""
    <div class="mini-metric">
      <div class="val" style="color:{cat_info_city['color']};">{int(city_mean)}</div>
      <div class="lbl">City annual avg</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <p style="font-size:0.76rem;color:#4a3f30;margin-top:0.8rem;line-height:1.55;">
      Reference only — your readings may differ due to local events, weather, or construction.
    </p>""", unsafe_allow_html=True)

    st.markdown('<hr class="sec-divider">', unsafe_allow_html=True)

    # ── Section: Model Info ──────────────────────────
    st.markdown('<div class="sec-label">🤖 Model Info</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.81rem;color:#6b5e4e;line-height:1.85;">
      <b style="color:#a8906e;">Algorithm</b> &nbsp;&nbsp;XGBoost Regressor<br>
      <b style="color:#a8906e;">Training data</b> &nbsp;&nbsp;24,850 records · 26 cities<br>
      <b style="color:#a8906e;">Test MAE</b> &nbsp;&nbsp;~18.9 AQI points<br>
      <b style="color:#a8906e;">Test R²</b> &nbsp;&nbsp;0.925<br>
      <b style="color:#a8906e;">Missing sensors</b> &nbsp;&nbsp;XGBoost NaN routing<br>
      <b style="color:#a8906e;">Top predictors</b> &nbsp;&nbsp;PM2.5 · CO · PM10 · City
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  RIGHT — Pollutant Inputs
# ══════════════════════════════════════════════════════
with right_col:

    # Header row (pure HTML — no Streamlit widgets)
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:flex-end;
                margin-bottom:0.85rem;">
      <div class="sec-label" style="margin-bottom:0;">💨 Pollutant Readings</div>
      <div style="font-size:0.72rem;color:#4a3f30;">
        Check <b style="color:#7c6f5e;">"Don't know"</b> for offline sensors
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Auto-fill button (Streamlit widget — outside any HTML wrapper)
    if st.button(f"⚡  Auto-fill with {city} typical values", key="autofill_btn"):
        st.session_state.autofill = True

    st.markdown("")

    # ── Primary pollutants ────────────────────────────
    st.markdown("""
    <div style="font-size:0.68rem;font-weight:700;color:#6b5e4e;text-transform:uppercase;
                letter-spacing:0.1em;margin-bottom:0.6rem;">
      ▸ Primary — most impactful
    </div>""", unsafe_allow_html=True)

    pollutant_vals = {}
    p_col1, p_col2 = st.columns(2)

    for i, poll in enumerate(PRIMARY_POLLUTANTS):
        col = p_col1 if i % 2 == 0 else p_col2
        meta    = POLLUTANT_META[poll]
        typical = get_city_typical(city, poll)

        with col:
            dont_know = st.checkbox("Don't know", key=f"dk_{poll}", value=False)
            st.markdown(
                f'<div style="font-size:0.82rem;font-weight:500;color:#a8906e;">'
                f'{poll} <span style="color:#4a3f30;font-family:JetBrains Mono,monospace;'
                f'font-size:0.68rem;">({meta["unit"]})</span></div>',
                unsafe_allow_html=True)
            if dont_know:
                st.markdown(
                    f'<div class="poll-hint">Offline → NaN routing'
                    f'{f" · typical {typical}" if typical else ""}</div>',
                    unsafe_allow_html=True)
                pollutant_vals[poll] = np.nan
            else:
                val = st.number_input(
                    label=poll, label_visibility="collapsed",
                    min_value=0.0, max_value=meta["max"],
                    step=meta["step"],
                    format="%.2f" if meta["step"] < 1 else "%.1f",
                    key=f"inp_{poll}")
                if typical:
                    st.markdown(
                        f'<div class="poll-hint">city median: {typical} {meta["unit"]}</div>',
                        unsafe_allow_html=True)
                pollutant_vals[poll] = val if val > 0 else np.nan

    st.markdown('<hr class="sec-divider">', unsafe_allow_html=True)

    # ── Secondary pollutants ──────────────────────────
    with st.expander("▸ Secondary pollutants  —  NO, NOx, NH3, Benzene, Toluene",
                     expanded=False):
        s_col1, s_col2 = st.columns(2)
        for i, poll in enumerate(SECONDARY_POLLUTANTS):
            col     = s_col1 if i % 2 == 0 else s_col2
            meta    = POLLUTANT_META[poll]
            typical = get_city_typical(city, poll)

            with col:
                dont_know = st.checkbox("Don't know", key=f"dk_{poll}", value=False)
                st.markdown(
                    f'<div style="font-size:0.82rem;font-weight:500;color:#a8906e;">'
                    f'{poll} <span style="color:#4a3f30;font-family:JetBrains Mono,monospace;'
                    f'font-size:0.68rem;">({meta["unit"]})</span></div>',
                    unsafe_allow_html=True)
                if dont_know:
                    st.markdown(
                        f'<div class="poll-hint">Offline → NaN routing'
                        f'{f" · typical {typical}" if typical else ""}</div>',
                        unsafe_allow_html=True)
                    pollutant_vals[poll] = np.nan
                else:
                    val = st.number_input(
                        label=poll, label_visibility="collapsed",
                        min_value=0.0, max_value=meta["max"],
                        step=meta["step"],
                        format="%.2f" if meta["step"] < 1 else "%.1f",
                        key=f"inp_{poll}")
                    if typical:
                        st.markdown(
                            f'<div class="poll-hint">city median: {typical} {meta["unit"]}</div>',
                            unsafe_allow_html=True)
                    pollutant_vals[poll] = val if val > 0 else np.nan

    # ── Sensor status summary ─────────────────────────
    active_polls  = [p for p, v in pollutant_vals.items()
                     if not (isinstance(v, float) and np.isnan(v))]
    missing_polls = [p for p, v in pollutant_vals.items()
                     if isinstance(v, float) and np.isnan(v)]
    pills_html = (
        "".join(f'<span class="sensor-pill sensor-on">{p}</span>'  for p in active_polls) +
        "".join(f'<span class="sensor-pill sensor-off">{p}</span>' for p in missing_polls)
    )
    st.markdown(f"""
    <div style="margin:0.8rem 0 1.2rem 0;">
      <span style="font-size:0.68rem;color:#4a3f30;text-transform:uppercase;
                   letter-spacing:0.1em;font-weight:700;">
        Sensors active: {len(active_polls)} / 11
      </span>
      <div style="margin-top:0.4rem;">{pills_html}</div>
    </div>""", unsafe_allow_html=True)

    # ── Predict Button ────────────────────────────────
    predict = st.button("🔍  Predict AQI", key="predict_btn", type="primary")

    if predict:
        if len(active_polls) == 0:
            st.warning("Enter at least one pollutant reading to make a prediction.")
        else:
            with st.spinner("Running model…"):
                pred_aqi = max(0.0, predict_aqi(city, month_num, pollutant_vals))
                category, cat_info = get_category(pred_aqi)
            st.session_state.result = {
                "aqi": pred_aqi, "category": category, "cat_info": cat_info,
                "city": city, "month": MONTHS[month_num], "season": season_str,
                "active": active_polls, "missing": missing_polls,
            }

# ─────────────────────────────────────────────────────────────────────────────
#  RESULTS
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.result:
    r        = st.session_state.result
    aqi      = r["aqi"]
    category = r["category"]
    cat_info = r["cat_info"]
    color    = cat_info["color"]
    bg       = cat_info["bg"]
    border   = cat_info["border"]

    st.markdown('<hr class="sec-divider">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;
                color:#6b5e4e;font-weight:700;margin-bottom:1rem;">
      Prediction &nbsp;—&nbsp; {r['city'].upper()} &nbsp;·&nbsp;
      {r['month'].upper()} &nbsp;({r['season'].upper()})
    </div>""", unsafe_allow_html=True)

    res_left, res_right = st.columns([1, 1.4], gap="large")

    # ── AQI card ──────────────────────────────────────
    with res_left:
        lo, hi = cat_info["range"]
        hi_lbl = str(hi) if hi < 9999 else "500+"
        st.markdown(f"""
        <div class="result-card" style="background:{bg};border:2px solid {border};">
          <div style="font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;
                      color:{color};opacity:0.65;margin-bottom:0.5rem;font-weight:700;">
            Air Quality Index
          </div>
          <div class="aqi-number" style="color:{color};">{int(round(aqi))}</div>
          <div class="aqi-cat" style="color:{color};">{cat_info['icon']}&nbsp; {category}</div>
          <div class="aqi-range" style="color:{color};">CPCB range: {lo} – {hi_lbl}</div>
        </div>""", unsafe_allow_html=True)

        # Scale bar
        scale_html = '<div style="margin-top:0.85rem;text-align:center;">'
        for cat_name, cinfo in CPCB.items():
            active_cls = "active" if cat_name == category else ""
            scale_html += (
                f'<span class="scale-seg {active_cls}" '
                f'style="background:{cinfo["bg"]};color:{cinfo["color"]};'
                f'border:1px solid {cinfo["border"]};">{cat_name}</span>'
            )
        scale_html += '</div>'
        st.markdown(scale_html, unsafe_allow_html=True)

    # ── Advisory panel ────────────────────────────────
    with res_right:
        st.markdown(f"""
        <div class="advisory" style="background:{bg};border-left-color:{color};">
          <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;
                      color:{color};font-weight:700;margin-bottom:0.4rem;">Health Advisory</div>
          <div style="color:#d1c4b0;font-size:0.88rem;line-height:1.6;">{cat_info['advice']}</div>
        </div>""", unsafe_allow_html=True)

        # Outdoor recommendation
        go_icon = "✅" if aqi <= 100 else ("⚠️" if aqi <= 200 else "🚫")
        st.markdown(f"""
        <div class="advisory" style="background:rgba(255,255,255,0.03);
             border-left-color:rgba(255,255,255,0.12);">
          <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;
                      color:#6b5e4e;font-weight:700;margin-bottom:0.4rem;">Go outside?</div>
          <div style="color:#d1c4b0;font-size:0.88rem;line-height:1.6;">
            {go_icon} {cat_info['outdoor']}
          </div>
        </div>""", unsafe_allow_html=True)

        # Contextual tips
        tips = []
        if aqi > 100:  tips.append("Keep an <b>N95 mask</b> handy if going out.")
        if aqi > 150:  tips.append("Keep windows <b>closed</b> during peak traffic hours (8–11 AM, 6–9 PM).")
        if aqi > 200:  tips.append("Use an <b>air purifier</b> indoors if available.")
        if aqi > 300:  tips.append("People with respiratory conditions should <b>contact a doctor</b> if symptoms worsen.")
        if aqi <= 100: tips.append("<b>Good day</b> to air out your home — open windows in the morning.")
        if r["season"] == "Winter" and aqi > 150:
            tips.append("Winter temperature inversion traps pollutants — AQI typically peaks <b>7–10 PM</b>.")
        if r["season"] == "Monsoon":
            tips.append("Monsoon rains help clean the air — AQI usually drops after a good shower.")

        if tips:
            tips_html = "".join(
                f'<div style="font-size:0.82rem;color:#7c6f5e;line-height:1.6;'
                f'padding:0.2rem 0;">— {t}</div>' for t in tips
            )
            st.markdown(f"""
            <div style="margin-top:0.8rem;">
              <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;
                          color:#4a3f30;font-weight:700;margin-bottom:0.5rem;">Tips</div>
              {tips_html}
            </div>""", unsafe_allow_html=True)

        # Sensor summary
        pills = (
            "".join(f'<span class="sensor-pill sensor-on">{p}</span>'  for p in r["active"]) +
            "".join(f'<span class="sensor-pill sensor-off">{p}</span>' for p in r["missing"])
        )
        missing_note = (
            f'<div style="font-size:0.7rem;color:#3a3028;margin-top:0.4rem;">'
            f'{len(r["missing"])} missing → handled via XGBoost NaN routing</div>'
            if r["missing"] else ""
        )
        st.markdown(f"""
        <div style="margin-top:1rem;padding:0.85rem 1rem;
                    background:rgba(255,255,255,0.03);
                    border:1px solid rgba(255,255,255,0.06);border-radius:10px;">
          <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;
                      color:#4a3f30;font-weight:700;margin-bottom:0.5rem;">
            Sensors used
          </div>
          {pills}{missing_note}
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#3a3028;font-size:0.74rem;
            margin-top:3rem;padding-bottom:1rem;">
  Trained on CPCB India data &nbsp;·&nbsp; 26 cities &nbsp;·&nbsp; Jan 2015 – Jul 2020
  &nbsp;·&nbsp;
  <a href="https://app.cpcbccr.com/AQI_India/" target="_blank"
     style="color:#4a3f30;text-decoration:underline;">Official CPCB Sameer App ↗</a>
</div>
""", unsafe_allow_html=True)
