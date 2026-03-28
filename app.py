import streamlit as st
from google import genai
from PIL import Image
import os
import json

# === Page Configuration ===
st.set_page_config(
    page_title="Aegis: Crisis Bridge",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === Styling ===
st.markdown("""
<style>
    /* Styling to make the UI look premium */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        color: #ff4b4b;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #aaaaaa;
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
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #aaaaaa;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# === AI Configuration ===
# Prompt the user for an API key if not set in environment or secrets
API_KEY = os.getenv("GEMINI_API_KEY")
try:
    if not API_KEY and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

# Sidebar configuration
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/512px-Google_Gemini_logo.svg.png", width=50)
    st.title("Aegis Configuration")
    if not API_KEY:
        API_KEY = st.text_input("Enter Google Gemini API Key", type="password")
        if API_KEY:
            st.success("API Key provided!")
    else:
        st.success("API Key loaded securely.")
    
    st.markdown("---")
    st.markdown("""
    **Societal Benefit Hackathon**
    Aegis is a universal bridge that connects messy real-world inputs 
    to structured, verifiable emergency actions.
    """)

if not API_KEY:
    st.warning("⚠️ Enter your Gemini API Key in the sidebar to enable AI Analysis.")

# === Main Layout ===
st.markdown('<p class="main-header">🛡️ Aegis</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">The Universal Crisis Bridge</p>', unsafe_allow_html=True)

st.write("Convert disorganized emergency signals (photos, erratic text) into structured dispatch plans instantly.")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📥 Input / Intelligence Gathering")
    
    input_mode = st.radio("Select Input Modality", ["Text / Dispatch Log", "Image / Scene Photo"])
    
    user_text = ""
    user_image = None
    
    if input_mode == "Text / Dispatch Log":
        user_text = st.text_area(
            "Enter raw, unstructured intelligence:",
            placeholder="e.g. 'massive accident mg road flyover. 3 cars hit. one upside down. people trapped inside. smelling gas. send help fast!!!'",
            height=200
        )
    else:
        uploaded_file = st.file_uploader("Upload scene photo or handwritten note", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            user_image = Image.open(uploaded_file)
            st.image(user_image, caption="Uploaded Evidence", use_container_width=True)
            user_text = st.text_input("Additional context (optional):", placeholder="Any other details?")

    analyze_btn = st.button("🔥 Generate Action Plan", use_container_width=True, type="primary")

with col2:
    st.subheader("📤 Structured Action Response")
    
    if analyze_btn:
        if not API_KEY:
            st.error("🚨 You need to enter your Gemini API Key in the Left Sidebar before you can generate a plan!")
        elif not user_text and not user_image:
            st.error("Please provide either text or an image input.")
        else:
            with st.spinner("Analyzing intelligence with Gemini..."):
                try:
                    client = genai.Client(api_key=API_KEY)
                    # Construct prompt
                    prompt = f"""
                    You are 'Aegis', an advanced emergency response AI. Your task is to analyze the following unstructured, messy intelligence (which may include a photo) and convert it into a structured, immediate action plan for first responders.
                    
                    RESPOND EXACTLY AND ONLY WITH VALID JSON using the format below. Do not use Markdown block tags (like ```json). Just return the raw JSON string.
                    {{
                        "CrisisType": "e.g., Medical, Fire, Collision, Natural Disaster",
                        "SeverityLevel": "e.g., Low, Medium, High, Critical",
                        "Location": "Extracted location from the input (or 'Unknown')",
                        "KeyEntities": ["List of critical factors, e.g., '3 victims', 'Gas leak detected'"],
                        "DispatchRecommendation": "Which departments to dispatch (e.g., 'Fire, EMS, Hazmat')",
                        "ImmediateProtocol": [
                            "Step 1: Secure the perimeter.",
                            "Step 2: Approach vehicle carefully due to gas leak.",
                            "Step 3: Extract victims."
                        ]
                    }}
                    
                    Context provided by user: {user_text}
                    """
                    
                    # Generate content using the new SDK
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
                        
                    # Parse JSON
                    raw_text = response.text.strip()
                    if raw_text.startswith("```json"):
                        raw_text = raw_text[7:]
                    if raw_text.startswith("```"):
                        raw_text = raw_text[3:]
                    if raw_text.endswith("```"):
                        raw_text = raw_text[:-3]
                    raw_text = raw_text.strip()
                    
                    result = json.loads(raw_text)
                    
                    # Display Results
                    st.success("Intelligence successfully structured!")
                    
                    # Metrics row
                    m1, m2, m3 = st.columns(3)
                    
                    severity_color = "#ff4b4b" if result["SeverityLevel"] == "Critical" else ("#ffa500" if result["SeverityLevel"] == "High" else "#00cc00")
                    
                    with m1:
                        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:{severity_color}">{result["SeverityLevel"]}</div><div class="metric-label">Severity</div></div>', unsafe_allow_html=True)
                    with m2:
                        st.markdown(f'<div class="metric-card"><div class="metric-value">{result["CrisisType"]}</div><div class="metric-label">Crisis Type</div></div>', unsafe_allow_html=True)
                    with m3:
                        st.markdown(f'<div class="metric-card"><div class="metric-value">{result["DispatchRecommendation"]}</div><div class="metric-label">Dispatch</div></div>', unsafe_allow_html=True)
                    
                    # Protocol
                    st.markdown("### 📋 Immediate Action Protocol")
                    for step in result["ImmediateProtocol"]:
                        st.info(f"👉 {step}")
                        
                    # Entities & Context
                    st.markdown("### 🔍 Key Extracted Entities")
                    for entity in result["KeyEntities"]:
                        st.write(f"- {entity}")
                    
                    st.markdown("### 📍 Location")
                    st.write(f"**{result['Location']}**")
                    
                except Exception as e:
                    st.error(f"Error analyzing input: {str(e)}")
                    st.write("Raw output for debugging:", response.text if 'response' in locals() else "None")
    else:
        st.info("Awaiting intelligence input. Fill out the left panel and click 'Generate Action Plan'.")
