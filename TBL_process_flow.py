import streamlit as st
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="TBL Stool Matrix", layout="wide", page_icon="🎯")
st.title("🎯 Triple Bottom Line Matrix Mapper")
st.write("Select a goal from the sidebar to automatically load its strategic TBL configuration. Optional: Add an industry sector to see direct operational tasks.")

# 2. Define the Universal Strategic Goals Data Structure
STRATEGIC_GOALS_DATA = {
    "🚀 Scale Revenue": {
        "symbol": "🚀",
        "people": "Fair compensation structures to increase sales productivity.",
        "planet": "Digital invoicing transitions to eliminate corporate paper waste.",
        "profit": "Direct expansion into high-margin emerging market segments."
    },
    "👥 Improve Retention": {
        "symbol": "👥",
        "people": "Flexible work schedules and comprehensive mental wellness plans.",
        "planet": "Subsidized public transit passes to reduce employee commute footprint.",
        "profit": "Drastic reduction in expensive employee recruitment and onboarding costs."
    },
    "🛠️ Reduce Technical Debt": {
        "symbol": "🛠️",
        "people": "Upskilling development teams to eliminate daily frustration and burnout.",
        "planet": "Migrating to green cloud data centers with optimized code execution.",
        "profit": "Lowering long-term software infrastructure maintenance expenditures."
    },
    "🌍 Expand Market Share": {
        "symbol": "🌍",
        "people": "Localized community hiring initiatives for new distribution centers.",
        "planet": "Transitioning global shipping lanes to use eco-friendly biofuel carriers.",
        "profit": "Increasing overarching volume sales to establish a dominant market presence."
    },
    "⚡ Optimize Operations": {
        "symbol": "⚡",
        "people": "Ergonomic workspace updates to prevent operational repetitive strain injuries.",
        "planet": "Upgrading facilities to smart IoT-managed renewable energy grids.",
        "profit": "Streamlining manufacturing supply chains to cut waste overhead costs by 15%."
    }
}

# 3. Define the Optional Industry Sector Data Structure
INDUSTRY_SECTOR_DATA = {
    "🏭 Manufacturing & Production": {
        "people": "Cross-train assembly crews on ergonomic physical safety to prevent repetitive task fatigue.",
        "planet": "Implement 'design to reduce material waste' policies to eliminate structural pattern scrap upfront.",
        "profit": "Lower raw input material procurement costs (COGS) through scrap reductions."
    },
    "💻 Technology & Digital Services": {
        "people": "Enforce strict boundaries on async communication to prevent digital fatigue and screen burnout.",
        "planet": "Optimize raw data infrastructure and cloud asset storage to reduce server farm grid loads.",
        "profit": "Reduce ongoing infrastructure hosting outlays by removing dead database processing storage."
    },
    "🚚 Logistics & Distribution": {
        "people": "Optimize regional work dispatch scheduling sheets to guarantee realistic, stress-free road times.",
        "planet": "Streamline vehicle shipping routes and packaging box dimensions to shrink total carbon burn.",
        "profit": "Slash overall delivery expenditures per package by slashing empty truck cargo space."
    }
}

# 4. Sidebar Configuration
st.sidebar.header("1. Choose a Business Goal")
selected_goal_key = st.sidebar.radio(
    "Goal Selector", 
    list(STRATEGIC_GOALS_DATA.keys()),
    index=None,
    label_visibility="collapsed"
)

# Optional Step 2 Interface
st.sidebar.header("2. Add Industry Filter (Optional)")
selected_industry_key = st.sidebar.radio(
    "Industry Selector",
    ["None (View Universal Strategy)"] + list(INDUSTRY_SECTOR_DATA.keys()),
    index=0
)

# Safe Initialization Logic
if selected_goal_key is not None:
    active_goal_info = STRATEGIC_GOALS_DATA[selected_goal_key]
    active_emoji = active_goal_info["symbol"]
else:
    active_goal_info = None
    active_emoji = "❓"

# Determine if the optional industry details should load
has_industry = selected_industry_key != "None (View Universal Strategy)"
if has_industry:
    active_industry_info = INDUSTRY_SECTOR_DATA[selected_industry_key]
else:
    active_industry_info = None

# 5. Building the 3-Legged Stool Figure
fig = go.Figure()

# --- STEP 1: THE THREE STOOL LEGS (Drawn First / Sent to Back) ---
fig.add_shape(type="path", path="M 1.5,7.1 L 1.5,1.3 Q 2.5,0.7 3.5,1.3 L 3.5,7.1 Z", fillcolor="rgba(255, 165, 0, 0.4)", line=dict(color="Orange", width=2))
fig.add_shape(type="path", path="M 4.0,7.1 L 4.0,1.3 Q 5.0,0.7 6.0,1.3 L 6.0,7.1 Z", fillcolor="rgba(52, 152, 219, 0.4)", line=dict(color="SkyBlue", width=2))
fig.add_shape(type="path", path="M 6.5,7.1 L 6.5,1.3 Q 7.5,0.7 8.5,1.3 L 8.5,7.1 Z", fillcolor="rgba(46, 204, 113, 0.4)", line=dict(color="LightGreen", width=2))

# --- STEP 2: 3D OVAL SEAT ASSEMBLY (Drawn Over Leg Tops) ---
fig.add_shape(type="path", path="M 1.0,7.6 Q 5.0,8.2 9.0,7.6 Q 5.0,7.0 1.0,7.6 Z", fillcolor="rgba(200, 200, 200, 0.9)", line=dict(color="Gray", width=1.5))
fig.add_shape(type="path", path="M 1.0,7.6 Q 5.0,7.0 9.0,7.6 L 9.0,7.1 Q 5.0,6.5 1.0,7.1 Z", fillcolor="rgba(160, 160, 160, 1.0)", line=dict(color="Gray", width=1.5))

# --- STEP 3: ACCESSIBLE 2D CARGO BOX (Unfilled Bounding Box) ---
fig.add_shape(type="rect", x0=4.0, y0=7.6, x1=6.0, y1=9.3, fillcolor="rgba(0,0,0,0)", line=dict(color="#333333", width=2.5, dash="dash"))

# --- STEP 4: TEXT LABELS AND DYNAMIC SYMBOL ---
fig.add_trace(go.Scatter(x=[5.0], y=[8.45], mode="text", text=[f"<span style='font-size:36px;'>{active_emoji}</span>"], textposition="middle center"))
fig.add_trace(go.Scatter(x=[5.0], y=[9.7], mode="text", text=["<b>TARGET GOAL</b>"], textposition="top center"))
fig.add_trace(go.Scatter(x=[2.5], y=[4.0], mode="text", text=["PEOPLE<br>(Social)"], textposition="middle center"))
fig.add_trace(go.Scatter(x=[5.0], y=[4.0], mode="text", text=["PLANET<br>(Environmental)"], textposition="middle center"))
fig.add_trace(go.Scatter(x=[7.5], y=[4.0], mode="text", text=["PROFIT<br>(Economic)"], textposition="middle center"))

fig.update_layout(
    xaxis=dict(range=[0, 10], showgrid=False, zeroline=False, visible=False),
    yaxis=dict(range=[0, 11], showgrid=False, zeroline=False, visible=False),
    width=800, height=550, showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20), hovermode=False
)

# 6. Render the Clean Stool Graphic (Condensed and Centered)
left_spacer, center_col, right_spacer = st.columns([0.2, 0.6, 0.2])
with center_col:
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})

# 7. Dynamic Strategic Alignment Output
if selected_goal_key is not None:
    st.write(f"### 📋 Strategic Alignment Matrix Breakdown")
    
    # Pre-build bullet strings based on whether an industry is selected
    people_bullets = f"• {active_goal_info['people']}"
    planet_bullets = f"• {active_goal_info['planet']}"
    profit_bullets = f"• {active_goal_info['profit']}"
    
    if has_industry:
        people_bullets += f"<br><br>• <b>{selected_industry_key}:</b> {active_industry_info['people']}"
        planet_bullets += f"<br><br>• <b>{selected_industry_key}:</b> {active_industry_info['planet']}"
        profit_bullets += f"<br><br>• <b>{selected_industry_key}:</b> {active_industry_info['profit']}"

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div style="border: 2px solid orange; padding: 15px; border-radius: 8px; background-color: rgba(255, 165, 0, 0.05); min-height: 220px;">
                <h3 style="color: darkorange; margin-top: 0;">2.1. People Allocation</h3>
                <p style="font-size: 15px; color: #333333; line-height: 1.4;">{people_bullets}</p>
            </div>
            """, unsafe_allow_html=True)
            
    with col2:
        st.markdown(f"""
            <div style="border: 2px solid #3498db; padding: 15px; border-radius: 8px; background-color: rgba(52, 152, 219, 0.05); min-height: 220px;">
                <h3 style="color: #2980b9; margin-top: 0;">2.2. Planet Allocation</h3>
                <p style="font-size: 15px; color: #333333; line-height: 1.4;">{planet_bullets}</p>
            </div>
            """, unsafe_allow_html=True)
            
    with col3:
        st.markdown(f"""
            <div style="border: 2px solid #2ecc71; padding: 15px; border-radius: 8px; background-color: rgba(46, 204, 113, 0.05); min-height: 220px;">
                <h3 style="color: #27ae60; margin-top: 0;">2.3. Profit Allocation</h3>
                <p style="font-size: 15px; color: #333333; line-height: 1.4;">{profit_bullets}</p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("💡 Please select a business goal from the sidebar to view its Triple Bottom Line alignment details.")
