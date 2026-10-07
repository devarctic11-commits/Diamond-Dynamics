"""
GemValuate AI: Intelligent Diamond Valuation & Market Segmentation
Interactive Streamlit Web Application
Luxury Gemological Intelligence Platform
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="GemValuate AI | Diamond Valuation & Market Intelligence",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN LUXURY CSS STYLING (EMERALD LUXE & CHAMPAGNE GOLD) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Overall background styling adjustments */
    .stApp {
        background: #0a0f17;
        color: #f1f5f9;
    }
    
    /* Header Gradient Banner - Emerald Luxe & Obsidian */
    .hero-banner {
        background: radial-gradient(circle at 12% 18%, rgba(5, 150, 105, 0.28) 0%, rgba(10, 15, 23, 0.95) 70%),
                    linear-gradient(135deg, #06231c 0%, #0d1e18 45%, #0a131b 100%);
        border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 20px;
        padding: 34px 40px;
        margin-bottom: 24px;
        box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.7), 
                    inset 0 1px 0 rgba(110, 231, 183, 0.25),
                    0 0 25px -5px rgba(16, 185, 129, 0.12);
    }
    
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(120deg, #ffffff 15%, #6ee7b7 55%, #fde68a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 400;
        max-width: 860px;
        line-height: 1.6;
    }
    
    /* Preset Bar Container */
    .preset-container {
        background: rgba(17, 24, 39, 0.75);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 22px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* Luxury Metric Cards */
    .metric-card {
        background: rgba(15, 23, 34, 0.75);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 10px 28px -6px rgba(0, 0, 0, 0.45);
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }
    
    .metric-card:hover {
        border-color: rgba(52, 211, 153, 0.55);
        transform: translateY(-3px);
        box-shadow: 0 14px 34px -6px rgba(16, 185, 129, 0.22);
    }
    
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94a3b8;
        margin-bottom: 6px;
        font-weight: 700;
    }
    
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #34d399;
        font-feature-settings: "tnum";
    }
    
    .metric-sub {
        font-size: 0.85rem;
        color: #cbd5e1;
        margin-top: 5px;
    }
    
    /* Result Showcase Banner */
    .price-showcase {
        background: radial-gradient(circle at 50% 0%, rgba(16, 185, 129, 0.22) 0%, rgba(15, 23, 36, 0.92) 80%),
                    linear-gradient(135deg, rgba(6, 78, 59, 0.3) 0%, rgba(17, 24, 39, 0.6) 100%);
        border: 1.5px solid rgba(52, 211, 153, 0.45);
        border-radius: 18px;
        padding: 28px 24px;
        text-align: center;
        margin-top: 15px;
        box-shadow: 0 16px 40px -8px rgba(16, 185, 129, 0.3), inset 0 1px 1px rgba(254, 240, 138, 0.25);
    }
    
    .price-number {
        font-family: 'Outfit', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        color: #34d399;
        margin: 8px 0;
        text-shadow: 0 0 28px rgba(52, 211, 153, 0.55), 0 0 55px rgba(16, 185, 129, 0.25);
        letter-spacing: -0.5px;
    }
    
    .cluster-tag {
        display: inline-block;
        padding: 7px 18px;
        background: linear-gradient(135deg, #065f46 0%, #10b981 100%);
        color: #ffffff;
        font-weight: 700;
        font-size: 0.95rem;
        border-radius: 9999px;
        letter-spacing: 0.3px;
        border: 1px solid rgba(110, 231, 183, 0.3);
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.35);
    }

    .gold-badge {
        display: inline-block;
        padding: 5px 14px;
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.4);
        color: #fde68a;
        font-size: 0.85rem;
        font-weight: 600;
        border-radius: 8px;
        margin-top: 6px;
    }
    
    /* Sidebar Brand Styling */
    .sidebar-brand {
        padding: 16px 0 22px 0;
        border-bottom: 1px solid rgba(16, 185, 129, 0.2);
        margin-bottom: 22px;
    }

    .brand-glow {
        color: #34d399;
        font-family: 'Outfit', sans-serif;
        font-size: 1.55rem;
        font-weight: 800;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;
        letter-spacing: -0.5px;
    }
    
    /* Preset quick buttons custom styling */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        border-color: #10b981 !important;
        color: #34d399 !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.25);
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        border: 1px solid #34d399 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.35) !important;
    }

    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 28px rgba(16, 185, 129, 0.55) !important;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD ARTIFACTS WITH CACHING ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

@st.cache_resource
def load_models():
    reg_model = joblib.load(os.path.join(MODELS_DIR, "best_regression_model.pkl"))
    scaler_reg = joblib.load(os.path.join(MODELS_DIR, "scaler_regression.pkl"))
    reg_features = joblib.load(os.path.join(MODELS_DIR, "regression_features.pkl"))
    
    cluster_model = joblib.load(os.path.join(MODELS_DIR, "clustering_model.pkl"))
    scaler_cluster = joblib.load(os.path.join(MODELS_DIR, "scaler_cluster.pkl"))
    pca_2d = joblib.load(os.path.join(MODELS_DIR, "pca_2d.pkl"))
    pca_3d = joblib.load(os.path.join(MODELS_DIR, "pca_3d.pkl"))
    cluster_features = joblib.load(os.path.join(MODELS_DIR, "cluster_features.pkl"))
    
    return {
        'reg_model': reg_model,
        'scaler_reg': scaler_reg,
        'reg_features': reg_features,
        'cluster_model': cluster_model,
        'scaler_cluster': scaler_cluster,
        'pca_2d': pca_2d,
        'pca_3d': pca_3d,
        'cluster_features': cluster_features
    }

@st.cache_data
def load_metadata():
    with open(os.path.join(MODELS_DIR, "category_mappings.json")) as f:
        mappings = json.load(f)
    with open(os.path.join(MODELS_DIR, "regression_metrics.json")) as f:
        reg_metrics = json.load(f)
    with open(os.path.join(MODELS_DIR, "clustering_metrics.json")) as f:
        cluster_metrics = json.load(f)
    sample_df = pd.read_csv(os.path.join(MODELS_DIR, "diamonds_app_sample.csv"))
    
    return mappings, reg_metrics, cluster_metrics, sample_df

try:
    artifacts = load_models()
    mappings, reg_metrics, cluster_metrics, sample_df = load_metadata()
    USD_TO_INR = reg_metrics.get('conversion_rate_usd_to_inr', 83.0)
except Exception as e:
    st.error(f"Error loading model artifacts: {e}. Please ensure model files are intact in the models/ folder.")
    st.stop()


# --- LUXURY PLOTLY HELPER FOR SEAMLESS STYLING ---
def style_plotly_chart(fig, height=360, title=None):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(15, 23, 34, 0.45)",
        plot_bgcolor="rgba(15, 23, 34, 0.45)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#cbd5e1"),
        title=dict(font=dict(family="Outfit, sans-serif", size=15, color="#f1f5f9")) if title else None,
        margin=dict(l=25, r=25, t=45 if title else 25, b=25),
        height=height
    )
    fig.update_xaxes(gridcolor="rgba(148, 163, 184, 0.1)", zerolinecolor="rgba(148, 163, 184, 0.2)")
    fig.update_yaxes(gridcolor="rgba(148, 163, 184, 0.1)", zerolinecolor="rgba(148, 163, 184, 0.2)")
    return fig


# --- SESSION STATE INITIALIZATION FOR PRESETS ---
if "carat_input" not in st.session_state:
    st.session_state.carat_input = 0.70
if "cut_input" not in st.session_state:
    st.session_state.cut_input = "Ideal"
if "color_input" not in st.session_state:
    st.session_state.color_input = "F"
if "clarity_input" not in st.session_state:
    st.session_state.clarity_input = "VS1"
if "x_input" not in st.session_state:
    st.session_state.x_input = 5.65
if "y_input" not in st.session_state:
    st.session_state.y_input = 5.68
if "z_input" not in st.session_state:
    st.session_state.z_input = 3.52
if "depth_input" not in st.session_state:
    st.session_state.depth_input = 61.8
if "table_input" not in st.session_state:
    st.session_state.table_input = 57.0

def set_spec_preset(c_val, cut_val, col_val, clar_val, x_val, y_val, z_val, d_val, t_val):
    st.session_state.carat_input = c_val
    st.session_state.cut_input = cut_val
    st.session_state.color_input = col_val
    st.session_state.clarity_input = clar_val
    st.session_state.x_input = x_val
    st.session_state.y_input = y_val
    st.session_state.z_input = z_val
    st.session_state.depth_input = d_val
    st.session_state.table_input = t_val


# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-glow">✨ GemValuate AI</div>
        <p style="font-size:0.83rem; color:#94a3b8; margin:4px 0 0 0; letter-spacing:0.3px;">
            Intelligent Valuation & Market Intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    nav_option = st.radio(
        "Navigation Portal",
        [
            "💎 Precision Valuation & Cluster Engine",
            "🏷️ Luxury Market Segmentation Explorer",
            "📊 Gemstone Statistical EDA & Trends",
            "🤖 AI Benchmark & Deep Learning (ANN)",
            "📖 Gemology 4Cs & Algorithmic Blueprint"
        ],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 💱 Real-Time Currency Anchor")
    st.markdown(f"""
    <div style="background:rgba(245, 158, 11, 0.1); border:1px solid rgba(245, 158, 11, 0.3); border-radius:10px; padding:12px; text-align:center;">
        <span style="font-size:0.8rem; color:#fde68a; text-transform:uppercase; font-weight:700; letter-spacing:0.8px;">Fixed Valuation Anchor</span>
        <div style="font-size:1.25rem; font-weight:800; color:#fbbf24; margin-top:2px;">1 USD ($) = {USD_TO_INR:.1f} INR (₹)</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🏆 Production AI Architecture")
    st.markdown(f"""
    <div style="font-size:0.88rem; line-height:1.7; color:#cbd5e1;">
        • <b>Top Regressor:</b> <span style="color:#34d399;">{reg_metrics['best_model']}</span> ($R^2 = {reg_metrics['results'][reg_metrics['best_model']]['R2']:.4f}$)<br>
        • <b>Segmentation:</b> <span style="color:#fbbf24;">K-Means (k={cluster_metrics['optimal_k']})</span><br>
        • <b>PCA Variance:</b> <span style="color:#6ee7b7;">{cluster_metrics['pca_variance']['2D_total_variance']*100:.1f}% (2D) | {cluster_metrics['pca_variance']['3D_total_variance']*100:.1f}% (3D)</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("✨ Developed for Advanced Diamond Market Analytics & Decision Support.")


# ==============================================================================
# TAB 1: VALUATION & CLUSTERING ENGINE
# ==============================================================================
if nav_option == "💎 Precision Valuation & Cluster Engine":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Diamond Valuation & Market Segment Predictor</div>
        <div class="hero-subtitle">
            Configure gemstone 4C attributes and geometric facet proportions to predict real-time market valuation in <b>INR (₹)</b> 
            powered by our gradient-boosted ensemble regressor (XGBoost) and identify the customer market segment.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # RAPID SPECIFICATION PRESETS (One-Click Selection)
    st.markdown("##### ⚡ Quick-Spec Presets (One-Click Auto-Fill):")
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        st.button("💍 Classic Solitaire (0.90 ct)", on_click=set_spec_preset, 
                  args=(0.90, "Ideal", "G", "VS1", 6.20, 6.24, 3.85, 61.8, 56.0), use_container_width=True)
    with p_col2:
        st.button("👑 Royal Investment (2.05 ct)", on_click=set_spec_preset, 
                  args=(2.05, "Ideal", "D", "IF", 8.20, 8.25, 5.08, 61.7, 57.0), use_container_width=True)
    with p_col3:
        st.button("🏷️ Everyday Commercial (0.45 ct)", on_click=set_spec_preset, 
                  args=(0.45, "Good", "H", "SI1", 4.90, 4.95, 3.05, 62.2, 58.0), use_container_width=True)
    with p_col4:
        st.button("✨ Elite Collector (1.50 ct)", on_click=set_spec_preset, 
                  args=(1.50, "Premium", "E", "VVS1", 7.35, 7.40, 4.55, 61.5, 57.0), use_container_width=True)

    st.write("")
    col_input, col_result = st.columns([1.1, 1.2], gap="large")
    
    with col_input:
        st.subheader("⚙️ Diamond Specifications")
        
        # Carat Weight
        carat = st.number_input(
            "Carat Weight (ct)",
            min_value=0.10,
            max_value=5.00,
            step=0.01,
            key="carat_input",
            help="Mass of the diamond in carats (1 carat = 200 milligrams)."
        )
        
        # Cut, Color, Clarity
        c1, c2, c3 = st.columns(3)
        with c1:
            cut = st.selectbox(
                "Cut Quality",
                options=mappings['cut_order'],
                key="cut_input",
                help="Facet proportion quality: Fair, Good, Very Good, Premium, Ideal."
            )
        with c2:
            color = st.selectbox(
                "Color Grade",
                options=mappings['color_order'],
                key="color_input",
                help="Colorless D (rarest) to faint yellow/brown J."
            )
        with c3:
            clarity = st.selectbox(
                "Clarity Grade",
                options=mappings['clarity_order'],
                key="clarity_input",
                help="Purity rating under 10x magnification from Flawless (IF) to Included (I1)."
            )
        
        # Dimensions x, y, z
        st.markdown("#### 📏 Physical Dimensions (mm)")
        d1, d2, d3 = st.columns(3)
        with d1:
            x = st.number_input("Length x (mm)", min_value=1.0, max_value=15.0, step=0.05, key="x_input")
        with d2:
            y = st.number_input("Width y (mm)", min_value=1.0, max_value=15.0, step=0.05, key="y_input")
        with d3:
            z = st.number_input("Depth z (mm)", min_value=1.0, max_value=12.0, step=0.05, key="z_input")
            
        # Depth % and Table %
        st.markdown("#### 📐 Proportions & Facet Angles (%)")
        p1, p2 = st.columns(2)
        with p1:
            depth = st.slider("Total Depth %", min_value=50.0, max_value=75.0, step=0.1, key="depth_input")
        with p2:
            table = st.slider("Table Width %", min_value=45.0, max_value=75.0, step=0.5, key="table_input")
            
        # Automated Derived Features Preview
        volume = x * y * z
        dim_ratio = (x + y) / (2.0 * z) if z > 0 else 1.0
        table_depth = table / depth if depth > 0 else 1.0
        
        if carat < 0.5:
            carat_cat = "Light"
        elif carat <= 1.5:
            carat_cat = "Medium"
        else:
            carat_cat = "Heavy"
            
        st.markdown("#### 🔍 Real-Time Derived Pipeline")
        f1, f2, f3 = st.columns(3)
        f1.markdown(f"""
        <div class="metric-card" style="padding:12px; text-align:center;">
            <div class="metric-label">Volume</div>
            <div style="font-size:1.15rem; font-weight:700; color:#34d399;">{volume:.1f} mm³</div>
        </div>
        """, unsafe_allow_html=True)
        f2.markdown(f"""
        <div class="metric-card" style="padding:12px; text-align:center;">
            <div class="metric-label">Dim Ratio</div>
            <div style="font-size:1.15rem; font-weight:700; color:#fbbf24;">{dim_ratio:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
        f3.markdown(f"""
        <div class="metric-card" style="padding:12px; text-align:center;">
            <div class="metric-label">Carat Class</div>
            <div style="font-size:1.15rem; font-weight:700; color:#6ee7b7;">{carat_cat}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        predict_btn = st.button("✨ Recalculate Valuation & Predict Cluster", type="primary", use_container_width=True)

    with col_result:
        st.subheader("💎 Valuation & Market Segment Output")
        
        # Prepare feature vector for Regression
        cut_enc = mappings['cut_map'][cut]
        color_enc = mappings['color_map'][color]
        clarity_enc = mappings['clarity_map'][clarity]
        carat_cat_enc = mappings['carat_cat_map'][carat_cat]
        
        reg_input = pd.DataFrame([{
            'carat': carat,
            'cut_encoded': cut_enc,
            'color_encoded': color_enc,
            'clarity_encoded': clarity_enc,
            'depth': depth,
            'table': table,
            'x': x,
            'y': y,
            'z': z,
            'volume': volume,
            'dimension_ratio': dim_ratio,
            'table_depth_ratio': table_depth,
            'carat_cat_encoded': carat_cat_enc
        }])[artifacts['reg_features']]
        
        # Predict Price
        pred_log = artifacts['reg_model'].predict(reg_input)[0]
        pred_price_inr = np.expm1(pred_log)
        pred_price_usd = pred_price_inr / USD_TO_INR
        price_per_carat_inr = pred_price_inr / carat
        price_per_carat_usd = pred_price_usd / carat
        
        # Cluster Prediction
        cluster_input = pd.DataFrame([{
            'carat': carat,
            'cut_encoded': cut_enc,
            'color_encoded': color_enc,
            'clarity_encoded': clarity_enc,
            'depth': depth,
            'table': table,
            'x': x,
            'y': y,
            'z': z,
            'volume': volume,
            'dimension_ratio': dim_ratio
        }])[artifacts['cluster_features']]
        
        cluster_input_scaled = artifacts['scaler_cluster'].transform(cluster_input)
        assigned_cluster = int(artifacts['cluster_model'].predict(cluster_input_scaled)[0])
        cluster_info = cluster_metrics['cluster_profiles'][str(assigned_cluster)]
        
        # Transform into PCA space
        pca_point_2d = artifacts['pca_2d'].transform(cluster_input_scaled)[0]
        
        # Valuation Tier Label
        if pred_price_usd > 10000:
            tier_badge = "👑 High-End Investment Grade"
        elif pred_price_usd > 4000:
            tier_badge = "✨ Premium Fine Jewelry"
        elif pred_price_usd > 1500:
            tier_badge = "💍 Commercial Mid-Market"
        else:
            tier_badge = "🏷️ Accessible Consumer Grade"

        # Display Price Showcase
        st.markdown(f"""
        <div class="price-showcase">
            <span class="metric-label" style="color:#6ee7b7; font-size:0.85rem;">Estimated AI Market Valuation</span>
            <div class="price-number">₹ {pred_price_inr:,.0f}</div>
            <div style="font-size:1.15rem; color:#f1f5f9; margin-bottom:12px; font-weight:600;">
                <span style="color:#fbbf24;">$ {pred_price_usd:,.2f} USD</span> &nbsp;•&nbsp; 
                <span style="color:#a7f3d0;">₹ {price_per_carat_inr:,.0f} / ct</span>
            </div>
            <div style="display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin-top:12px;">
                <span class="cluster-tag">🏷️ {cluster_info['segment_name']} (Cluster {assigned_cluster})</span>
                <span class="gold-badge">{tier_badge}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        # Cluster Profile Box
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #10b981; margin-bottom:16px;">
            <div style="font-size:1.05rem; font-weight:700; color:#34d399; margin-bottom:4px;">
                Segment Persona: {cluster_info['segment_name']}
            </div>
            <p style="font-size:0.88rem; color:#cbd5e1; margin-bottom:8px;">{cluster_info['description']}</p>
            <div style="font-size:0.84rem; color:#94a3b8; display:flex; gap:18px; flex-wrap:wrap;">
                <span>📊 Market Share: <b style="color:#f1f5f9;">{cluster_info['percentage']}%</b></span>
                <span>⚖️ Avg Carat: <b style="color:#f1f5f9;">{cluster_info['mean_carat']} ct</b></span>
                <span>💰 Avg Price: <b style="color:#f1f5f9;">₹ {cluster_info['mean_price_inr']:,.0f}</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Visual Position in PCA Space
        st.markdown("#### 🗺️ Market Cluster Position (PCA 2D Mapping)")
        
        pca_sample = sample_df.sample(n=min(1200, len(sample_df)), random_state=42)
        fig_pca = px.scatter(
            pca_sample,
            x='pca_1',
            y='pca_2',
            color='segment_name',
            opacity=0.45,
            labels={'pca_1': 'PC 1 (Mass & Volume)', 'pca_2': 'PC 2 (Cut & Proportion)', 'segment_name': 'Segment'},
            title="Diamond Position in Market Segment Space",
            color_discrete_sequence=['#10b981', '#34d399', '#f59e0b', '#f43f5e']
        )
        
        # Add User's Diamond Point
        fig_pca.add_trace(go.Scatter(
            x=[pca_point_2d[0]],
            y=[pca_point_2d[1]],
            mode='markers+text',
            marker=dict(symbol='star', size=20, color='#fde047', line=dict(color='#ffffff', width=2)),
            text=["⭐ Your Diamond"],
            textposition="top center",
            name="Configured Diamond"
        ))
        
        fig_pca = style_plotly_chart(fig_pca, height=330)
        fig_pca.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.32, xanchor="center", x=0.5, font=dict(size=10))
        )
        st.plotly_chart(fig_pca, use_container_width=True)


# ==============================================================================
# TAB 2: MARKET SEGMENTATION EXPLORER
# ==============================================================================
elif nav_option == "🏷️ Luxury Market Segmentation Explorer":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Market Segmentation & Clustering Analytics</div>
        <div class="hero-subtitle">
            Unsupervised machine learning via <b>K-Means (k=4)</b> segments the diamond inventory into four actionable retail personas.
            Evaluated rigorously using the <b>Elbow Method (Inertia)</b> and <b>Silhouette Analysis</b>, reduced with <b>PCA</b> without price leakage.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 4 Cluster Profile Cards
    st.subheader("👥 The 4 Diamond Market Personas")
    p_cols = st.columns(4)
    
    profiles = cluster_metrics['cluster_profiles']
    icons = ["⚖️", "✨", "👑", "💎"]
    colors = ["#10b981", "#34d399", "#fbbf24", "#f43f5e"]
    
    for i, c_idx in enumerate(sorted(profiles.keys())):
        p = profiles[c_idx]
        with p_cols[i]:
            st.markdown(f"""
            <div class="metric-card" style="border-top: 4px solid {colors[i]};">
                <div style="font-size:1.6rem; margin-bottom:4px;">{icons[i]}</div>
                <div class="metric-label" style="color:{colors[i]};">Cluster {c_idx}</div>
                <div style="font-size:1.15rem; font-weight:700; color:#f8fafc; margin-bottom:8px;">{p['segment_name']}</div>
                <p style="font-size:0.83rem; color:#94a3b8; height:50px; line-height:1.4;">{p['description']}</p>
                <hr style="border-color:rgba(16, 185, 129, 0.15); margin:8px 0;">
                <div style="font-size:0.85rem; color:#cbd5e1; margin-bottom:3px;"><b>Market Share:</b> <span style="color:#fde68a;">{p['percentage']}%</span></div>
                <div style="font-size:0.85rem; color:#cbd5e1; margin-bottom:3px;"><b>Avg Carat:</b> {p['mean_carat']} ct</div>
                <div style="font-size:0.85rem; color:#cbd5e1; margin-bottom:3px;"><b>Avg Price:</b> ₹ {p['mean_price_inr']:,.0f}</div>
                <div style="font-size:0.85rem; color:#cbd5e1;"><b>Common Cut:</b> {p['most_common_cut']}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.write("")
    
    # Elbow & Silhouette Curves + 3D PCA
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("📉 Elbow Method (Inertia Trajectory)")
        elbow_data = cluster_metrics['elbow_inertias']
        sil_data = cluster_metrics['silhouette_scores']
        
        k_vals = [int(k) for k in elbow_data.keys()]
        inertias = [elbow_data[str(k)] for k in k_vals]
        sils = [sil_data[str(k)] for k in k_vals]
        
        fig_eval = go.Figure()
        fig_eval.add_trace(go.Scatter(
            x=k_vals, y=inertias, name="Inertia (Elbow Curve)",
            mode='lines+markers', line=dict(color='#10b981', width=3),
            marker=dict(size=9, color='#34d399', line=dict(width=2, color='#ffffff'))
        ))
        fig_eval = style_plotly_chart(fig_eval, height=350, title="K-Means Inertia vs Number of Clusters (k)")
        fig_eval.update_layout(xaxis_title="Number of Clusters (k)", yaxis_title="Sum of Squared Errors (Inertia)")
        st.plotly_chart(fig_eval, use_container_width=True)
        
    with col_b:
        st.subheader("🎯 Silhouette Score Validation")
        fig_sil = go.Figure()
        fig_sil.add_trace(go.Bar(
            x=k_vals, y=sils, name="Silhouette Score",
            marker_color=['#475569' if k != 4 else '#10b981' for k in k_vals]
        ))
        fig_sil = style_plotly_chart(fig_sil, height=350, title="Silhouette Scores (k=4 chosen as optimal)")
        fig_sil.update_layout(xaxis_title="Number of Clusters (k)", yaxis_title="Silhouette Coefficient")
        st.plotly_chart(fig_sil, use_container_width=True)
        
    # Interactive 3D PCA Cluster Space
    st.subheader("🌌 3D Interactive PCA Cluster Projection")
    st.caption("Principal Component Analysis projects the 11 feature dimensions to 3 principal components capturing 80.3% of the total dataset variance.")
    
    pca_sample = sample_df.sample(n=min(2500, len(sample_df)), random_state=42)
    fig_3d = px.scatter_3d(
        pca_sample,
        x='pca_3d_1',
        y='pca_3d_2',
        z='pca_3d_3',
        color='segment_name',
        opacity=0.65,
        size_max=5,
        title="3D Diamond Market Clusters",
        labels={'pca_3d_1': 'PC 1 (Dimension/Volume)', 'pca_3d_2': 'PC 2 (Cut/Depth)', 'pca_3d_3': 'PC 3 (Clarity/Color)'},
        color_discrete_sequence=['#10b981', '#34d399', '#fbbf24', '#f43f5e']
    )
    fig_3d = style_plotly_chart(fig_3d, height=540)
    st.plotly_chart(fig_3d, use_container_width=True)


# ==============================================================================
# TAB 3: EXPLORATORY DATA ANALYTICS (EDA)
# ==============================================================================
elif nav_option == "📊 Gemstone Statistical EDA & Trends":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Gemstone Statistical EDA & Market Trends</div>
        <div class="hero-subtitle">
            Comprehensive exploratory analysis across <b>53,940 diamonds</b>, analyzing distribution skews, 
            valuation correlations, and the pricing impact across cut, color, and clarity.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Overview metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Dataset Records</div>
            <div class="metric-value">53,940</div>
            <div class="metric-sub">Cleaned & Engineered instances</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Median Price (INR)</div>
            <div class="metric-value" style="color:#fbbf24;">₹ 1,99,283</div>
            <div class="metric-sub">Fixed conversion @ 83.0 INR/USD</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Mean Carat Weight</div>
            <div class="metric-value">0.798 ct</div>
            <div class="metric-sub">Range: 0.20 - 5.01 ct</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Retention Integrity</div>
            <div class="metric-value" style="color:#6ee7b7;">99.7%</div>
            <div class="metric-sub">20 unphysical entries purged</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    
    eda_tab1, eda_tab2, eda_tab3 = st.tabs(["📊 Price & Carat Distributions", "💎 4Cs Price Impact", "🔥 Correlation Heatmap"])
    
    with eda_tab1:
        c1, c2 = st.columns(2)
        with c1:
            fig_hist = px.histogram(
                sample_df,
                x='price_inr',
                nbins=50,
                marginal="box",
                title="Diamond Price in INR (₹) Distribution (Right-Skewed)",
                color_discrete_sequence=['#10b981']
            )
            fig_hist = style_plotly_chart(fig_hist, height=390)
            st.plotly_chart(fig_hist, use_container_width=True)
            
        with c2:
            fig_carat = px.scatter(
                sample_df,
                x='carat',
                y='price_inr',
                color='cut',
                opacity=0.5,
                trendline="ols",
                title="Carat vs Price (INR) with Regression Trendline",
                color_discrete_sequence=['#10b981', '#34d399', '#6ee7b7', '#fbbf24', '#f43f5e']
            )
            fig_carat = style_plotly_chart(fig_carat, height=390)
            st.plotly_chart(fig_carat, use_container_width=True)
            
    with eda_tab2:
        c1, c2 = st.columns(2)
        with c1:
            fig_box_cut = px.box(
                sample_df,
                x='cut',
                y='price_inr',
                category_orders={'cut': mappings['cut_order']},
                color='cut',
                title="Price Distribution Across Cut Qualities",
                color_discrete_sequence=['#059669', '#10b981', '#34d399', '#fbbf24', '#f43f5e']
            )
            fig_box_cut = style_plotly_chart(fig_box_cut, height=390)
            fig_box_cut.update_layout(showlegend=False)
            st.plotly_chart(fig_box_cut, use_container_width=True)
            
        with c2:
            fig_box_clarity = px.box(
                sample_df,
                x='clarity',
                y='price_inr',
                category_orders={'clarity': mappings['clarity_order']},
                color='clarity',
                title="Price Distribution Across Clarity Grades",
                color_discrete_sequence=px.colors.sequential.Darkmint
            )
            fig_box_clarity = style_plotly_chart(fig_box_clarity, height=390)
            fig_box_clarity.update_layout(showlegend=False)
            st.plotly_chart(fig_box_clarity, use_container_width=True)
            
    with eda_tab3:
        corr_cols = ['carat', 'depth', 'table', 'x', 'y', 'z', 'volume', 'dimension_ratio', 'price_inr']
        corr_matrix = sample_df[corr_cols].corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            text_auto='.3f',
            color_continuous_scale='Emrld',
            title="Correlation Heatmap of Physical & Valuation Features",
            aspect="auto"
        )
        fig_corr = style_plotly_chart(fig_corr, height=480)
        st.plotly_chart(fig_corr, use_container_width=True)
        st.info("💡 **Insight:** Carat, Volume, and dimensions x, y, z exhibit near-perfect correlation with Price in INR (~0.90 to 0.92), verifying that physical displacement and mass represent the primary pricing drivers.")


# ==============================================================================
# TAB 4: MODEL BENCHMARK & ARCHITECTURE
# ==============================================================================
elif nav_option == "🤖 AI Benchmark & Deep Learning (ANN)":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Model Benchmark & Deep Learning Architecture</div>
        <div class="hero-subtitle">
            Evaluating 5 Regression algorithms alongside an <b>Artificial Neural Network (ANN)</b> trained on log1p-transformed prices.
            All architectures evaluated using <b>MAE (₹)</b>, <b>MSE</b>, <b>RMSE (₹)</b>, and <b>R² Score</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🏆 Model Evaluation Leaderboard")
    
    results = reg_metrics['results']
    results_df = pd.DataFrame(results).T.reset_index().rename(columns={'index': 'Model Name'})
    results_df = results_df.sort_values(by='R2', ascending=False).reset_index(drop=True)
    
    # Styled Table
    styled_df = results_df.copy()
    styled_df['MAE (INR)'] = styled_df['MAE'].apply(lambda v: f"₹ {v:,.2f}")
    styled_df['RMSE (INR)'] = styled_df['RMSE'].apply(lambda v: f"₹ {v:,.2f}")
    styled_df['MSE'] = styled_df['MSE'].apply(lambda v: f"{v:,.0f}")
    styled_df['R² Score'] = styled_df['R2'].apply(lambda v: f"{v:.4f}")
    
    st.dataframe(
        styled_df[['Model Name', 'R² Score', 'MAE (INR)', 'RMSE (INR)', 'MSE']],
        use_container_width=True,
        hide_index=True
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 R² Score Comparison (Higher is Better)")
        fig_r2 = px.bar(
            results_df,
            x='R2',
            y='Model Name',
            orientation='h',
            color='R2',
            color_continuous_scale='Teal',
            range_x=[0.94, 1.0],
            text='R2'
        )
        fig_r2.update_traces(texttemplate='%{text:.4f}', textposition='outside')
        fig_r2 = style_plotly_chart(fig_r2, height=350)
        st.plotly_chart(fig_r2, use_container_width=True)
        
    with col2:
        st.subheader("📉 Root Mean Squared Error (RMSE in ₹)")
        fig_rmse = px.bar(
            results_df,
            x='RMSE',
            y='Model Name',
            orientation='h',
            color='RMSE',
            color_continuous_scale='Oranges_r',
            text='RMSE'
        )
        fig_rmse.update_traces(texttemplate='₹ %{text:,.0f}', textposition='outside')
        fig_rmse = style_plotly_chart(fig_rmse, height=350)
        st.plotly_chart(fig_rmse, use_container_width=True)
        
    # Feature Importance Plot
    st.subheader("🌲 Feature Importance (from XGBoost Champion)")
    feat_imp = pd.DataFrame(list(reg_metrics['feature_importance'].items()), columns=['Feature', 'Importance'])
    feat_imp = feat_imp.sort_values(by='Importance', ascending=True)
    
    fig_imp = px.bar(
        feat_imp,
        x='Importance',
        y='Feature',
        orientation='h',
        color='Importance',
        color_continuous_scale='Emrld',
        title="Predictive Feature Weights"
    )
    fig_imp = style_plotly_chart(fig_imp, height=400)
    st.plotly_chart(fig_imp, use_container_width=True)
    
    # Deep Learning Architecture
    st.subheader("🧠 Deep Learning ANN Architecture Specification")
    st.markdown("""
    ```
    Input Layer: 13 Standardized Gemological Features
         │
         ▼
    Dense(128, activation='relu') + BatchNormalization() + Dropout(0.15)
         │
         ▼
    Dense(64, activation='relu') + BatchNormalization() + Dropout(0.10)
         │
         ▼
    Dense(32, activation='relu')
         │
         ▼
    Output Layer: Dense(1, linear) -> Predicts log1p(Price INR) -> expm1() Inversion
    
    Optimizer: Adam (lr=0.003) | Loss: Huber Loss | Callbacks: EarlyStopping, ReduceLROnPlateau
    ```
    """)


# ==============================================================================
# TAB 5: GEMOLOGY & PROJECT GUIDE
# ==============================================================================
elif nav_option == "📖 Gemology 4Cs & Algorithmic Blueprint":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Diamond Gemology & Algorithmic Blueprint</div>
        <div class="hero-subtitle">
            Comprehensive breakdown of the 4Cs diamond grading standards, mathematical formulas used in feature engineering, 
            and project architecture.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        ### 💎 The 4Cs of Diamond Grading
        - **Carat (Weight):** Measures gemstone mass. $1 \\text{ carat} = 200 \\text{ mg}$. The single dominant driver of physical market price.
        - **Cut (Proportion & Finish):** Categorized *Fair, Good, Very Good, Premium, Ideal*. Dictates internal light refraction, scintillation, and optical fire.
        - **Color (Grading Scale):** Evaluated from **D** (totally colorless, purest grade) down to **J** (detectable warm tint).
        - **Clarity (Purity Scale):** Evaluates microscopic inclusions and surface blemishes under 10x magnification, from **IF** (Internally Flawless) to **I1** (Included).
        """)
        
    with c2:
        st.markdown("""
        ### 📐 Feature Engineering Formulas
        - **INR Valuation:** $\\text{Price}_{\\text{INR}} = \\text{Price}_{\\text{USD}} \\times 83.0$
        - **Volumetric Mass:** $\\text{Volume} = x \\times y \\times z \\text{ mm}^3$
        - **Aspect Ratio:** $\\frac{x + y}{2 \\times z}$ (physical symmetry quotient)
        - **Facet Table Ratio:** $\\frac{\\text{Table}}{\\text{Depth}}$
        - **Carat Classification:**
          - *Light:* $< 0.5$ ct
          - *Medium:* $0.5 - 1.5$ ct
          - *Heavy:* $> 1.5$ ct
        """)
        
    st.markdown("---")
    st.markdown("""
    ### 🏢 Architecture Overview
    - **System:** GemValuate AI Platform
    - **Domain:** Luxury Retail Intelligence, Gemological Price Modeling & Consumer Segmentation
    - **Algorithms:** XGBoost Regressor, Random Forest, Decision Tree, KNN, Artificial Neural Network (TensorFlow/Keras), K-Means Clustering, PCA.
    """)

# Footer
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.82rem; margin-top: 55px; padding: 22px 0; border-top: 1px solid rgba(16, 185, 129, 0.15);">
    ✨ <b>GemValuate AI</b> • Next-Gen Diamond Valuation & Segment Architecture • End-to-End ML, ANN & PCA System
</div>
""", unsafe_allow_html=True)
