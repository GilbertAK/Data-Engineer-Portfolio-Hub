import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import os

# --- INTEGRATED ANALYTICS ENGINE ---
class AdminEngine:
	@staticmethod
	def generate_bulk_applicants(n=10):
		names = ["Kamau", "Otieno", "Mutesi", "Wanjiku", "Ochieng", "Hassan", "Cherono", "Mutua", "Achieng", "Njoroge"]
		data = []
		for i in range(n):
			income = np.random.randint(25000, 120000)
			expenses = np.random.randint(15000, income)
			score = np.random.randint(300, 850)
			data.append({
				"ID": f"MP-{100+i}",
				"Name": names[i % len(names)],
				"Monthly Income": income,
				"Expenses": expenses,
				"Score": score,
				"Status": "Pending"
			})
		return pd.DataFrame(data)

# --- PAGE CONFIG ---
st.set_page_config(page_title="M-Pesa Admin Risk Portal", layout="wide")

# --- CUSTOM CSS FOR UNIFORMITY & ANIMATION ---
st.markdown("""
	<style>
	[data-testid="stSidebar"] .stMarkdown p { color: #ffffff !important; }
	@keyframes slideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
	.stMetric, .stPlot, .stTable { animation: slideUp 0.6s ease-out; }
	.admin-header { background: #161b22; padding: 20px; border-radius: 10px; border-left: 5px solid #00d4ff; margin-bottom: 25px; }
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

# --- HEADER SECTION ---
st.title("🏦 M-Pesa Financial Scoring Admin Portal")

# --- GITHUB LINK ---
st.markdown(
	"""
	<div class="github-link">
		<b>📂 Source Code:</b> 
		<a href='https://github.com/GilbertAK/MPesaFinancialScoring' target='_blank' style='color: #ff4b4b; text-decoration: none;'>
			View on GitHub Repository
		</a>
	</div>
	""", 
	unsafe_allow_html=True
)

st.markdown("""
<div class="admin-header">
	<h3>Executive Summary</h3>
	<p>This <b>B2B Risk Management Dashboard</b> allows financial administrators to assess the creditworthiness 
	of mobile money users in real-time. By analyzing M-Pesa transaction patterns, utility bill consistency, 
	and debt-to-income ratios, the system generates a <b>Credit Score (300-850)</b>. 
	Administrators can set risk thresholds, review bulk applications, and monitor portfolio health dynamically.</p>
</div>
""", unsafe_allow_html=True)

# --- ADMIN CONTROLS ---
st.subheader("⚙️ System Global Parameters")
c1, c2, c3 = st.columns([1, 1, 1])
with c1:
	min_pass_score = st.slider("Minimum Approval Score", 300, 850, 650, 
							 help="Applicants below this score are automatically flagged for rejection.")
with c2:
	interest_rate = st.slider("Base Interest Rate (%)", 5.0, 25.0, 12.0, 
							 help="Adjust the global interest rate based on current market risk.")
with c3:
	data_refresh = st.button("🔄 Sync M-Pesa Cloud Logs", help="Fetches latest transaction metadata from Safaricom API (Simulated).")

if data_refresh:
	with st.spinner("Processing transaction hashes..."):
		time.sleep(1)
		st.toast("Logs synchronized successfully!")

# --- DATA PROCESSING ---
if 'applicants' not in st.session_state:
	st.session_state.applicants = AdminEngine.generate_bulk_applicants(12)

df = st.session_state.applicants
df['Decision'] = df['Score'].apply(lambda s: "✅ Approve" if s >= min_pass_score else "❌ Reject")

# --- PORTFOLIO METRICS ---
st.write("---")
st.header("1. Portfolio Health Overview")
m1, m2, m3, m4 = st.columns(4)
total_apps = len(df)
approved_count = len(df[df['Decision'] == "✅ Approve"])
avg_score = int(df['Score'].mean())

m1.metric("Total Applicants", total_apps, help="Total unique IDs analyzed today.")
m2.metric("Approval Rate", f"{(approved_count/total_apps)*100:.1f}%", help="Percentage of users meeting current score threshold.")
m3.metric("Avg. Credit Score", avg_score, delta=f"{avg_score-500}", help="Weighted average across current segment.")
m4.metric("Risk Exposure", "KSh 1.2M", delta="-5%", delta_color="normal", help="Estimated capital at risk in current segment.")

# --- DATA VISUALIZATION ---
st.write("---")
st.header("2. Risk Analysis & Segmentation")
g1, g2 = st.columns([1.5, 1])

with g1:
	st.subheader("Credit Score Distribution (Bulk Data)")
	fig, ax = plt.subplots(figsize=(10, 5))
	plt.style.use('dark_background')
	ax.hist(df['Score'], bins=10, color='#00d4ff', alpha=0.7, edgecolor='white')
	ax.axvspan(300, min_pass_score, color='red', alpha=0.2, label='Rejection Zone')
	ax.axvline(min_pass_score, color='red', linestyle='--', label='Admin Threshold')
	ax.set_xlabel("FICO-Equivalent Score")
	ax.set_ylabel("Number of Applicants")
	ax.legend()
	st.pyplot(fig)
	st.info("**Insight:** The red shaded area represents applicants who fail to meet your current risk appetite.")

with g2:
	st.subheader("Status Breakdown")
	status_counts = df['Decision'].value_counts()
	fig2, ax2 = plt.subplots()
	ax2.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', colors=['#44ff44', '#ff4b4b'], startangle=90, textprops={'color':"w"})
	st.pyplot(fig2)

# --- DATA TABLE ---
st.write("---")
st.header("3. Application Management Queue")
st.write("Manage individual cases based on AI recommendations.")

search_query = st.text_input("🔍 Search by Applicant Name or ID", "")
filtered_df = df[df['Name'].str.contains(search_query, case=False) | df['ID'].str.contains(search_query)]

def color_decision(val):
	color = '#44ff44' if 'Approve' in val else '#ff4b4b'
	return f'color: {color}; font-weight: bold'

st.dataframe(filtered_df.style.applymap(color_decision, subset=['Decision']), use_container_width=True, hide_index=True)

# --- ACTIONS & NAVIGATION ---
st.markdown("### 📤 Bulk Operations")
c_act1, c_act2, c_act3 = st.columns(3)
with c_act1:
	if st.button("📥 Export CSV Report", use_container_width=True):
		st.success("Report generated: mpesa_risk_report.csv")
with c_act2:
	if st.button("📧 Notify Approved Users", use_container_width=True):
		st.info("Sending SMS notifications via Africa's Talking API...")
with c_act3:
	if st.button("⬅️ Back to Portfolio Hub", key="bottom_back", use_container_width=True):
		st.switch_page("app.py")

# --- FOOTER ---
# st.markdown("---")
st.markdown(f"<div class='footer'>M-Pesa Risk Engine v2.1 | Admin Console | Developed by Gilbert ASANI KAMARA (2026)</div>", unsafe_allow_html=True)
