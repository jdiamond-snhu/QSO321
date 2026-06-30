import streamlit as st
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events

# 1. Page Configuration
st.set_page_config(page_title="TBL Stool Matrix", layout="wide")
st.title("🪑 Triple Bottom Line Matrix Mapper")
st.write("Select a goal from the sidebar to automatically load its strategic TBL configuration, then click on the map to place markers.")

# 2. Define the Static Mapping Data Structure
# Each goal contains its display label, its core symbol, and its hardcoded TBL alignments.
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

# 3. State Management Initialization
if "placed_goals" not in st.session_state:
    st.session_state.placed_goals = []  # Stores manual user clicks: {'goal': str, 'x': float, 'y': float, 'component': str}

# 4. Sidebar Goal Selection
st.sidebar.header("1. Choose a Business Goal")
selected_goal_key = st.sidebar.radio("", list(STRATEGIC_GOALS_DATA.keys()))

# Extract data for the actively selected goal
active_goal_info = STRATEGIC_GOALS_DATA[selected_goal_key]
active_emoji = active_goal_info["symbol"]

if st.sidebar.button("Reset Placed Markers"):
    st.session_state.placed_goals = []
    st.rerun()

# 5. Building the 3-Legged Stool Figure
fig = go.Figure()

# --- STEP 1: THE THREE STOOL LEGS (Drawn First / Sent to Back) ---
fig.add_shape(
    type="path",
    path="M 1.5,7.1 L 1.5,1.3 Q 2.5,0.7 3.5,1.3 L 3.5,7.1 Z",
    fillcolor="rgba(255, 165, 0, 0.4)", 
    line=dict(color="Orange", width=2)
)
fig.add_shape(
    type="path",
    path="M 4.0,7.1 L 4.0,1.3 Q 5.0,0.7 6.0,1.3 L 6.0,7.1 Z",
    fillcolor="rgba(52, 152, 219, 0.4)", 
    line=dict(color="SkyBlue", width=2)
)
fig.add_shape(
    type="path",
    path="M 6.5,7.1 L 6.5,1.3 Q 7.5,0.7 8.5,1.3 L 8.5,7.1 Z",
    fillcolor="rgba(46, 204, 113, 0.4)", 
    line=dict(color="LightGreen", width=2)
)

# --- STEP 2: 3D OVAL SEAT ASSEMBLY ---
fig.add_shape(
    type="path",
    path="M 1.0,7.6 Q 5.0,8.2 9.0,7.6 Q 5.0,7.0 1.0,7.6 Z",
    fillcolor="rgba(200, 200, 200, 0.9)",
    line=dict(color="Gray", width=1.5)
)
fig.add_shape(
    type="path",
    path="M 1.0,7.6 Q 5.0,7.0 9.0,7.6 L 9.0,7.1 Q 5.0,6.5 1.0,7.1 Z",
    fillcolor="rgba(160, 160, 160, 1.0)",
    line=dict(color="Gray", width=1.5)
)

# --- STEP 3: ACCESSIBLE 2D CARGO BOX (Unfilled Bounding Box) ---
fig.add_shape(
    type="rect",
    x0=4.0, y0=7.6, x1=6.0, y1=9.3,
    fillcolor="rgba(0,0,0,0)",
    line=dict(color="#333333", width=2.5, dash="dash")
)

# --- STEP 4: TEXT LABELS AND DYNAMIC SYMBOL ---
fig.add_trace(go.Scatter(
    x=[5.0], y=[8.45], 
    mode="text", 
    text=[f"<span style='font-size:36px;'>{active_emoji}</span>"], 
    textposition="middle center"
))

# Labels for the Legs & Seat
fig.add_trace(go.Scatter(x=[5.0], y=[9.7], mode="text", text=["<b>SUSTAINABILITY LOAD</b>"], textposition="top center"))
fig.add_trace(go.Scatter(x=[2.5], y=[4.0], mode="text", text=["PEOPLE<br>(Social)"], textposition="middle center"))
fig.add_trace(go.Scatter(x=[5.0], y=[4.0], mode="text", text=["PLANET<br>(Environmental)"], textposition="middle center"))
fig.add_trace(go.Scatter(x=[7.5], y=[4.0], mode="text", text=["PROFIT<br>(Economic)"], textposition="middle center"))

# Plot user-clicked custom markers onto the chart if they want to physically pin them
if st.session_state.placed_goals:
    goals_x = [item['x'] for item in st.session_state.placed_goals]
    goals_y = [item['y'] for item in st.session_state.placed_goals]
    goals_text = [f"{item['goal']}" for item in st.session_state.placed_goals]
    
    fig.add_trace(go.Scatter(
        x=goals_x, y=goals_y,
        mode="markers",
        marker=dict(size=14, color="#E74C3C", symbol="circle"),
        name="User Pins"
    ))

# Graph Grid and Interactivity Settings
fig.update_layout(
    xaxis=dict(range=[0, 10], showgrid=False, zeroline=False, visible=False),
    yaxis=dict(range=[0, 11], showgrid=False, zeroline=False, visible=False),
    width=800, height=550,
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20),
    clickmode="event+select"
)

# 6. Optional: Capture Click Events (Preserving mapping mechanics)
click_data = plotly_events(fig, click_event=True, hover_event=False, override_height=550, override_width="100%")

if click_data:
    click_point = click_data[0]
    cx = click_point["x"]
    cy = click_point["y"]
    
    component = "Outside Stool Boundaries"
    if 6.5 <= cy <= 9.5 and 1.0 <= cx <= 9.0:
        component = "Seat"
    elif 0.7 <= cy < 6.5:
        if 1.5 <= cx <= 3.5:
            component = "People"
        elif 4.0 <= cx <= 6.0:
            component = "Planet"
        elif 6.5 <= cx <= 8.5:
            component = "Profit"
            
    if component != "Outside Stool Boundaries":
        st.session_state.placed_goals.append({"goal": active_emoji, "x": cx, "y": cy})
        st.toast(f"Pinned marker to {component}!", icon="📍")
        st.rerun()

# 7. Dynamic Strategic Alignment Output
st.write(f"### 📋 Triple Bottom Line Alignment: {selected_goal_key}")

# Render high-contrast containers using standard Streamlit columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style="border: 2px solid orange; padding: 15px; border-radius: 8px; background-color: rgba(255, 165, 0, 0.05); min-height: 150px;">
            <h3 style="color: darkorange; margin-top: 0;">🟠 People Allocation</h3>
            <p style="font-size: 16px; color: #333333;">{active_goal_info["people"]}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
with col2:
    st.markdown(
        f"""
        <div style="border: 2px solid #3498db; padding: 15px; border-radius: 8px; background-color: rgba(52, 152, 219, 0.05); min-height: 150px;">
            <h3 style="color: #2980b9; margin-top: 0;">🔵 Planet Allocation</h3>
            <p style="font-size: 16px; color: #333333;">{active_goal_info["planet"]}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
with col3:
    st.markdown(
        f"""
        <div style="border: 2px solid #2ecc71; padding: 15px; border-radius: 8px; background-color: rgba(46, 204, 113, 0.05); min-height: 150px;">
            <h3 style="color: #27ae60; margin-top: 0;">🟢 Profit Allocation</h3>
            <p style="font-size: 16px; color: #333333;">{active_goal_info["profit"]}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
