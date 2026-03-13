import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import os

# --- MOTEUR DE SIMULATION ---
class MatatuEngine:
	def __init__(self):
		self.routes = {
			"Thika Road": {"lat": -1.221, "lon": 36.885, "speed_limit": 50},
			"Ngong Road": {"lat": -1.300, "lon": 36.780, "speed_limit": 40},
			"Jogoo Road": {"lat": -1.290, "lon": 36.850, "speed_limit": 35},
			"Waiyaki Way": {"lat": -1.260, "lon": 36.760, "speed_limit": 60},
			"Mombasa Road": {"lat": -1.330, "lon": 36.900, "speed_limit": 55}
		}
		self.fleet_size = 20 # Augmenté pour une meilleure densité visuelle
		self.fleet = self._initialize_fleet()

	def _initialize_fleet(self):
		fleet_data = []
		for i in range(self.fleet_size):
			route_name = np.random.choice(list(self.routes.keys()))
			fleet_data.append({
				"id": f"K{np.random.choice(['BA','BZ','CQ'])}{np.random.randint(100,999)}X",
				"route": route_name,
				"lat": self.routes[route_name]["lat"] + np.random.uniform(-0.015, 0.015),
				"lon": self.routes[route_name]["lon"] + np.random.uniform(-0.015, 0.015),
				"speed": np.random.randint(10, 60),
				"prev_speed": 0
			})
		return pd.DataFrame(fleet_data)

	def update_telemetry(self):
		for idx, row in self.fleet.iterrows():
			self.fleet.at[idx, 'prev_speed'] = row['speed']
			self.fleet.at[idx, 'lat'] += np.random.uniform(-0.002, 0.002)
			self.fleet.at[idx, 'lon'] += np.random.uniform(-0.002, 0.002)
			limit = self.routes[row['route']]["speed_limit"]
			self.fleet.at[idx, 'speed'] = max(5, min(limit + 10, row['speed'] + np.random.randint(-8, 8)))
		return self.fleet

	def get_heat_metrics(self):
		metrics = []
		for route in self.routes.keys():
			route_fleet = self.fleet[self.fleet['route'] == route]
			avg_speed = route_fleet['speed'].mean()
			density = len(route_fleet)
			score = (density * 20) / (max(1, avg_speed) / 5)
			status = "HEAVY" if score > 15 else "MODERATE" if score > 8 else "CLEAR"
			metrics.append({"Route": route, "Active Matatus": density, "Avg Speed": f"{avg_speed:.1f} km/h", "Status": status})
		return metrics

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Nairobi Matatu Heatmap", layout="wide")

# --- CUSTOM CSS FOR UNIFORMITY ---
st.markdown("""
	<style>
	[data-testid="stSidebar"] .stMarkdown p { color: #ffffff !important; }
	.stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 10px; border-radius: 10px; }
	.info-card { background: #1b1b1b; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 20px; }
	.github-link {
		background-color: #161b22; padding: 10px; border-radius: 5px; 
		border-left: 5px solid #ff4b4b; margin-bottom: 20px;
	}
	.footer { text-align: center; color: #888; margin-top: 50px; border-top: 1px solid #333; padding-top: 20px; }
	.desc-text { color: #8b949e; font-size: 14px; line-height: 1.5; margin-bottom: 20px; }
	</style>
	""", unsafe_allow_html=True)

# --- SIDEBAR (Standardized Identity) ---
with st.sidebar:
	if os.path.exists("assets/profile.jpg"):
		st.image("assets/profile.jpg", use_container_width=True)
	st.markdown("### **Gilbert ASANI KAMARA**")
	st.markdown("Full-Stack Data Engineer")
	st.markdown("---")
	if st.button("⬅️ Back to Portfolio Hub", key="side_back"):
		st.switch_page("app.py")
	st.markdown("---")
	st.write("💬 WhatsApp: [+243 893 958 170]")
	st.write("📧 gilbertakg@gmail.com")

# --- HEADER ---
st.title("🚐 Nairobi Matatu Traffic Heatmap")

# --- GITHUB LINK ---
st.markdown(
	"""
	<div class="github-link">
		<b>📂 Source Code:</b> 
		<a href='https://github.com/GilbertAK/MatatuTrafficHeatmapAndRouteOptimization' target='_blank' style='color: #ff4b4b; text-decoration: none;'>
			View on GitHub Repository
		</a>
	</div>
	""", 
	unsafe_allow_html=True
)

st.markdown("""
<div class="info-card">
	<h3>Real-Time Urban Mobility Analytics (Plotly Engine)</h3>
	<p>Using <b>Plotly Density Contours</b> for high-performance geospatial rendering. This version is optimized for low-bandwidth environments while maintaining precise traffic bottleneck detection.</p>
</div>
""", unsafe_allow_html=True)

if 'heatmap_engine' not in st.session_state:
	st.session_state.heatmap_engine = MatatuEngine()

# --- CONTROLS ---
col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
with col_c1:
	run_sim = st.toggle("📡 Activate Live GPS Stream", value=True)
with col_c2:
	refresh_speed = st.select_slider("GPS Polling Interval (Seconds)", options=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0], value=4.0)
with col_c3:
	st.markdown(f"<br><b style='color:white'>Status: {'🔴 LIVE' if run_sim else '⚪ STANDBY'}</b>", unsafe_allow_html=True)

col_left, col_right = st.columns([2, 1])
map_placeholder = col_left.empty()
metrics_placeholder = col_right.empty()
table_placeholder = st.empty()

# --- MAIN LOOP ---
while run_sim:
	fleet = st.session_state.heatmap_engine.update_telemetry()
	metrics = st.session_state.heatmap_engine.get_heat_metrics()
	
	with map_placeholder.container():
		st.subheader("📍 Geospatial Density Analysis")
		st.markdown("<p class='desc-text'>Plotly Heatmap: Areas with dense clusters of GPS pings appear in yellow/red, highlighting congestion centers across Nairobi.</p>", unsafe_allow_html=True)
		
		fig = px.density_mapbox(
			fleet, lat='lat', lon='lon', z='speed', radius=30,
			center=dict(lat=-1.286389, lon=36.817223), zoom=11,
			mapbox_style="carto-darkmatter",
			color_continuous_scale="Viridis",
			height=500
		)
		fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="#0e1117")
		st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

	with metrics_placeholder.container():
		st.subheader("📈 Route Efficiency")
		for m_data in metrics[:5]:
			st.metric(
				label=f"Route: {m_data['Route']}", 
				value=m_data['Avg Speed'], 
				delta=m_data['Status'], 
				delta_color="inverse" if m_data['Status'] == "HEAVY" else "normal"
			)

	with table_placeholder.container():
		st.markdown("---")
		st.subheader("📋 Fleet Telemetry Log")
		st.markdown("<p class='desc-text'>Live GPS stream data. Speed column highlights: Green (Accelerating), Red (Decelerating), Gray (Stable).</p>", unsafe_allow_html=True)
		
		def style_speed(row):
			if row['speed'] > row['prev_speed']:
				color = 'rgba(0, 255, 0, 0.2)'
			elif row['speed'] < row['prev_speed']:
				color = 'rgba(255, 0, 0, 0.2)'
			else:
				color = 'rgba(128, 128, 128, 0.1)'
			return ['' , '', f'background-color: {color}', '']

		df_display = fleet[['id', 'route', 'speed', 'prev_speed']]
		st.dataframe(
			df_display.style.apply(style_speed, axis=1),
			use_container_width=True, 
			hide_index=True,
			column_order=("id", "route", "speed")
		)

	time.sleep(refresh_speed)
	if not run_sim: break

# --- NAVIGATION & FOOTER ---
st.write("---")
if st.button("⬅️ Return to Portfolio Hub", key="bottom_back"):
	st.switch_page("app.py")

st.markdown(f"""
<div class="footer">
	Nairobi Mobility Heatmap v1.0 | Urban Logistics | Developed by Gilbert ASANI KAMARA (2026)
</div>
""", unsafe_allow_html=True)