# Team 29 — Energentic Hackathon

## Homie App

We built **Homie**, a multi-agent web app for **Problem Statement 3: Utility-Led Agent for Electricity Connection & Solarization**.

### 🏗️ Architecture

| Role | Purpose | Key APIs |
|------|---------|----------|
| **Homie (Coordinator)** | Starts the conversation, delegates tasks, and logs every action. | — |
| **Electricity-Connection Agent** | Collects user details and secures a new electricity connection. | Beckn **Connection** |
| *(Homie action)* | Creates the digital assets for the new connection. | World Engine **Meter** + **Energy Resource** |
| **Solar-Retail Agent** | Guides the user in choosing & buying a rooftop PV system. | Beckn **Solar-Retail** |
| **Solar-Service Agent** | Books installation, permits, and commissioning. | Beckn **Solar-Service** |
| **Subsidy Agent** | Finds and applies every eligible subsidy *after* installation. | Public subsidy portals |

All agents run on `gemini-2.5-flash-preview-04-17`.

### ✨ Key Features

- **Streamlit interface** with live status cards and action logs.  
- **Clean multi-agent orchestration** — every tool call is logged.  
- **Real-time feedback** keeps the user informed at each step.

---

## 👥 Team

| Name | 
|------|
| **Saksham Gupta** |
| **Ruchir Chheda** | 

---

## 🛠️ Tech Stack

- **Google AI Developer Kit (ADK)**
- **Streamlit** for the front end
- **Python** (see `requirements.txt`)
- **Cursor** editor :p

---

## 🚀 Setup Instructions

```bash
# 1 — Clone the repo
git clone https://github.com/<your-org>/team-29-energentic-hackathon.git
cd team-29-energentic-hackathon

# 2 — Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3 — Install dependencies
pip install -r requirements.txt

# 4 — Add your Google API key
export GOOGLE_API_KEY="YOUR_KEY_HERE"     # Windows: set GOOGLE_API_KEY=YOUR_KEY_HERE

# 5 — Run the app
streamlit run app.py
```
## 🎥 Demo Video
Video file: demo/video.mp4 (also uploaded separately).

(Link coming soon.)
## 📚 Challenges & Learnings
Prompt engineering is everything — agent reliability rose and fell with the clarity of every system prompt.

We had initally planned to work on the second problem statement, however the World Engine DER API quirks forced a mid-hackathon pivot from Problem Statement 2 to 3.

Rapid iteration with ADK — once roles were defined, wiring up the UI and logs was fast and fun.

Made with ☕, ⚡, and an unreasonable amount of late-night debugging.
