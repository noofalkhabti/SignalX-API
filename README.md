# SignalX – Saudi Delivery Signal Intelligence

SignalX is an intelligent data platform designed to analyze and estimate delivery workforce activity across major Saudi cities using non-traditional data sources.

## 🚀 Overview

The platform integrates multiple data streams such as:

* Google Trends indicators
* Application activity signals
* Geo-spatial mobility data

These sources are processed to generate real-time estimations of:

* Active delivery vehicles 🚗
* Delivery motorcycles 🏍️
* Workforce distribution across cities
* Demand intensity and activity patterns

## 📊 Key Features

* Multi-city live dashboard (Riyadh, Jeddah, Dammam)
* Real-time vehicle movement simulation
* Heatmap visualization for demand density
* Time-based activity analysis (Morning / Evening / Night)
* Scenario-based simulation (Rush Hour, Low Activity, Peak Demand)
* AI-driven recommendation engine

## 🔐 Privacy by Design

SignalX operates with:

* No personally identifiable information (No PII)
* Aggregated data only
* Ethical AI principles

## ⚙️ API Endpoints

### Dashboard Data

```bash
/api/dashboard?city=riyadh
```

### Live Vehicles

```bash
/api/live-vehicles?city=riyadh
```

## 🛠️ Tech Stack

* FastAPI (Backend)
* Python (Data Processing)
* Pandas (Data Analysis)
* OpenStreetMap + Leaflet (Visualization)
* JavaScript (Frontend Dashboard)

## 🌍 Vision

SignalX aims to bridge the gap between official statistics and real-world activity in the gig economy by leveraging alternative data sources.

---

Developed as an innovation project for intelligent urban mobility analysis.
