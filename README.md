# CloudCanary 🐤

Decoy Cloud Credential Trap & Real-Time Breach Alert System

## 🎯 What is CloudCanary?

CloudCanary plants fake AWS credentials (canary tokens) in public places. When attackers use them, we detect in real-time, enrich with threat intel, and visualize on a live dashboard.

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Cloud | AWS (CloudTrail, EventBridge, Lambda, SNS) |
| Backend | Python + FastAPI |
| Database | PostgreSQL (Supabase) |
| Frontend | React + Vite + Tailwind |
| Alerts | Telegram Bot |
| Threat Intel | IPinfo, AbuseIPDB |
| Hosting | Render + Vercel + AWS |

## 📦 Build Progress

- [x] Part 1: Project Setup + AWS Foundation
- [ ] Part 2: Honeytoken Creation
- [ ] Part 3: Trap Monitoring (CloudTrail + EventBridge + Lambda)
- [ ] Part 4: Backend API + Threat Intel
- [ ] Part 5: Database Design
- [ ] Part 6: Live Dashboard
- [ ] Part 7: Alert System
- [ ] Part 8: External Device + Demo + Docs

## 🔐 Security Note

## 🌐 Live Links

- **Frontend Dashboard:** https://cloudcanary.vercel.app
- **Backend API:** https://cloudcanary.onrender.com
- **API Docs (Swagger):** https://cloudcanary.onrender.com/docs]

## 🏗️ How It Works?
Attacker uses fake AWS key
↓
AWS CloudTrail logs the API call
↓
EventBridge rule detects "canary-*" user
↓
Lambda function fires
↓
Sends event to backend API (Render)
↓
Enriches with IPinfo + AbuseIPDB
↓
Stores in Supabase PostgreSQL
↓
Live Dashboard (Vercel) + Telegram Alert

## 📄 License
         for educational purpose

Educational project 
