import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime
import os

# --- INTEGRATED ANALYTICAL ENGINE ---
class EnergyPulseEngine:
	@staticmethod
	def get_live_metrics():
		"""Simulates real-time telemetry from Kenyan power stations."""
		data = {
			"Source": ["Geothermal (Olkaria)", "Wind (Turkana)", "Hydro (Tana)", "Thermal (Msa)"],
			"Output_MW": [
				np.random.randint(790, 810), # Geothermal: Stable base load
				np.random.randint(150, 450), # Wind: High volatility
				np.random.randint(350, 500), # Hydro: Seasonal/Daily shift
				np.random.randint(80, 130)   # Thermal: Emergency backup
			],
			"Frequency_Hz": [np.random.uniform(49.8, 50.2) for _ in range(4)]
		}
		return pd.DataFrame(data)

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Kenya Energy Pulse", layout="wide")

# FLAGRANT ANIMATIONS & RESPONSIVE CSS
st.markdown("""
	<style>
	[data-testid="stSidebar"] .stMarkdown p { color: #ffffff !important; }
	@keyframes slideIn { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }
	@keyframes pulseGlow { 0% { box-shadow: 0 0 5px #ff4b4b; } 50% { box-shadow: 0 0 15px #ff4b4b; } 100% { box-shadow: 0 0 5px #ff4b4b; } }
	
	.stMetric, .stPlot, .stTable { animation: slideIn 0.5s ease-out both; }
	.live-indicator { 
		color: #ff4b4b; font-weight: bold; border: 1px solid #ff4b4b; 
		padding: 5px 15px; border-radius: 20px; animation: pulseGlow 2s infinite;
	}
	.main-card { background: #161b22; padding: 25px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 20px; }
	.github-link {
		background-color: #161b22; padding: 10px; border-radius: 5px; 
		border-left: 5px solid #ff4b4b; margin-bottom: 20px;
	}
	.footer { text-align: center; color: #888; margin-top: 50px; border-top: 1px solid #333; padding-top: 20px; }
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

# --- HEADER & PROJECT CONTEXT ---
st.title("⚡ Kenya Energy Grid & Fuel Pulse")

# --- GITHUB LINK ---
st.markdown(
	"""
	<div class="github-link">
		<b>📂 Source Code:</b> 
		<a href='https://github.com/GilbertAK/KenyaEnergyGridAndFuelPulse' target='_blank' style='color: #ff4b4b; text-decoration: none;'>
			View on GitHub Repository
		</a>
	</div>
	""", 
	unsafe_allow_html=True
)

st.markdown("""
<div class="main-card" style='background-color: #1b1b1b; padding: 20px; border-radius: 10px; border-left: 5px solid #ffcc00;'>
	<h3>Real-Time Data Science Infrastructure Monitor</h3>
	<p>This B2B-oriented dashboard monitors the <b>Kenyan National Power Grid</b> and correlates its stability 
	with <b>EPRA Fuel Price</b> fluctuations. In a country where energy costs directly impact industrial 
	productivity, this tool provides real-time telemetry simulation and price discovery.</p>
</div>
""", unsafe_allow_html=True)

# --- INTERACTIVE CONTROL PANEL ---
st.subheader("🛠️ Stream Control & Configuration")
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 1, 1])

with col_ctrl1:
	run_stream = st.toggle("🚀 Start Real-Time Stream", value=True, help="Toggle this to start/stop the live data ingestion simulation.")
with col_ctrl2:
	speeds = [round(x, 1) for x in np.arange(0.2, 2.2, 0.2)]
	refresh_speed = st.select_slider("Refresh Rate (Seconds)", options=speeds, value=0.4, help="Adjust how often the system polls the generation units.")
with col_ctrl3:
	st.markdown(f"<br><span class='live-indicator'>{'● LIVE MONITORING ACTIVE' if run_stream else '○ STREAM PAUSED'}</span>", unsafe_allow_html=True)

# --- DYNAMIC DATA HOOKS ---
metric_container = st.empty()
graph_container = st.empty()
table_container = st.empty()

if 'old_df' not in st.session_state:
    st.session_state.old_df = None

# --- THE EXECUTION LOOP ---
while run_stream:
	# 1. Fetch Fresh Data
	df = EnergyPulseEngine.get_live_metrics()
	total_mw = df['Output_MW'].sum()
	fuel_price = 196.50 + np.random.uniform(-0.15, 0.15)
	
	# 2. UPDATE METRICS
	with metric_container.container():
		st.info("**Key Performance Indicators:** Monitoring the national energy demand vs current EPRA fuel benchmarks.")
		m1, m2, m3, m4 = st.columns(4)
		m1.metric("National Load", f"{total_mw} MW", delta=f"{np.random.randint(-5, 6)} MW", help="The current total electricity consumption in Kenya.")
		m2.metric("Nairobi Petrol", f"KSh {fuel_price:.2f}", delta=f"{fuel_price-196.50:.3f}", help="Live estimation based on EPRA monthly price ceilings.")
		m3.metric("Grid Frequency", f"{df['Frequency_Hz'].mean():.2f} Hz", help="Standard is 50Hz. Deviations can cause industrial machinery failure.")
		m4.metric("Green Energy %", f"{(df.iloc[:3]['Output_MW'].sum()/total_mw)*100:.1f}%", help="Combined contribution from Geothermal, Wind, and Hydro-power.")

	# 3. UPDATE VISUALS
	with graph_container.container():
		left_col, right_col = st.columns([2, 1])
		
		with left_col:
			st.subheader("📊 Dynamic Generation Mix")
			st.write("Visualizing the output of Kenya's primary power plants to track source reliability.")
			fig, ax = plt.subplots(figsize=(10, 4.5))
			plt.style.use('dark_background')
			colors = ['#00ff00', '#ffffff', '#00d4ff', '#ff4b4b']
			ax.bar(df['Source'], df['Output_MW'], color=colors, edgecolor='white', alpha=0.8)
			ax.set_ylabel("Megawatts (MW)")
			ax.grid(axis='y', alpha=0.2)
			st.pyplot(fig)
			st.caption("**Insight:** Real-time fluctuations reflect Turkana's wind gusts and Tana's hydro-flow adjustments.")

		with right_col:
			st.subheader("⚖️ Load Distribution")
			st.write("Breakdown of energy contribution by source types.")
			fig2, ax2 = plt.subplots()
			ax2.pie(df['Output_MW'], labels=df['Source'], autopct='%1.1f%%', colors=colors, startangle=140, textprops={'color':"w"})
			st.pyplot(fig2)
			st.caption("**Insight:** Geothermal remains the backbone of the Kenyan grid.")

	# 4. UPDATE TABLE WITH CONDITIONAL COLORING
	with table_container.container():
		st.subheader("📋 Detailed Generation Logs")
		st.write("**Simulated SCADA Feed:** Tracking micro-fluctuations in generation and frequency for industrial audits.")
		
		def style_comparison(new_data):
			style_df = pd.DataFrame('', index=new_data.index, columns=new_data.columns)
			if st.session_state.old_df is not None:
				for col in ['Output_MW', 'Frequency_Hz']:
					for idx in new_data.index:
						new_val = new_data.loc[idx, col]
						old_val = st.session_state.old_df.loc[idx, col]
						if new_val > old_val:
							style_df.loc[idx, col] = 'background-color: rgba(0, 255, 0, 0.2)'
						elif new_val < old_val:
							style_df.loc[idx, col] = 'background-color: rgba(255, 0, 0, 0.2)'
						else:
							style_df.loc[idx, col] = 'background-color: rgba(128, 128, 128, 0.2)'
			return style_df

		st.dataframe(df.style.apply(style_comparison, axis=None), use_container_width=True, hide_index=True)
		st.session_state.old_df = df.copy()

	time.sleep(refresh_speed)
	if not run_stream:
		break

# --- STOPPED STATE ---
if not run_stream:
	st.warning("Data stream is currently paused. Please toggle 'Start Real-Time Stream' to resume monitoring.")

# --- NAVIGATION & FOOTER ---
st.write("---")
if st.button("⬅️ Return to Portfolio Hub", key="bottom_back"):
	st.switch_page("app.py")

st.markdown(f"""
<div class="footer">
	Kenya Energy Monitor v1.5 | Infrastructure SCADA | Developed by Gilbert ASANI KAMARA (2026)
</div>
""", unsafe_allow_html=True)
