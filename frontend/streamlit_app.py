import os
import requests
import streamlit as st
from urllib.parse import urlparse

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="PhishGuard AI",
    page_icon="🛡️",
    layout="wide",
)

# --------------------------------------------------
# Config
# --------------------------------------------------
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8001")
PREDICT_URL = f"{API_BASE_URL}/predict"
TIMEOUT_SECONDS = 20

# --------------------------------------------------
# Styling
# --------------------------------------------------
st.markdown(
    """
    <style>
        .main {
            padding-top: 1rem;
        }
        .hero-box {
            padding: 1.5rem;
            border: 1px solid #2a2a2a;
            border-radius: 16px;
            background: linear-gradient(135deg, #0f172a, #111827);
            color: white;
            margin-bottom: 1rem;
        }
        .metric-card {
            padding: 1rem;
            border-radius: 14px;
            border: 1px solid #2a2a2a;
            background: #111827;
        }
        .safe-box {
            padding: 1rem;
            border-radius: 12px;
            background: rgba(34, 197, 94, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.35);
        }
        .phish-box {
            padding: 1rem;
            border-radius: 12px;
            background: rgba(239, 68, 68, 0.12);
            border: 1px solid rgba(239, 68, 68, 0.35);
        }
        .neutral-box {
            padding: 1rem;
            border-radius: 12px;
            background: rgba(59, 130, 246, 0.10);
            border: 1px solid rgba(59, 130, 246, 0.30);
        }
        .small-label {
            font-size: 0.85rem;
            opacity: 0.8;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Helpers
# --------------------------------------------------
def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url.strip())
        return bool(parsed.scheme and parsed.netloc)
    except Exception:
        return False


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def extract_domain(url: str) -> str:
    try:
        return urlparse(url).netloc
    except Exception:
        return "Unknown"


def risk_label(score: float, is_phishing: bool) -> str:
    if is_phishing:
        if score >= 0.9:
            return "Critical"
        if score >= 0.75:
            return "High"
        return "Medium"
    return "Low"


def parse_response(data: dict) -> dict:
    """
    Handles multiple possible backend response formats gracefully.
    """
    prediction = data.get("prediction", data.get("label", "Unknown"))
    probability = (
        data.get("phishing_probability")
        or data.get("probability")
        or data.get("confidence")
        or data.get("score")
        or 0.0
    )

    try:
        probability = float(probability)
    except Exception:
        probability = 0.0

    is_phishing = False
    pred_str = str(prediction).strip().lower()

    if pred_str in {"phishing", "malicious", "1", "true", "yes"}:
        is_phishing = True
    elif isinstance(prediction, (int, float)) and int(prediction) == 1:
        is_phishing = True

    features = data.get("features", {})
    model_name = data.get("model_name", "PhishGuard AI Classifier")

    return {
        "prediction": "Phishing" if is_phishing else "Legitimate",
        "is_phishing": is_phishing,
        "probability": probability,
        "risk": risk_label(probability, is_phishing),
        "features": features if isinstance(features, dict) else {},
        "model_name": model_name,
        "raw": data,
    }


def call_api(url: str) -> dict:
    payload = {"url": url}
    response = requests.post(PREDICT_URL, json=payload, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.title("PhishGuard AI")
    st.caption("Intelligent Phishing Detection System")

    st.markdown("### System")
    st.write(f"**API Base URL:** `{API_BASE_URL}`")
    st.write(f"**Predict Endpoint:** `{PREDICT_URL}`")

    st.markdown("### What this project demonstrates")
    st.markdown(
        """
- Machine learning–based phishing URL classification  
- FastAPI backend and Streamlit frontend integration  
- Security-focused application design for portfolio and internship showcases  
        """
    )

    st.markdown("### Suggested test URLs")
    st.code("https://www.google.com")
    st.code("http://secure-login-paypal.verify-account-example.com")

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(
    """
    <div class="hero-box">
        <h1 style="margin-bottom: 0.4rem;">PhishGuard AI</h1>
        <p style="font-size: 1.05rem; margin-bottom: 0.75rem;">
            End-to-end phishing detection platform for analyzing suspicious URLs with
            machine learning, backend inference, and an interactive security dashboard.
        </p>
        <p style="margin: 0;">
            This interface is designed to present the project as a polished, portfolio-ready
            cybersecurity application rather than a basic demo page.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Main Input Section
# --------------------------------------------------
left, right = st.columns([2, 1])

with left:
    st.subheader("Analyze URL")
    user_url = st.text_input(
        "Enter a URL to inspect",
        placeholder="https://example.com/login",
    )

with right:
    st.subheader("Quick Actions")
    analyze_clicked = st.button("Run Analysis", use_container_width=True)
    clear_clicked = st.button("Clear", use_container_width=True)

if clear_clicked:
    st.rerun()

# --------------------------------------------------
# Overview Section
# --------------------------------------------------
st.markdown("### Professional Summary")
st.markdown(
    """
PhishGuard AI evaluates suspicious links using engineered URL-based indicators and a trained
machine learning classifier. The application demonstrates how a detection model can be integrated
into a real security workflow through an API backend and an analyst-friendly frontend.
"""
)

# --------------------------------------------------
# Analysis Flow
# --------------------------------------------------
if analyze_clicked:
    if not user_url.strip():
        st.warning("Please enter a URL before running analysis.")
        st.stop()

    normalized_url = normalize_url(user_url)

    if not is_valid_url(normalized_url):
        st.error("Please enter a valid URL. Example: https://example.com")
        st.stop()

    with st.spinner("Submitting URL for analysis..."):
        try:
            response_data = call_api(normalized_url)
            result = parse_response(response_data)

            domain = extract_domain(normalized_url)
            confidence_pct = round(result["probability"] * 100, 2)

            st.markdown("## Analysis Results")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Verdict", result["prediction"])
            col2.metric("Risk Level", result["risk"])
            col3.metric("Confidence", f"{confidence_pct}%")
            col4.metric("Domain", domain)

            if result["is_phishing"]:
                st.markdown(
                    f"""
                    <div class="phish-box">
                        <h3 style="margin-top: 0;">Threat Assessment: {result["risk"]}</h3>
                        <p>
                            This URL was classified as <strong>potentially malicious</strong>.
                            Treat the link as suspicious until verified through trusted channels.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <div class="safe-box">
                        <h3 style="margin-top: 0;">Threat Assessment: Low</h3>
                        <p>
                            This URL was classified as <strong>likely legitimate</strong>.
                            That said, safe classifications should still be interpreted with context.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("### Detection Details")

            info1, info2 = st.columns(2)
            with info1:
                st.markdown(
                    f"""
                    <div class="neutral-box">
                        <div class="small-label">Analyzed URL</div>
                        <div style="margin-top: 0.35rem; word-break: break-all;">
                            {normalized_url}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with info2:
                st.markdown(
                    f"""
                    <div class="neutral-box">
                        <div class="small-label">Model</div>
                        <div style="margin-top: 0.35rem;">
                            {result["model_name"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            if result["features"]:
                st.markdown("### Engineered Feature Signals")
                feature_rows = []
                for key, value in result["features"].items():
                    feature_rows.append(
                        {
                            "Feature": str(key).replace("_", " ").title(),
                            "Value": value,
                        }
                    )
                st.dataframe(feature_rows, use_container_width=True)

            with st.expander("Raw API Response"):
                st.json(result["raw"])

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to the backend API. Make sure FastAPI is running on "
                "`http://127.0.0.1:8001`."
            )
        except requests.exceptions.Timeout:
            st.error("The API request timed out. Please try again.")
        except requests.exceptions.HTTPError as exc:
            st.error(f"API returned an error: {exc}")
        except Exception as exc:
            st.error(f"Unexpected error: {exc}")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.caption(
    "PhishGuard AI | Cybersecurity Portfolio Project | Streamlit Frontend + FastAPI Backend + ML Inference"
)