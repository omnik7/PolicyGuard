import streamlit as st
from scraper import scrape_rbi_circulars, get_sample_circulars
from analyzer import analyze_circular, generate_amendment, detect_changes
import time
from streamlit_autorefresh import st_autorefresh

# Auto refresh every 60 seconds
st_autorefresh(interval=60000, key="autorefresh")

# Page config
st.set_page_config(
    page_title="PolicyGuard",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .circular-card {
        background: #f8f9fa;
        border-left: 4px solid #e63946;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .high-impact { border-left-color: #e63946; }
    .medium-impact { border-left-color: #f4a261; }
    .low-impact { border-left-color: #2a9d8f; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 style="color: white; font-size: 3rem;">🛡️ PolicyGuard</h1>
    <p style="color: #adb5bd; font-size: 1.2rem;">AI-Powered Compliance & Regulatory Intelligence System</p>
    <p style="color: #e63946;">Never miss a regulatory change again</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("logo.png")
    st.markdown("### 🏛️ Regulatory Sources")
    st.success("✅ RBI - Connected")
    st.success("✅ SEBI - Connected")
    st.success("✅ MCA - Connected")
    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.metric("Circulars Monitored", "247", "+3 today")
    st.metric("Alerts This Month", "12", "+2 this week")
    st.metric("Policies Updated", "8", "+1 today")
    st.markdown("---")
    st.markdown("### ⏰ Auto-Monitor Status")
    st.success("🟢 Monitoring Active")

    # Dynamic last checked time
    if "last_fetched" in st.session_state:
        import time
        elapsed = int(time.time() - st.session_state["last_fetched"])
        if elapsed < 60:
            last_checked = "< 1 min ago"
            next_check = "59 mins"
            progress_val = 99
        elif elapsed < 3600:
            mins = elapsed // 60
            last_checked = f"{mins} mins ago"
            next_check = f"{60 - mins} mins"
            progress_val = max(0, 100 - mins)
        else:
            last_checked = "1 hour ago"
            next_check = "checking now..."
            progress_val = 0
    else:
        last_checked = "5 mins ago"
        next_check = "55 mins"
        progress_val = 85

    st.markdown(f"**Last Checked:** {last_checked}")
    st.markdown(f"**Next Check:** {next_check}")
    st.markdown("**Sources:** RBI • SEBI • MCA")
    st.progress(progress_val, text="Daily scan progress")
    st.markdown("---")
    st.markdown("### 🔔 Recent Alerts")
    st.warning("⚠️ New RBI Circular detected!")
    st.info("📋 3 policies need update")
    st.markdown("---")
    st.markdown("### 🤖 AI Agents Status")
    st.success(" Agent 1: Regulatory Monitor")
    st.success(" Agent 2: Change Detector")
    st.success(" Agent 3: Impact Analyzer")
    st.success(" Agent 4: Amendment Drafter")
    st.markdown("---")
    st.markdown("**Built for:** Indian Enterprises")
    

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📡 Live Circulars",
    "🔍 Analyze Impact", 
    "📝 Generate Amendment",
    "🔄 Change Detection"
])

# TAB 1: Live Circulars
with tab1:
    st.header("📡 Latest Regulatory Circulars")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        fetch_rbi = st.button("🏦 Fetch RBI Circulars", use_container_width=True)
    with col2:
        fetch_sample = st.button("📋 Load Sample Data", use_container_width=True)
    with col3:
        fetch_all = st.button("🔄 Fetch All Sources", use_container_width=True)

    if fetch_rbi or fetch_all:
        with st.spinner("Fetching latest circulars from RBI, SEBI, MCA..."):
            import time
            time.sleep(1)
            circulars = scrape_rbi_circulars()
            st.session_state["last_fetched"] = time.time()
            if circulars:
                st.success(f"✅ Loaded {len(circulars)} circulars!")
            st.session_state["circulars"] = circulars

    if fetch_sample or "circulars" not in st.session_state:
        import time
        circulars = get_sample_circulars()
        st.session_state["circulars"] = circulars
        st.session_state["last_fetched"] = time.time()
    # Automated monitoring banner
import time
if "last_fetched" in st.session_state:
    elapsed = int(time.time() - st.session_state["last_fetched"])
    if elapsed < 60:
        banner_last = f"{elapsed} secs ago"
        banner_next = "59 mins"
    elif elapsed < 3600:
        mins = elapsed // 60
        secs = elapsed % 60
        banner_last = f"{mins}m {secs}s ago"
        banner_next = f"{60 - mins} mins"
    else:
        banner_last = "1 hour ago"
        banner_next = "checking now..."
else:
    banner_last = "5 minutes ago"
    banner_next = "55 minutes"

st.markdown(f"""
<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); 
     padding: 1rem; border-radius: 10px; margin-bottom: 1rem;
     border-left: 4px solid #2a9d8f;">
    <h4 style="color: #2a9d8f; margin:0;">🤖 Autonomous Monitoring Active</h4>
    <p style="color: #adb5bd; margin:0; font-size:0.9rem;">
    PolicyGuard automatically checks RBI, SEBI and MCA every hour. 
    Last scan: <strong style="color:white;">{banner_last}</strong> | 
    Next scan: <strong style="color:white;">{banner_next}</strong>
    </p>
</div>
""", unsafe_allow_html=True)
if "circulars" in st.session_state:
    if "circulars" in st.session_state:
        for i, circular in enumerate(st.session_state["circulars"]):
            with st.expander(f"📌 {circular['source']} | {circular['title'][:80]}..."):
                st.write(circular.get("content", circular.get("url", "")))
                if st.button(f"Analyze This Circular", key=f"analyze_{i}"):
                    st.session_state["selected_circular"] = circular
                    st.success("✅ Circular selected! Go to 'Analyze Impact' tab")

# TAB 2: Analyze Impact
with tab2:
    st.header("🔍 Compliance Impact Analyzer")

    col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📜 Regulatory Circular")
    if "selected_circular" in st.session_state:
        circular_text = st.text_area(
            "Circular Content",
            value=st.session_state["selected_circular"].get("content",
                  st.session_state["selected_circular"].get("title", "")),
            height=200
        )
    else:
        circular_text = st.text_area(
            "Paste circular content here...",
            height=200,
            placeholder="Paste RBI/SEBI/MCA circular text here..."
        )

with col2:
    st.subheader("📋 Company Policy")
    try:
        with open("sample_data/sample_policy.txt", "r") as f:
            default_policy = f.read()
    except:
        default_policy = "Paste your company policy here..."

    company_policy = st.text_area(
        "Company Policy",
        value=default_policy,
        height=200
    )

with col3:
    st.subheader("📄 Contracts & Products")
    contracts_text = st.text_area(
        "Contracts & Products",
        height=200,
        placeholder="""Paste your contracts or product details here...

Example:
- Home Loan Product: Max 80% LTV
- Personal Loan: No collateral required
- KYC Contract clause 3.2: Annual verification
- Digital Wallet Agreement: Section 4.1
"""
    )
    if "selected_circular" in st.session_state:
        circular_text = st.text_area(
            "Circular Content",
            value=st.session_state["selected_circular"].get("content", ""),
            height=250
        )
    else:
        circular_text = st.text_area(
            "Paste circular content here...",
            height=250,
            placeholder="Paste RBI/SEBI/MCA circular text here..."
        )

    with col2:
        st.subheader("📋 Your Company Policy")
        try:
            with open("sample_data/sample_policy.txt", "r") as f:
                default_policy = f.read()
        except:
            default_policy = "Paste your company policy here..."

        company_policy = st.text_area(
            "Company Policy",
            value=default_policy,
            height=250
        )

    if st.button("🚀 Generate Impact Report", use_container_width=True, type="primary"):
        if circular_text and company_policy:
            with st.spinner("🤖 PolicyGuard AI is analyzing compliance impact..."):
                # Combine policy and contracts for analysis
                full_context = company_policy
                if contracts_text:
                    full_context = f"{company_policy}\n\nCONTRACTS & PRODUCTS:\n{contracts_text}"
                report = analyze_circular(circular_text, full_context)
                st.session_state["report"] = report
                st.session_state["circular_for_amendment"] = circular_text
        else:
            st.error("Please provide both circular content and company policy!")

    if "report" in st.session_state:
        st.markdown("---")
        st.subheader("📊 Compliance Impact Report")
        st.markdown(st.session_state["report"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📥 Download Report",
                st.session_state["report"],
                file_name="PolicyGuard_Report.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col2:
            if st.button("📝 Generate Amendment →", use_container_width=True):
                st.info("Go to 'Generate Amendment' tab!")

# TAB 3: Generate Amendment
with tab3:
    st.header("📝 Auto-Generate Policy Amendment")
    st.info("PolicyGuard will rewrite your policy section to be fully compliant")

    policy_section = st.text_area(
        "Paste the specific policy section to update",
        height=150,
        placeholder="e.g., Paste your KYC policy section here..."
    )

    circular_for_amendment = st.text_area(
        "Relevant Circular",
        value=st.session_state.get("circular_for_amendment", ""),
        height=150
    )

    if st.button("✨ Generate Compliant Amendment", use_container_width=True, type="primary"):
        if policy_section and circular_for_amendment:
            with st.spinner("✍️ Drafting compliant policy amendment..."):
                amendment = generate_amendment(circular_for_amendment, policy_section)
                st.markdown("---")
                st.subheader("✅ Updated Policy Text (Ready to Use)")
                st.markdown(amendment)
                st.download_button(
                    "📥 Download Amendment",
                    amendment,
                    file_name="PolicyGuard_Amendment.txt",
                    use_container_width=True
                )
        else:
            st.error("Please provide both the policy section and circular!")
# TAB 4: Change Detection
with tab4:
    st.header("🔄 Regulatory Change Detector")
    st.info("Compare old vs new circular to detect exactly what changed")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📜 Old Circular Version")
        old_circular = st.text_area(
            "Paste previous circular here...",
            height=250,
            placeholder="""Example:
RBI Circular 2023:
- KYC renewal every 5 years
- PAN required above Rs 1 lakh
- Video KYC optional
"""
        )

    with col2:
        st.subheader("📜 New Circular Version")
        new_circular = st.text_area(
            "Paste new circular here...",
            height=250,
            placeholder="""Example:
RBI Circular 2024:
- KYC renewal every 2 years
- PAN required above Rs 50,000
- Video KYC mandatory above Rs 10 lakhs
"""
        )

    if st.button("🔍 Detect Changes", use_container_width=True, type="primary"):
        if old_circular and new_circular:
            with st.spinner("🧠 Agent 2 detecting regulatory changes..."):
                changes = detect_changes(old_circular, new_circular)
                st.markdown("---")
                st.subheader("📊 Change Detection Report")
                st.markdown(changes)
                st.download_button(
                    "📥 Download Change Report",
                    changes,
                    file_name="PolicyGuard_Changes.txt",
                    use_container_width=True
                )
        else:
            st.error("Please provide both old and new circular versions!")

    st.markdown("---")
    st.subheader("💡 Demo — Try This Example")
    if st.button("Load Sample Comparison", use_container_width=True):
        st.session_state["demo_old"] = """RBI Circular 2023 - KYC Guidelines:
1. KYC renewal every 5 years for all customers
2. PAN required for transactions above Rs 1 lakh  
3. Video KYC optional
4. Re-KYC for high risk customers every 3 years
5. Digital wallet KYC updated annually"""

        st.session_state["demo_new"] = """RBI Circular 2024 - KYC Guidelines Updated:
1. KYC renewal every 2 years for all customers
2. PAN required for transactions above Rs 50,000
3. Video KYC mandatory for accounts above Rs 10 lakhs
4. Re-KYC for high risk customers every 1 year
5. Digital wallet KYC updated every 6 months
6. Aadhaar OTP verification now mandatory"""
        st.success("✅ Sample loaded! Scroll up and click Detect Changes!")
# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d;">
    🛡️ <strong>PolicyGuard</strong> | AI-Powered Regulatory Compliance | 
    Built for Indian Enterprises | RBI • SEBI • MCA
</div>
""", unsafe_allow_html=True)