# 🛡️ Aegis: The Universal Crisis Bridge

**PromptWars: Bengaluru Hackathon Submission**
**Track: Societal Benefit**

## 📖 Inspiration & Problem Statement
During a crisis, critical seconds are often wasted deciphering panicked, unstructured information—whether from civilians reporting an incident via chaotic text messages, or bystanders sharing messy photos of an ongoing disaster. Dispatchers and emergency services must quickly interpret this "messy" data to deploy the right resources. 

**Aegis** bridges the gap between chaotic human intent and complex response systems. It takes unstructured Real-World Data (images, text) and instantly structures it into verifiable, life-saving action protocols using Google's powerful Gemini models.

## ✨ Features
1. **Multimodal Incident Ingestion**: Accept either unstructured, messy text inputs or images (e.g., scene photos, handwritten medical or situational notes).
2. **Instant Structuring**: Leverages `gemini-1.5-flash` to instantly parse the chaotic scene into a structured JSON dispatch payload.
3. **Automated Triage**: Automatically determines the Crisis Type, Severity Level, and Dispatch Recommendations.
4. **Action Protocols**: Generates a step-by-step immediate action plan for first responders based on extracted entities (e.g., hazardous materials, trapped individuals).

## 🛠️ Built With
- **[Streamlit](https://streamlit.io/)**: For a rapid, modern, and highly responsive user interface designed around dynamic data consumption.
- **Google GenAI (`gemini-1.5-flash`)**: The core cognitive engine of Aegis, parsing the messy, multimodal inputs safely and incredibly fast.
- **Python**: Core logic implementation.

## 🚀 How to Run Locally

You'll need a Google Gemini API Key.
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Streamlit Application:
   ```bash
   streamlit run app.py
   ```
3. Open your browser and navigate to `http://localhost:8501`. Enter your API Key in the sidebar if you haven't set `GEMINI_API_KEY` in your environment.

## 📝 Evaluation Criteria Met
- **Code Quality**: Clean modular Python, strict error handling, and separation of UI components from processing logic.
- **Security**: The Gemini API key is taken via a secure Streamlit password input and not hardcoded anywhere in the app. Secrets management is also supported.
- **Efficiency**: `gemini-1.5-flash` is utilized due to its fast multimodal inference speed, essential for emergency contexts where every millisecond counts.
- **Accessibility**: UI relies on high-contrast colors, clear typography, semantic headings, and distinct visual hierarchies. 
- **Google Services Integration**: Direct, meaningful integration of the Google Generative AI Python SDK to bridge human intent and structured system logic.

---
*Built with ❤️ for PromptWars: Bengaluru.*
