import streamlit as st
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events

# 1. Page Configuration
st.set_page_config(page_title="TBL Stool Matrix", layout="wide")
st.title("🪑 Triple Bottom Line Matrix Mapper")
st.write("Select a goal, then click directly on a specific leg or seat of the stool to place it.")

# 2. State Management Initialization
if "placed_goals" not in st.session_state:
    st.session_state.placed_goals = []  # Stores: {'goal': str, 'x': float, 'y': float, 'component': str}

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

if st.sidebar.button("Reset Matrix"):
    st.session_state.placed_goals = []
    st.rerun()

# 4. Building the 3-Legged Stool Figure
fig = go.Figure()

# --- 3D OVAL SEAT ASSEMBLY ---
# A. Top of the seat: A flat horizontal oval surface
fig.add_shape(
    type="path",
    path="M 1.0,7.6 Q 5.0,8.2 9.0,7.6 Q 5.0,7.0 1.0,7.6 Z",
    fillcolor="rgba(200, 200, 200, 0.9)",
    line=dict(color="Gray", width=1.5)
)

# B. Front rim of the seat: Gives the seat its 3D depth/thickness
fig.add_shape(
    type="path",
    path="M 1.0,7.6 Q 5.0,7.0 9.0,7.6 L 9.0,7.1 Q 5.0,6.5 1.0,7.1 Z",
    fillcolor="rgba(160, 160, 160, 1.0)",
    line=dict(color="Gray", width=1.5)
)

# --- THE THREE STOOL LEGS (With Rounded Bottoms) ---
# 1. People Leg (Light Orange)
fig.add_shape(
    type="path",
    path="M 1.5,7.1 L 1.5,1.3 Q 2.5,0.7 3.5,1.3 L 3.5,7.1 Z",
    fillcolor="rgba(255, 165, 0, 0.4)", 
    line=dict(color="Orange", width=2)
)

# 2. Planet Leg (Light Blue)
fig.add_shape(
    type="path",
    path="M 4.0,7.1 L 4.0,1.3 Q 5.0,0.7 6.0,1.3 L 6.0,7.1 Z",
    fillcolor="rgba(52, 152, 219, 0.4)", 
    line=dict(color="SkyBlue", width=2)
)

# 3. Profit Leg (Light Green)
fig.add_shape(
    type="path",
    path="M 6.5,7.1 L 6.5,1.3 Q 7.5,0.7 8.5,1.3 L 8.5,7.1 Z",
    fillcolor="rgba(46, 204, 113, 0.4)", 
    line=dict(color="LightGreen", width=2)
)

# Text Labels for the Legs & Seat
fig.add_trace(go.Scatter(x=[5.0], y=[7.5], mode="text", text=["SUSTAINABILITY SEAT"], textposition="top center"))
fig.add_trace(go.Scatter(x=[2.5], y=[4.0], mode="text", text=["PEOPLE<br>(Social)"], textposition="middle center"))
fig.add_trace(go.Scatter(x=[5.0], y=[4.0], mode="text", text=["PLANET<br>(Environmental)"], textposition="middle center"))
fig.add_trace(go.Scatter(x=[7.5], y=[4.0], mode="text", text=["PROFIT<br>(Economic)"], textposition="middle center"))

# Plot already placed goals onto the chart
if st.session_state.placed_goals:
    goals_x = [item['x'] for item in st.session_state.placed_goals]
    goals_y = [item['y'] for item in st.session_state.placed_goals]
    goals_text = [f"{item['goal']}<br>({item['component']})" for item in st.session_state.placed_goals]
    
    fig.add_trace(go.Scatter(
        x=goals_x, y=goals_y,
        mode="markers+text",
        text=goals_text,
        textposition="bottom center",
        marker=dict(size=14, color="#E74C3C", symbol="circle"),
        name="Placed Goals"
    ))

# Graph Grid and Interactivity Settings
fig.update_layout(
    xaxis=dict(range=[0, 10], showgrid=False, zeroline=False, visible=False),
    yaxis=dict(range=[0, 10], showgrid=False, zeroline=False, visible=False),
    width=800, height=550,
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20),
    clickmode="event+select"
)

# 5. Capture Click Events and Determine Location
st.subheader("2. Interactive TBL Map")
click_data = plotly_events(fig, click_event=True, hover_event=False, override_height=550, override_width="100%")

if click_data:
    click_point = click_data[0]
    cx = click_point["x"]
    cy = click_point["y"]
    
    # Check what part of the stool was clicked based on revised boundaries
    component = "Outside Stool Boundaries"
    
    if 6.5 <= cy <= 8.2 and 1.0 <= cx <= 9.0:
        component = "Seat (Balance Area)"
    elif 0.7 <= cy < 6.5:
        if 1.5 <= cx <= 3.5:
            component = "People Leg (Social)"
        elif 4.0 <= cx <= 6.0:
            component = "Planet Leg (Environmental)"
        elif 6.5 <= cx <= 8.5:
            component = "Profit Leg (Economic)"
            
    # Save target placement if it falls inside a leg or seat
    if component != "Outside Stool Boundaries":
        new_placement = {
            "goal": selected_goal,
            "x": cx,
            "y": cy,
            "component": component
        }
        st.session_state.placed_goals.append(new_placement)
        st.toast(f"Assigned to {component}!", icon="🎯")
        st.rerun()
    else:
        st.warning("Click directly on one of the stool components to register the goal alignment.")

# 6. Dynamic Text Output Breakdown
if st.session_state.placed_goals:
    st.write("### Current Strategic Alignment")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🟠 People Allocations")
        for item in st.session_state.placed_goals:
            if "People" in item['component']:
                st.write(f"* {item['goal']}")
                
    with col2:
        st.subheader("🔵 Planet Allocations")
        for item in st.session_state.placed_goals:
            if "Planet" in item['component']:
                st.write(f"* {item['goal']}")
                
    with col3:
        st.subheader("🟢 Profit Allocations")
        for item in st.session_state.placed_goals:
            if "Profit" in item['component']:
                st.write(f"* {item['goal']}")
