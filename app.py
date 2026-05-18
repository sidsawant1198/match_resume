import os
import google.generativeai as genai
import streamlit as st
from pdf_text_extractor import extract_text
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Skill Matcher AI",
    page_icon="🎯",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Dark background ── */
.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Remove Streamlit default top padding ── */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
}

[data-testid="stAppViewContainer"] > .main {
    padding-top: 0rem !important;
}

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a0f2e 50%, #0f1a2e 100%);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 20px;
    padding: 48px 52px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 20%;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(16,185,129,0.1) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.4);
    color: #818cf8;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 6px 16px;
    border-radius: 100px;
    margin-bottom: 20px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 52px;
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 0%, #818cf8 60%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 14px 0;
}
.hero-sub {
    color: #94a3b8;
    font-size: 17px;
    font-weight: 300;
    margin: 0;
    max-width: 520px;
    line-height: 1.6;
}

/* ── Step cards ── */
.steps-row {
    display: flex;
    gap: 16px;
    margin-bottom: 32px;
}
.step-card {
    flex: 1;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 22px 24px;
    display: flex;
    align-items: flex-start;
    gap: 16px;
    transition: border-color 0.2s;
}
.step-card:hover { border-color: rgba(99,102,241,0.35); }
.step-num {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: rgba(99,102,241,0.4);
    line-height: 1;
    min-width: 32px;
}
.step-text strong {
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #e2e8f0;
    display: block;
    margin-bottom: 4px;
}
.step-text span {
    font-size: 13px;
    color: #64748b;
    line-height: 1.5;
}

/* ── Section label ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 10px;
}

/* ── Result container ── */
.result-box {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 32px 36px;
    margin-top: 24px;
}
.result-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #34d399;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* ── Sidebar styling ── */
[data-testid="stSidebar"] {
    background: #0d0d18 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #e2e8f0 !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── Sidebar logo area ── */
.sidebar-logo {
    background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(52,211,153,0.1));
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin-bottom: 24px;
}
.sidebar-logo-icon {
    font-size: 36px;
    margin-bottom: 8px;
}
.sidebar-logo-text {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 15px;
    color: #818cf8;
}

/* ── Warning box ── */
.warn-box {
    background: rgba(251,191,36,0.08);
    border: 1px solid rgba(251,191,36,0.25);
    border-radius: 10px;
    padding: 14px 18px;
    color: #fbbf24;
    font-size: 14px;
    margin-top: 8px;
}

/* ── Error box ── */
.error-box {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 10px;
    padding: 14px 18px;
    color: #f87171;
    font-size: 14px;
    margin-top: 8px;
}

/* ── Text area ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    resize: vertical !important;
}
.stTextArea textarea:focus {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px dashed rgba(99,102,241,0.3) !important;
    border-radius: 12px !important;
    padding: 8px !important;
}

/* ── Analyse button ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 32px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; }
.stButton > button:disabled {
    background: rgba(99,102,241,0.25) !important;
    cursor: not-allowed !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #6366f1 !important; }

/* ── Success message ── */
.stSuccess {
    background: rgba(52,211,153,0.08) !important;
    border: 1px solid rgba(52,211,153,0.25) !important;
    border-radius: 10px !important;
    color: #34d399 !important;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.06) !important; }
</style>
""", unsafe_allow_html=True)

# ── Configure model ───────────────────────────────────────────────────────────
api_key = os.getenv("GOOGLE_GEMINI_API") or st.secrets.get("GOOGLE_GEMINI_API")
if not api_key:
    st.error("⚠ Gemini API key not found. Set GOOGLE_GEMINI_API in your .env or Streamlit secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🎯</div>
        <div class="sidebar-logo-text">SKILL MATCHER AI</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Upload Resume</div>', unsafe_allow_html=True)
    pdf_doc = st.file_uploader("PDF only", type=["pdf"], label_visibility="collapsed")

    pdf_text = None
    if pdf_doc:
        try:
            pdf_text = extract_text(pdf_doc)
            st.success(f"✓ {pdf_doc.name}")
        except ValueError as e:
            # Catches scanned PDF, empty PDF, corrupt PDF
            st.markdown(f'<div class="warn-box">⚠ {e}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="warn-box">⚠ Please upload your resume to get started.</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="color:#475569; font-size:12px; line-height:1.7;">
        Powered by <span style="color:#818cf8;">Google Gemini AI</span><br>
        Your resume is never stored.
    </div>
    """, unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ AI Powered</div>
    <div class="hero-title">Land Your Dream Job</div>
    <p class="hero-sub">Upload your resume and paste a job description. Our AI analyses the match, scores your ATS compatibility, and rewrites your resume to maximise shortlisting chances.</p>
</div>
""", unsafe_allow_html=True)

# ── Steps ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="steps-row">
    <div class="step-card">
        <div class="step-num">1</div>
        <div class="step-text">
            <strong>Upload Resume</strong>
            <span>Add your PDF resume in the sidebar panel on the left.</span>
        </div>
    </div>
    <div class="step-card">
        <div class="step-num">2</div>
        <div class="step-text">
            <strong>Paste Job Description</strong>
            <span>Copy the full job description and paste it below.</span>
        </div>
    </div>
    <div class="step-card">
        <div class="step-num">3</div>
        <div class="step-text">
            <strong>Get Your Analysis</strong>
            <span>Receive ATS score, SWOT, and two AI-optimised resume versions.</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Job Description Input ─────────────────────────────────────────────────────
st.markdown('<div class="section-label">Job Description</div>', unsafe_allow_html=True)
job_desc = st.text_area(
    "job_desc",
    placeholder="Paste the full job description here...",
    height=220,
    max_chars=10000,
    label_visibility="collapsed"
)

# ── Analyse Button (gates the API call) ───────────────────────────────────────
analyse = st.button(
    "🎯 Analyse My Resume",
    disabled=(not pdf_text or not job_desc.strip())
)

# ── Prompt & Response ─────────────────────────────────────────────────────────
if analyse:
    # Both inputs are guaranteed to be present here (button is disabled otherwise)
    prompt = f'''Assuming you are an expert in job skill matching and profile short listing.
You have the resume = {pdf_text} and job description = {job_desc}. Using this data generate the
output on the following outline:

* Calculate and show the ATS score. Discuss matching and non matching keywords (max 2 line discussion).
* Calculate and show the chances of selection of profile (One line discussion)
* Perform SWOT analysis and discuss in bullet points.
* Discuss in bullet points what the positives in the resume that will help in getting shortlisted.
* Discuss in bullet points what other things can be mentioned and discussed in resume.
* Prepare two revised resume's for this particular job description with chances of selection
  being maximised while implementing all the points discussed above.
* Prepare these resume in such a way that it can be copied and pasted in word and generate pdf.'''

    try:
        with st.spinner("Analysing your resume against the job description..."):
            response = model.generate_content(prompt)

        st.success("✓ Analysis complete!")

        st.markdown("""
        <div class="result-box">
            <div class="result-title">📊 Your Resume Analysis</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(response.text)

    except Exception as e:
        st.markdown(f'<div class="error-box">❌ Something went wrong: {e}</div>', unsafe_allow_html=True)
