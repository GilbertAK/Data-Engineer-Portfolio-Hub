import streamlit as st
import os
from PIL import Image

# 1. GLOBAL SETTINGS (Force Dark Mode via config is best, but we set layout here)
st.set_page_config(
	page_title="Gilbert | Full-Stack Data Engineer",
	page_icon="💻",
	layout="wide",
	initial_sidebar_state="expanded"
)

# 2. PROFESSIONAL SIDEBAR (IDENTITY & CONTACT)
with st.sidebar:
	# High-quality profile picture
	if os.path.exists("assets/profile.jpg"):
		profile_img = Image.open("assets/profile.jpg")
		st.image(profile_img, use_container_width=True)
	
	st.markdown("## **Gilbert ASANI KAMARA**")
	st.markdown("---")
	
	# Professional Bio Snippet
	st.markdown("### 🎓 **Expertise**")
	st.write("Python Developer since 2019, specializing in high-scale Data Engineering and Algorithmic Trading systems.")
	
	st.markdown("---")
	st.markdown("### 📍 **Location**")
	st.write("Bukavu, DRC / Nairobi, Kenya")

	st.markdown("### 📱 **Connect**")
	st.write("📧 gilbertakg@gmail.com")
	st.write("💬 WhatsApp: [+243 893958170]")
	
	st.markdown("---")
	st.caption("© 2026 Silicon Savannah Solutions")

# 3. MAIN INTERFACE (STORY & SKILLS)
# Header for Mobile: If sidebar is closed, we want them to see who you are
# st.title("Full-Stack Data Engineer Portfolio")
st.title("Gilbert ASANI KAMARA")
st.write("Python Developer, specializing in Data Engineering and Algorithmic Trading systems.")
# st.write("Python Developer since 2019, specializing in high-scale Data Engineering and Algorithmic Trading systems.")
# High-quality profile picture

col_img, _ = st.columns([1, 1])
with col_img:
	if os.path.exists("assets/profile2.jpg"):
		profile_img = Image.open("assets/profile2.jpg")
		st.image(profile_img, use_container_width=True)

col_intro, col_stats = st.columns([2, 1])
with col_intro:
	st.header("My Story 📖")
	st.write("""
	I started my coding journey in **2019**, driven by a passion for automation and complex data structures. 
	Over the past **5 years**, I have deeply specialized in **Algorithmic Trading Research**, where precision and 
	speed are non-negotiable. 

	My technical DNA is built on **Python**, but I am equally proficient in building modern web interfaces using 
	**HTML5, CSS3, and JavaScript**. I bridge the gap between complex backend logic and elegant user experiences.

	As a **self-taught programmer**, I have forged my skills through rigorous online training on platforms like 
	YouTube and Udemy, bypassing traditional academic routes to focus on immediate, industrial-grade applications. 
	This journey has instilled in me a unique ability to learn fast and adapt to the ever-evolving tech landscape 
	of the **Silicon Savannah**.

	My core expertise lies in **Data Engineering** and **Full-Stack Development**, with a particular focus on 
	**Web Scraping** and **Artificial Intelligence**. I specialize in building robust scrapers for 
	regional giants like **Jumia** and **BrighterMonday**, turning raw web data into actionable market intelligence.

	In the realm of **Algorithmic Trading**, I have spent over half a decade investigating the **GBPUSD** and 
	**EURUSD** currency pairs. By applying **Smart Money Concepts (SMC)** and multi-timeframe analysis, 
	I develop quantitative models and indicators, such as my **Signal Convergence Index (ICS)**, to navigate 
	complex financial markets.

	Beyond global markets, I am deeply committed to building **local technological infrastructure** in the 
	**Kivu region**. My projects, such as the automated **SNEL Cash Power** payment system in Bukavu, 
	aim to interconnect services and bring seamless digital utility automation to my community via mobile money 
	integrations.

	I operate as a **Full-Stack Data Engineer** who understands that data is only valuable when it is accessible 
	and actionable. Whether I am optimizing **Firebase Cloud Functions** or architecting complex 
	**Streamlit** dashboards, my goal remains the same: building high-performance solutions that solve 
	real-world problems.
	""")

with col_stats:
	st.header("Technical DNA 🛠️")
	st.progress(95, text="Python / Web Scraping")
	st.progress(90, text="Data Science / ML")
	st.progress(80, text="Algorithmic Trading")
	st.progress(70, text="Full-Stack (JS/CSS)")
	st.markdown("---")

with col_stats:
	st.header("LANGUAGES")
	st.progress(95, text = "Swahili (Native): Advanced")
	st.progress(90, text = "French : Advanced")
	st.progress(67, text = "English: Intermediate")
	st.progress(52, text = "Lingala: Elementary")
st.markdown("---")

# 4. NAVIGATION HUB (PROJECTS)
st.header("🚀 Solutions Showcase")
st.info("Click on a project to view the live interactive demonstration and GitHub source.")

# # We use tabs or columns for a clean "Portfolio Grid"
# tab_scraping, tab_ml, tab_data = st.tabs(["🔍 Web Scraping", "🤖 Machine Learning", "📊 Data Science"])


# --- CONFIGURATION ET ONGLETS ---
tab_ml, tab_data, tab_scraping = st.tabs([
	"🤖 Predictive ML", 
	"📊 Business Intelligence", 
	"📂 Extraction & Scraping", 
])


# --- ONGLETS : MACHINE LEARNING ---
with tab_ml:
	st.subheader("Predictive Analytics")
	col1, col2 = st.columns(2)
	
	with col1:
		st.write("### 01. Nairobi Food Forecaster")
		st.write("Time-series forecasting for staple food prices using local market data.")
		if st.button("View Food Forecast", key="btn_m3"):
			st.switch_page("pages/3_Nairobi_Food_Price_Forecaster.py")

	with col2:
		st.write("### 02. NSE AI Predictive Ticker")
		st.write("Machine Learning regression for Nairobi Securities Exchange live price movement.")
		if st.button("View AI Ticker", key="btn_m6"):
			st.switch_page("pages/6_NSE_AI_Predictive_Ticker.py")

# --- ONGLETS : DATA & DASHBOARDS ---
with tab_data:
	st.subheader("Fintech & Infrastructure Intelligence")
	col1, col2, col3 = st.columns(3)
	
	with col1:
		st.write("### 01. M-Pesa Admin Dashboard")
		st.write("Financial flow visualization and transaction scoring for fintech operations.")
		if st.button("View M-Pesa Analytics", key="btn_d4"):
			st.switch_page("pages/4_MPesa_Admin_Dashboard.py")
	
	with col2:
		st.write("### 02. Kenya Energy Monitor")
		st.write("Live tracking of energy distribution and grid stability metrics.")
		if st.button("View Energy Monitor", key="btn_d5"):
			st.switch_page("pages/5_Kenya_Energy_Live_Monitor.py")

	with col3:
		st.write("### 03. Traffic Heatmap")
		st.write("Geospatial analysis of Matatu movement and traffic congestion in Nairobi.")
		if st.button("View Traffic Map", key="btn_d7"):
			st.switch_page("pages/7_Nairobi_Traffic_Heatmap.py")

# --- ONGLETS : EXTRACTION ---
with tab_scraping:
	st.subheader("Massive Extraction Systems")
	col1, col2 = st.columns(2)
	
	with col1:
		st.write("### 01. BrighterMonday 🇰🇪")
		st.write("Extracting 1,000+ job insights with anti-bot bypass for the Kenyan market.")
		if st.button("View Job Board Project", key="btn_s1"):
			st.switch_page("pages/1_BrighterMonday_Job_Board.py")
			
	with col2:
		st.write("### 02. Jumia Price Tracker")
		st.write("Automated price intelligence and monitoring for the Kenyan e-commerce market.")
		if st.button("View Jumia Project", key="btn_s2"):
			st.switch_page("pages/2_Jumia_Tracker.py")

# 5. FOOTER (PERSISTENT)
st.markdown("---")
st.markdown(
	"""
	<div style="text-align: center; color: #888; padding: 20px;">
		Designed & Coded by Gilbert ASANI KAMARA | 2026 | Silicon Savannah Hub
	</div>
	""", 
	unsafe_allow_html=True
)

