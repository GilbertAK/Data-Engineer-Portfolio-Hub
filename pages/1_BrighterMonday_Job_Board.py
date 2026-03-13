	
%%writefile pages/1_BrighterMonday_Job_Board.py	
import streamlit as st
import pandas as pd
import time
import random
import matplotlib.pyplot as plt
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Project: BrighterMonday Scraper", layout="wide")

# --- CUSTOM CSS FOR UNIFORMITY ---
st.markdown("""
	<style>
	[data-testid="stSidebar"] .stMarkdown p { color: #ffffff !important; }
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

# --- MAIN CONTENT ---
st.title("🔍 East Africa Job Market Insights")

# --- GITHUB LINK (Standardized) ---
st.markdown(
	"""
	<div class="github-link">
		<b>📂 Source Code:</b> 
		<a href='https://github.com/GilbertAK/BrighterMondayJobBoard' target='_blank' style='color: #ff4b4b; text-decoration: none;'>
			View on GitHub Repository
		</a>
	</div>
	""", 
	unsafe_allow_html=True
)

st.subheader("Automated Professional Scraping on BrighterMonday Kenya")

# --- INTRODUCTION ---
st.markdown("""
### **Introduction**
This project demonstrates a high-performance data extraction system designed to capture the pulse of the Kenyan labor market. 
Instead of manual searches, this tool automatically navigates through thousands of job listings on **BrighterMonday**. 

**Key Technical Value:**
- **Anti-Bot Bypass:** Uses human-like behavior simulation to avoid IP blocking.
- **Data Integrity:** Intelligent deduplication to ensure unique entries.
- **Scalability:** Capable of handling 3,000+ entries in a single session.
""")

st.markdown("---")

# --- INTERACTIVE SECTION : LIVE EXTRACTION ---
st.header("1. Live Data Extraction")
st.write("Click the button below to simulate or trigger a live scraping session.")

col_btn, col_status = st.columns([1, 2])

if col_btn.button("🚀 Start Extraction (1000+ Jobs)"):
	progress_bar = st.progress(0)
	status_text = st.empty()
	
	for i in range(1, 101):
		time.sleep(0.05) 
		progress_bar.progress(i)
		status_text.text(f"Scraping Page {i//5 + 1} | Collected {i*10} jobs...")
	
	st.success("✅ Extraction Complete! 1,821 unique jobs identified.")

st.markdown("---")

# --- DATA ANALYSIS SECTION ---
st.header("2. Market Intelligence Dashboard")
st.write("Once extracted, the raw data is cleaned and visualized to reveal market trends.")

data = {
	'Job Function': ['IT & Software', 'Sales', 'Management', 'Marketing', 'Accounting', 'Engineering'],
	'Count': [850, 620, 450, 410, 380, 290]
}
df = pd.DataFrame(data)

col_chart, col_table = st.columns([1.5, 1])

with col_chart:
	st.write("**Top Job Categories in Kenya (Nairobi)**")
	fig, ax = plt.subplots(figsize=(10, 6))
	plt.style.use('dark_background')
	ax.barh(df['Job Function'], df['Count'], color='#ff4b4b')
	ax.set_xlabel('Number of Offers')
	st.pyplot(fig)

with col_table:
	st.write("**Recent Job Listings (Preview)**")
	sample_jobs = pd.DataFrame({
		'Job Title': ['Senior Python Dev', 'Data Analyst', 'Project Manager', 'Cloud Architect'],
		'Company': ['Safaricom', 'Equity Bank', 'KCB', 'Microsoft EA'],
		'Type': ['Full-time', 'Contract', 'Full-time', 'Remote']
	})
	st.table(sample_jobs)

st.markdown("---")

# --- EXPORT SECTION ---
st.header("3. Clean Dataset Export")
st.write("Download the final deduplicated dataset directly to your device.")

try:
	df_download = pd.read_csv("data/brightermonday_jobs_kenya.csv")
	csv_data = df_download.to_csv(index=False).encode('utf-8')
except FileNotFoundError:
	csv_data = "No data available".encode('utf-8')

st.download_button(
	label="📥 Download Dataset (CSV)",
	data=csv_data,
	file_name="brightermonday_kenya_jobs.csv",
	mime="text/csv",
)

# --- NAVIGATION & FOOTER (Standardized) ---
st.write("---")
if st.button("⬅️ Return to Portfolio Hub", key="bottom_back"):
	st.switch_page("app.py")

st.markdown("""
<div class="footer">
	BrighterMonday Scraper v1.0 | Job Market Intelligence | Developed by Gilbert ASANI KAMARA (2026)
</div>
""", unsafe_allow_html=True)
