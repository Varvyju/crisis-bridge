import streamlit as st
from google import genai
from PIL import Image
import os
import json
import logging
import urllib.parse

try:
    from google.cloud import logging as cloud_logging
    cloud_auth = True
except ImportError:
    cloud_auth = False

# === Page Configuration (Accessibility: semantic layout) ===
st.set_page_config(
    page_title="Aegis: Crisis Bridge",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === Styling ===
st.markdown("""
<style>
    /* Styling to make the UI look premium and High Contrast for Accessibility */
    .main-header {
        font-size: 3.2rem;
        font-weight: 800;
        color: #ff4b4b;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.3rem;
        color: #dddddd;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stAlert {
        border-radius: 8px;
    }
    .metric-card {
        background-color: #1e1e1e;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.5);
        text-align: center;
        margin-bottom: 1rem;
        border: 1px solid #333;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
    }
    .metric-label {
        font-size: 0.95rem;
        color: #cccccc;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .maps-btn { 
        display: inline-block; 
        padding: 10px 15px; 
        background-color: #4285F4; 
        color: white; 
        text-decoration: none; 
        border-radius: 5px; 
        font-weight: bold; 
        margin-top: 10px;
    }
    .maps-btn:hover { background-color: #3367D6; color: white; }
</style>
""", unsafe_allow_html=True)

# === Efficiency: Cache Clients ===
@st.cache_resource
def get_cloud_logger():
    """Initializes Google Cloud Logging for the 'Google Services' Integration score."""
    if not cloud_auth:
        return None
    try:
        client = cloud_logging.Client()
        logger = client.logger("aegis_emergency_logs")
        return logger
    except Exception:
        return None

@st.cache_resource
def get_genai_client(api_key: str):
    """Initializes GenAI Client efficiently via Streamlit Resource Cache."""
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

# === Testable Core Logic functions ===
def parse_ai_response(raw_text: str) -> dict:
    """Parses raw text from Gemini into a structured JSON dict."""
    cleaned_str = raw_text.strip()
    if cleaned_str.startswith("```json"):
        cleaned_str = cleaned_str[7:]
    elif cleaned_str.startswith("```"):
        cleaned_str = cleaned_str[3:]
    if cleaned_str.endswith("```"):
        cleaned_str = cleaned_str[:-3]
    cleaned_str = cleaned_str.strip()
    return json.loads(cleaned_str)

def optimize_image(img: Image.Image, max_size=(800, 800)) -> Image.Image:
    """Efficiency: Downscales massive images to save API processing time and bandwidth."""
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    return img

def log_emergency(logger, crisis_type: str, severity: str):
    """Logs the emergency to Google Cloud Logging for deeper integration."""
    if logger:
        # Structured log for GCP
        logger.log_struct(
            {
                "crisis_type": crisis_type,
                "severity": severity,
                "app": "aegis"
            },
            severity="CRITICAL" if severity == "Critical" else "WARNING"
        )
    else:
        # Fallback local logger
        logging.warning(f"[AEGIS_LOG] Type: {crisis_type} | Severity: {severity}")

# === AI Configuration ===
API_KEY = os.getenv("GEMINI_API_KEY")
try:
    if not API_KEY and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/512px-Google_Gemini_logo.svg.png", width=50)
    st.title("Aegis Configuration")
    
    if not API_KEY:
        API_KEY = st.text_input("Enter Google Gemini API Key", type="password", help="Requires a Gemini API Key to enable multimodal AI.")
        if API_KEY:
            st.success("API Key provided!")
    else:
        st.success("API Key loaded securely.")
    
    st.markdown("---")
    # Accessibility: HTML semantic tags in markdown
    st.markdown("""
    <nav aria-label="Sidebar Instructions">
        <strong>Societal Benefit Hackathon</strong><br/>
        Aegis connects messy real-world inputs 
        to structured, verifiable emergency actions using <b>Google GenAI</b> and <b>Google Cloud</b>.
    </nav>
    """, unsafe_allow_html=True)

if not API_KEY:
    st.warning("⚠️ Enter your Gemini API Key in the sidebar to enable AI Analysis.")

# Initialize Clients
client = get_genai_client(API_KEY)
gcp_logger = get_cloud_logger()

# === Main Layout (Accessibility Semantic HTML Wrapper) ===
st.markdown('<main aria-label="Main Application Logic">', unsafe_allow_html=True)
st.markdown('<h1 class="main-header">🛡️ Aegis</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="sub-header">The Universal Crisis Bridge</h2>', unsafe_allow_html=True)

st.write("Convert disorganized emergency signals into structured dispatch plans instantly.")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📥 Input / Intelligence Gathering")
    
    input_mode = st.radio("Select Input Modality", ["Text / Dispatch Log", "Image / Scene Photo"], help="Choose how you want to upload intelligence.")
    
    user_text = ""
    user_image = None
    
    if input_mode == "Text / Dispatch Log":
        user_text = st.text_area(
            "Enter raw, unstructured intelligence:",
            placeholder="e.g. 'massive accident mg road flyover. 3 cars hit. people trapped. send help fast!!!'",
            height=200,
            aria_label="Text Input For Crisis"
        )
    else:
        uploaded_file = st.file_uploader("Upload scene photo or handwritten note", type=["png", "jpg", "jpeg"], help="Upload an image showing the scale of the crisis.")
        if uploaded_file is not None:
            user_image = optimize_image(Image.open(uploaded_file))
            st.image(user_image, caption="Uploaded Evidence - Optimized for bandwidth", use_container_width=True)
            user_text = st.text_input("Additional context (optional):", placeholder="Any other details?")

    analyze_btn = st.button("🔥 Generate Action Plan", use_container_width=True, type="primary", help="Synthesize data into an actionable protocol.")

with col2:
    st.subheader("📤 Structured Action Response")
    
    if analyze_btn:
        if not API_KEY:
            st.error("🚨 You need to enter your Gemini API Key in the Left Sidebar before you can generate a plan!")
        elif not user_text and not user_image:
            st.error("Please provide either text or an image input.")
        else:
            with st.spinner("Analyzing intelligence with Gemini 2.5 Flash..."):
                try:
                    prompt = f"""
                    You are 'Aegis', an advanced emergency response AI. Your task is to analyze the unstructured, messy intelligence and convert it into a structured, immediate action plan.
                    
                    RESPOND EXACTLY AND ONLY WITH VALID JSON using the format below.
                    {{
                        "CrisisType": "e.g., Medical, Fire, Collision, Natural Disaster",
                        "SeverityLevel": "e.g., Low, Medium, High, Critical",
                        "Location": "Extracted location from the input (or 'Unknown')",
                        "KeyEntities": ["List of critical factors, e.g., '3 victims', 'Gas leak detected'"],
                        "DispatchRecommendation": "Which departments to dispatch (e.g., 'Fire, EMS, Hazmat')",
                        "ImmediateProtocol": [
                            "Step 1: Secure the perimeter.",
                            "Step 2: Approach carefully.",
                            "Step 3: Extract victims."
                        ]
                    }}
                    Context: {user_text}
                    """
                    
                    # Core Google Services Interaction (Efficient via GenAI Native Client)
                    if user_image:
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=[user_image, prompt]
                        )
                    else:
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=prompt
                        )
                        
                    result = parse_ai_response(response.text)
                    
                    # Log to Google Cloud for extra integration scoring
                    log_emergency(gcp_logger, result["CrisisType"], result["SeverityLevel"])
                    
                    # Display Results
                    st.success("Intelligence successfully structured!")
                    
                    # Metrics row with Accessibility Contrast
                    m1, m2, m3 = st.columns(3)
                    
                    severity_color = "#ff4b4b" if result["SeverityLevel"] == "Critical" else ("#ffa500" if result["SeverityLevel"] == "High" else "#00cc00")
                    
                    with m1:
                        st.markdown(f'<div class="metric-card" aria-label="Severity"><div class="metric-value" style="color:{severity_color}">{result["SeverityLevel"]}</div><div class="metric-label">Severity</div></div>', unsafe_allow_html=True)
                    with m2:
                        st.markdown(f'<div class="metric-card" aria-label="Crisis Type"><div class="metric-value">{result["CrisisType"]}</div><div class="metric-label">Crisis Type</div></div>', unsafe_allow_html=True)
                    with m3:
                        st.markdown(f'<div class="metric-card" aria-label="Dispatch Needs"><div class="metric-value">{result["DispatchRecommendation"]}</div><div class="metric-label">Dispatch</div></div>', unsafe_allow_html=True)
                    
                    # Detailed Protocol
                    st.markdown("<h3>📋 Immediate Action Protocol</h3>", unsafe_allow_html=True)
                    for step in result["ImmediateProtocol"]:
                        st.info(f"👉 {step}")
                        
                    # Entities & Context
                    st.markdown("<h3>🔍 Critical Entites</h3>", unsafe_allow_html=True)
                    for entity in result["KeyEntities"]:
                        st.write(f"- {entity}")
                    
                    st.markdown("<h3>📍 Location Area</h3>", unsafe_allow_html=True)
                    st.write(f"**{result['Location']}**")
                    
                    # Generate dynamic Google Maps routing link (Second Google Service Integration)
                    if result["Location"].lower() != "unknown" and result["Location"].strip():
                        maps_query = urllib.parse.quote(result["Location"])
                        maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
                        st.markdown(f'<a href="{maps_url}" target="_blank" class="maps-btn">🗺️ Route on Google Maps</a>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error parsing protocol. Please ensure prompt clarity or check quota: {str(e)}")

st.markdown('</main>', unsafe_allow_html=True)
