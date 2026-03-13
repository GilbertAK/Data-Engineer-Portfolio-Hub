# %%writefile pages/6_NSE_AI_Predictive_Ticker.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import time
from collections import deque
import os

# --- ASSET CONFIGURATION ---
STOCKS = {
	"SCOM": {"name": "Safaricom PLC", "base_price": 17.50, "volatility": 0.25},
	"EQTY": {"name": "Equity Group", "base_price": 42.10, "volatility": 0.45},
	"KCB":  {"name": "KCB Group", "base_price": 29.35, "volatility": 0.35},
	"EABL": {"name": "East African Breweries", "base_price": 150.00, "volatility": 0.85},
	"ABSA": {"name": "ABSA Bank Kenya", "base_price": 12.80, "volatility": 0.15}
}

# --- ML & SIMULATION ENGINE ---
class NSEStockEngine:
	def __init__(self):
		self.model = LinearRegression()
		if 'market_history' not in st.session_state:
			st.session_state.market_history = {
				symbol: deque([info['base_price']] * 20, maxlen=20) 
				for symbol, info in STOCKS.items()
			}

	def update_and_predict(self, symbol):
		history = st.session_state.market_history[symbol]
		current_price = history[-1]
		change = np.random.normal(0, STOCKS[symbol]['volatility'])
		new_price = max(0.01, round(current_price + change, 2))
		history.append(new_price)
		X = np.array(range(len(history))).reshape(-1, 1)
		y = np.array(history)
		self.model.fit(X, y)
		prediction = self.model.predict([[len(history)]])[0]
		return new_price, prediction, list(history)

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="NSE AI Ticker", layout="wide")

# --- CUSTOM CSS FOR UNIFORMITY & OPTIMIZATION ---
st.markdown("""
	<style>
	[data-testid="stSidebar"] .stMarkdown p { color: #ffffff !important; }
	.ai-card { background: #1b1b1b; padding: 20px; border-radius: 10px; border-left: 5px solid #00ff00; margin-bottom: 20px; }
	.metric-box { background: #161b22; border: 1px solid #30363d; padding: 8px; border-radius: 8px; text-align: center; }
	.metric-label { color: #8b949e; font-size: 12px; font-weight: bold; }
	.metric-value { color: #ffffff; font-size: 18px; font-weight: bold; }
	.github-link {
		background-color: #161b22; padding: 10px; border-radius: 5px; 
		border-left: 5px solid #ff4b4b; margin-bottom: 20px;
	}
	.footer { text-align: center; color: #888; margin-top: 50px; border-top: 1px solid #333; padding-top: 20px; }
	@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
	.live-dot { color: #00ff00; animation: pulse 1s infinite; font-weight: bold; }
	.desc-text { color: #8b949e; font-size: 14px; margin-bottom: 15px; line-height: 1.4; }
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
st.title("📈 NSE AI Predictive Ticker")

# --- GITHUB LINK ---
st.markdown(
	"""
	<div class="github-link">
		<b>📂 Source Code:</b> 
		<a href='https://github.com/GilbertAK/NairobiSecuritiesExchange' target='_blank' style='color: #ff4b4b; text-decoration: none;'>
			View on GitHub Repository
		</a>
	</div>
	""", 
	unsafe_allow_html=True
)

st.markdown("""
<div class="ai-card">
	<h3>Nairobi Securities Exchange - Real-Time AI Forecasting</h3>
	<p>This simulation platform leverages <b>Machine Learning</b> algorithms to analyze the market microstructure of Kenya's stock exchange. 
	By training a linear regression model on a high-frequency data stream, we identify emerging trends 
	for the country's largest blue-chip capitalizations.</p>
</div>
""", unsafe_allow_html=True)

# --- CONTROL PANEL ---
col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
with col_c1:
	run_trading = st.toggle("🚀 Start AI Trading Session", value=True)
with col_c2:
	refresh_speed = st.select_slider("Polling Rate (Seconds)", options=[0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0], value=0.4)
with col_c3:
	st.markdown(f"<br><span class='live-dot'>{'● LIVE MARKET DATA' if run_trading else '○ MARKET CLOSED'}</span>", unsafe_allow_html=True)

ticker_placeholder = st.empty()
chart_placeholder = st.empty()
log_placeholder = st.empty()

engine = NSEStockEngine()

# --- THE EXECUTION LOOP ---
while run_trading:
	market_data = []
	for symbol in STOCKS.keys():
		new_p, pred_p, hist = engine.update_and_predict(symbol)
		raw_change = ((new_p - STOCKS[symbol]['base_price']) / STOCKS[symbol]['base_price']) * 100
		market_data.append({"Symbol": symbol, "Price": new_p, "Change_PC": raw_change, "AI Forecast (T+1)": round(pred_p, 2), "Trend": "▲ UP" if pred_p > new_p else "▼ DOWN", "History": hist})

	with ticker_placeholder.container():
		st.markdown("<p class='desc-text'><b>Key Performance Indicators:</b> Comparative analysis of current market cap versus base prices. The delta reflects the simulated intra-day volatility for each NSE-listed asset, allowing for real-time spread monitoring.</p>", unsafe_allow_html=True)
		cols = st.columns(len(market_data))
		for i, data in enumerate(market_data):
			color = "#3fb950" if data['Change_PC'] >= 0 else "#f85149"
			cols[i].markdown(f"""
				<div class="metric-box">
					<div class="metric-label">{data['Symbol']}</div>
					<div class="metric-value">{data['Price']:.2f}</div>
					<div style="color: {color}; font-size: 12px;">{'+' if data['Change_PC'] >= 0 else ''}{data['Change_PC']:.2f}%</div>
				</div>
			""", unsafe_allow_html=True)

	with chart_placeholder.container():
		st.subheader("📊 AI Forecast Visualization")
		st.markdown("<p class='desc-text'>These charts illustrate price trajectories over the last 20 ticks. The red dashed line is generated by <b>Scikit-Learn</b>; it represents the mathematical prediction of the next movement based on current momentum slopes.</p>", unsafe_allow_html=True)
		c1, c2 = st.columns(2)
		for i, stock_idx in enumerate([0, 1]):
			data = market_data[stock_idx]
			fig, ax = plt.subplots(figsize=(8, 3.5)); plt.style.use('dark_background')
			y = data['History']; x = np.arange(len(y))
			ax.plot(x, y, label="Actual", color="#00ff00", linewidth=2.5)
			model = LinearRegression().fit(x.reshape(-1,1), np.array(y))
			trend_line = model.predict(np.append(x, [len(y)]).reshape(-1,1))
			ax.plot(np.append(x, [len(y)]), trend_line, '--', color="#ff4b4b", label="AI Prediction")
			ax.set_title(f"Momentum: {data['Symbol']}"); ax.legend(prop={'size': 8})
			[c1, c2][i].pyplot(fig)

	with log_placeholder.container():
		st.subheader("📋 Predictive Analytics Table")
		st.markdown("<p class='desc-text'>This summary table consolidates raw data and trend forecasts. It allows analysts to quickly verify market direction (Trend) calculated by the regression algorithm across the entire portfolio for high-level decision making.</p>", unsafe_allow_html=True)
		df_display = pd.DataFrame(market_data).drop(columns=['History', 'Change_PC'])
		def highlight_forecast(row):
			color = 'rgba(0, 255, 0, 0.15)' if 'UP' in str(row['Trend']) else 'rgba(255, 0, 0, 0.15)'
			return ['background-color: ' + color if name in ['AI Forecast (T+1)', 'Trend'] else '' for name in row.index]
		st.dataframe(df_display.style.apply(highlight_forecast, axis=1), use_container_width=True, hide_index=True)

	time.sleep(refresh_speed)
	if not run_trading: break

# --- NAVIGATION & FOOTER ---
st.write("---")
if st.button("⬅️ Return to Portfolio Hub", key="bottom_back"):
	st.switch_page("app.py")

st.markdown("""
<div class="footer">
	NSE AI Ticker v2.0 | Fintech Intelligence | Developed by Gilbert ASANI KAMARA (2026)
</div>
""", unsafe_allow_html=True)