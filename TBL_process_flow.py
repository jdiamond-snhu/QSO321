import streamlit as st
import plotly.graph_objects as iplots
from streamlit_plotly_events import plotly_events

# 1. Page Configuration
st.set_page_config(page_title="Business Goal Matrix", layout="wide")
st.title("🎯 Business Goal Matrix Mapper")
st.write("Select a goal from the sidebar, then click on the circular matrix to place it.")

# 2. State Management Initialization
if "placed_goals" not in st.session_state:
    st.session_state.placed_goals = []  # Stores dicts: {'goal': str, 'r': float, 'theta': float}

# 3. Sidebar Goal Selection
st.sidebar.header("1. Choose a Business Goal")
static_goals = [
    "🚀 Scale Revenue",
    "👥 Improve Retention",
    "🛠️ Reduce Technical Debt",
    "🌍 Expand Market Share",
    "⚡ Optimize Operations"
]
selected_goal = st.sidebar.radio("Active Goal:", static_goals)

# Clear button to reset the matrix
if st.sidebar.button("Reset Matrix"):
    st.session_state.placed_goals = []
    st.rerun()

# 4. Building the Circular Matrix Visuals
fig = iplots.Figure()

# Background layout: Add concentric circles to define the matrix zones
radii = [0.3, 0.6, 0.9, 1.0]
zone_colors = ["rgba(46, 204, 113, 0.1)", "rgba(52, 152, 219, 0.1)", "rgba(155, 89, 182, 0.1)", "rgba(230, 126, 34, 0.1)"]

for r, color in zip(radii, zone_colors):
    fig.add_trace(iplots.Scatterpolar(
        r=[0, r, r, 0],
        theta=[0, 0, 360, 0],
        fill="toself",
        fillcolor=color,
        line=dict(color="rgba(255,255,255,0.3)", width=1),
        mode="lines",
        showlegend=False,
        hoverinfo="skip"
    ))

# Plot already placed goals onto the chart
if st.session_state.placed_goals:
    goals_r = [item['r'] for item in st.session_state.placed_goals]
    goals_theta = [item['theta'] for item in st.session_state.placed_goals]
    goals_text = [item['goal'] for item in st.session_state.placed_goals]
    
    fig.add_trace(iplots.Scatterpolar(
        r=goals_r,
        theta=goals_theta,
        mode="markers+text",
        text=goals_text,
        textposition="top center",
        marker=dict(size=14, color="#E74C3C", symbol="triangle-up"),
        name="Placed Goals"
    ))

# Polar Chart Formatting
fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 1], tickvals=[0.3, 0.6, 0.9]),
        angularaxis=dict(visible=True, direction="counterclockwise", period=360)
    ),
    width=700,
    height=700,
    showlegend=False,
    margin=dict(l=40, r=40, t=40, b=40)
)

# 5. Capture Click Events and Update State
st.subheader("2. Click on the Matrix to Place Goal")
click_data = plotly_events(fig, click_event=True, hover_event=False, override_height=700, override_width="100%")

# If the user clicks the map, save the goal coordinates and refresh
if click_data:
    click_point = click_data[0]
    
    # Simple check to filter out clicks on existing markers
    if click_point.get('curveNumber') == 0 or click_point.get('curveNumber') is not None:
        new_placement = {
            "goal": selected_goal,
            "r": click_point["r"],
            "theta": click_point["theta"]
        }
        
        # Append to our session state list
        st.session_state.placed_goals.append(new_placement)
        st.toast(f"Placed: {selected_goal}!", icon="🎯")
        st.rerun()

# 6. Dynamic Text Output Breakdown
if st.session_state.placed_goals:
    st.write("### Matrix Composition Breakdown")
    for idx, item in enumerate(st.session_state.placed_goals):
        st.write(f"**Goal {idx+1}:** {item['goal']} (Distance from center: `{item['r']:.2f}`, Angle: `{item['theta']:.1f}°`)")
