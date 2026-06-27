# PhishGuard AI

![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688)
![Streamlit](https://img.shields.io/badge/frontend-Streamlit-red)

End-to-end phishing detection system using machine learning, FastAPI, and Streamlit with real-time URL analysis and risk scoring.

---

## Overview

PhishGuard AI analyzes URLs in real time and classifies them as phishing or legitimate using a trained machine learning model. It provides risk scoring, feature extraction, and a live dashboard for monitoring results.

---

## Demo

![Demo Screenshot](docs/screenshot.png)
<!-- Replace with actual screenshot or GIF -->

---

## Key Features

- Real-time URL phishing detection
- ML-based classification with risk scoring
- FastAPI backend with REST endpoints
- Streamlit frontend dashboard
- Dockerized deployment (API + UI)
- Modular ML pipeline (train, evaluate, predict)

---

## Project Structure

PhishGuard_AI/
│
├── app.py / main entry
├── backend/         # FastAPI app
├── frontend/        # Streamlit UI
├── ml/              # Model training and prediction
├── models/          # Saved ML models
├── data/raw/        # Raw datasets
├── tests/           # Unit tests
├── Dockerfile.api
├── Dockerfile.ui
├── docker-compose.yml
└── requirements.txt

---

## Installation

git clone https://github.com/BEZERKMODE/PhishGuard_AI.git
cd PhishGuard_AI
pip install -r requirements.txt

---

## Usage

### Run with Docker
docker-compose up --build

### Run manually
uvicorn backend.main:app --reload
streamlit run frontend/app.py

---

## Disclaimer

This tool is intended for educational purposes and authorized testing only. Do not use on systems without permission.

---

## Author

Suraj Bartwal
B.Tech Computer Science (Cybersecurity)

---

## License

MIT License - See LICENSE file for details.
