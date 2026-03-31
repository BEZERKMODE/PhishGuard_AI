<p align="center">
  <img src="https://via.placeholder.com/1200x300/0f172a/22c55e?text=PhishGuard+AI+-+Intelligent+Phishing+Detection+System" alt="PhishGuard AI Banner"/>
</p>

# 🛡️ PhishGuard AI – Intelligent Phishing Detection System

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![ML](https://img.shields.io/badge/Machine%20Learning-XGBoost-orange)

---

## ⚡ Recruiter Snapshot

PhishGuard AI is a production-style phishing detection system that combines machine learning, backend APIs, and an interactive frontend to simulate real-world cybersecurity workflows.

Key highlights:

* Designed like a real security tool, not just a model notebook
* Demonstrates end-to-end ML deployment (training → API → UI)
* Built with technologies used in modern security engineering environments
* Portfolio-ready project aligned with SOC, detection engineering, and threat analysis roles

---

## 🚀 Overview

Phishing attacks remain one of the most common entry points for cyber threats. PhishGuard AI analyzes suspicious URLs and classifies them as **legitimate** or **phishing** using a machine learning pipeline.

---

## 📸 Application Preview

### 🔹 Dashboard

![Dashboard](assets/dashboard.png)

### 🔹 Detection Result

![Result](assets/result.png)

### 🔹 API Documentation

![API](assets/api.png)

---

## 🧠 Key Features

* Phishing URL Detection using ML (Random Forest / XGBoost)
* Feature Engineering Pipeline
* FastAPI Backend for real-time prediction
* Streamlit Frontend for analysis
* Risk Scoring (Low / Medium / High / Critical)
* Clean full-stack architecture

---

## 🏗️ System Architecture

```
User Input (URL)
        ↓
Frontend (Streamlit)
        ↓
Backend API (FastAPI)
        ↓
Feature Extraction
        ↓
ML Model
        ↓
Prediction + Risk Score
        ↓
UI Output
```

---

## 🧪 Tech Stack

Frontend: Streamlit
Backend: FastAPI
ML: Scikit-learn, XGBoost
Data: Pandas, NumPy
Deployment: Docker

---

## ⚡ Setup

```
git clone https://github.com/your-username/PhishGuard_AI.git
cd PhishGuard_AI

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

---

## ▶️ Run

Backend:

```
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8001
```

Frontend:

```
streamlit run frontend/streamlit_app.py
```

---

## 🌐 Access

Frontend:
http://localhost:8501

Backend:
http://127.0.0.1:8001/docs

---

## 🏆 Project Impact

PhishGuard AI bridges the gap between machine learning models and real-world cybersecurity applications.

It demonstrates:

* deployable ML systems
* real-time detection workflows
* full-stack integration

Relevant for:

* SOC roles
* Detection engineering
* Threat analysis
* Cybersecurity internships

---

## 👨‍💻 Author

Suraj Bartwal
Cybersecurity | ML | Detection Engineering

---

## 📜 License

MIT License
