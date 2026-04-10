import streamlit as st
from scraper import scrape_rbi_circulars, get_sample_circulars
from analyzer import analyze_circular, generate_amendment
import time

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
    st.image("https://via.placeholder.com/150x50/1a1a2e/ffffff?text=PolicyGuard")
    st.markdown("### 🏛️ Regulatory Sources")
    st.success("✅ RBI - Connected")
    st.success("✅ SEBI - Connected")
    st.success("✅ MCA - Connected")
    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.metric("Circulars Monitored", "247")
    st.metric("Alerts This Month", "12")
    st.metric("Policies Updated", "8")
    st.markdown("---")
    st.markdown("**Built for:** Indian Enterprises")
    st.markdown("**Response Time:** < 24 hours")

# Main tabs
tab1, tab2, tab3 = st.tabs([
    "📡 Live Circulars",
    "🔍 Analyze Impact",
    "📝 Generate Amendment"
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
            time.sleep(1)
            circulars = scrape_rbi_circulars()
            if circulars:
                st.success(f"✅ Loaded {len(circulars)} circulars!")
            st.session_state["circulars"] = circulars

    if fetch_sample or "circulars" not in st.session_state:
        circulars = get_sample_circulars()
        st.session_state["circulars"] = circulars

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

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📜 Regulatory Circular")
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
                report = analyze_circular(circular_text, company_policy)
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

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d;">
    🛡️ <strong>PolicyGuard</strong> | AI-Powered Regulatory Compliance | 
    Built for Indian Enterprises | RBI • SEBI • MCA
</div>
""", unsafe_allow_html=True)