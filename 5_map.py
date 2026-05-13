import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import apply_styles, render_footer, render_sidebar
apply_styles()
render_sidebar()

# ==========================================
# PAGE: Vaccination Coverage Map
# ==========================================

st.title("🗺️ Vaccination Coverage Map")
st.markdown("Geographic distribution of vaccination coverage across regions.")
st.markdown("---")

# Summary Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("🏙️ Districts Covered", "24")
m2.metric("✅ Fully Vaccinated", "68%")
m3.metric("⚠️ Partial Coverage", "22%")
m4.metric("❌ Not Vaccinated", "10%")

st.markdown("---")

# Choropleth-style mock map using Plotly scatter_geo
st.subheader("📍 District-Level Coverage")

# Dummy lat/lon for Indian districts
districts = {
    "Mumbai":    (19.076, 72.877, 92),
    "Delhi":     (28.613, 77.209, 85),
    "Kolkata":   (22.572, 88.363, 78),
    "Chennai":   (13.082, 80.270, 88),
    "Hyderabad": (17.385, 78.486, 74),
    "Pune":      (18.520, 73.856, 81),
    "Jaipur":    (26.912, 75.787, 62),
    "Lucknow":   (26.846, 80.946, 55),
    "Bhopal":    (23.259, 77.413, 49),
    "Patna":     (25.594, 85.137, 41),
}

names    = list(districts.keys())
lats     = [v[0] for v in districts.values()]
lons     = [v[1] for v in districts.values()]
coverage = [v[2] for v in districts.values()]
colors   = ["#28a745" if c >= 75 else "#ffc107" if c >= 50 else "#dc3545" for c in coverage]

fig_map = go.Figure(go.Scattergeo(
    lat=lats, lon=lons,
    text=[f"{n}: {c}%" for n, c in zip(names, coverage)],
    mode='markers+text',
    textposition='top center',
    marker=dict(
        size=[c / 5 for c in coverage],
        color=coverage,
        colorscale=[[0, '#dc3545'], [0.5, '#ffc107'], [1, '#28a745']],
        cmin=0, cmax=100,
        colorbar=dict(title="Coverage %"),
        showscale=True
    )
))
fig_map.update_layout(
    geo=dict(
        scope='asia',
        center=dict(lat=22, lon=80),
        projection_scale=4,
        showland=True,
        landcolor='#f0f4f8',
        showocean=True,
        oceancolor='#ddeeff',
        showcountries=True,
        countrycolor='#aac4dd',
    ),
    height=500,
    margin=dict(l=0, r=0, t=10, b=0)
)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")

# Table of coverage data
st.subheader("📊 District Coverage Summary")
df = pd.DataFrame({
    "District":  names,
    "Coverage %": coverage,
    "Status": ["🟢 Good" if c >= 75 else "🟡 Moderate" if c >= 50 else "🔴 At Risk" for c in coverage]
})
st.dataframe(df, use_container_width=True, hide_index=True)
