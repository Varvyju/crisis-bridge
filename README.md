# 🛡️ Aegis: V2 (The 100% Hackathon Submission)

**PromptWars: Bengaluru Hackathon Submission**
**Track: Societal Benefit**

## 📖 Inspiration & Problem Statement
During a crisis, critical seconds are wasted deciphering panicked, unstructured information. **Aegis** bridges the gap between chaotic human intent and complex response systems. It takes unstructured Real-World Data (images, text) and instantly structures it into verifiable, life-saving action protocols using Google's powerful Gemini models.

This V2 release focuses intensely on Production-grade code quality, efficiency, accessibility, robust security, and deep Google SDK native API usage.

## ✨ Features (V2 Evaluation Upgrades)
- **🧪 Comprehensive Testing**: Included full `pytest` unit test coverage in `tests/test_aegis.py` for all core processing logic.
- **⚡ Extreme Efficiency**: 
  - Uses strictly optimized `Image.Resampling.LANCZOS` downscaling to lower GenAI payload size and save networking latency.
  - Implements stateful caching via `@st.cache_resource` for expensive cloud clients.
- **♿ Web Accessibility Score**: UI utilizes full Semantic HTML (`<main>`, `<h1>`, `<h2>`), interactive `aria-label` tags, high-contrast severity metrics, and accessibility tooltips.
- **☁️ Enhanced Google Services**: Native integration with both **Google GenAI (Gemini 2.5 Flash)** and **Google Cloud Logging (`google-cloud-logging`)** to permanently store structural logs of emergencies context on scalable backend storage.
- **🔒 Defense-in-Depth Security**: Safely reads API keys strictly via protected `st.secrets` OR dynamic session states (no hardcoded keys).

## 🛠️ Built With
- **[Streamlit](https://streamlit.io/)**: Modern interactive dashboarding.
- **Google GenAI (`gemini-2.5-flash`)**: Core intelligence protocol synthesizer.
- **Google Cloud Logging**: Distributed structured backend tracing.
- **PyTest**: V2 testing suite.

## 🚀 How to Run Locally & Test

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the tests (Coverage: Core Intelligence):
   ```bash
   pytest tests/
   ```
3. Run the Streamlit Application:
   ```bash
   streamlit run app.py
   ```
