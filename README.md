# LawAI Advisor — Professional AI Legal Guidance Platform

> **"Understand Your Rights. Know Your Next Step."**

LawAI Advisor is a complete, functional, professional web application designed to help users understand complex legal problems, identify applicable statutory provisions (with verified references in India), evaluate lawful solutions, and execute prioritized step-by-step action plans following an incident.

---

## 1. Core Mission & Five Essential Questions

LawAI Advisor answers the five essential questions every person faces after a legal incident:

1. **What legal issue might I be facing?** — Neutral incident classification (Civil, Consumer, Labour, Cybercrime, Property, Criminal).
2. **Which laws or legal provisions may apply?** — Authoritative Indian statutes (Bharatiya Nyaya Sanhita 2023, Bharatiya Nagarik Suraksha Sanhita 2023, Information Technology Act 2000, Consumer Protection Act 2019, Model Tenancy regulations, etc.).
3. **What are my possible solutions and legal options?** — Comparative evaluation of informal notices, government conciliation, arbitration, and court proceedings.
4. **What should I do immediately, and what should I do next?** — Interactive action plan checklist with deadlines and fallback steps.
5. **What evidence, documents, or professional assistance might I need?** — Evidence preservation guidelines and automated legal notice/grievance drafts.

---

## 2. Key Architecture & Features

### Frontend (SPA & Design System)
- **Design Language**: Deep Navy (`#0b132b`, `#1c2541`), Slate (`#334155`), Teal accents (`#0d9488`), and accessible contrast.
- **Responsive Layout**: Desktop, tablet, and mobile-friendly layouts with collapsible navigation drawers.
- **Client-Side Routing**: Supports full browser history (`/`, `/signup`, `/login`, `/dashboard`, `/consultation/new`, `/consultation/:id`, `/cases`, `/documents`, `/profile`, `/privacy`, `/terms`).
- **Interactive Action Plan**: Interactive status tracking for individual action steps (Pending, In Progress, Completed, Optional) with real-time percentage progress bars.
- **Print & PDF Export**: Dedicated `@media print` stylesheet for generating formatted legal consultation reports.

### Backend (Python & Flask)
- **API Engine**: Flask with RESTful JSON endpoints.
- **Authentication & Security**: Scrypt/PBKDF2 password hashing via `werkzeug.security`, HttpOnly SameSite session cookies, user-level data isolation, and input sanitization.
- **Legal Knowledge Engine**: Authoritative mapping of Indian statutes, limitation periods, official dispute resolution portals, and emergency hotlines (112, 1930, 1915, 15100).
- **Document Drafting Studio**: Automated templating for Legal Demand Notices, Consumer Grievance Letters, Workplace Salary Demands, Landlord Deposit Notices, and Cybercrime Police Complaints.
- **OpenAI Integration**: Backend-only API key handling with model fallback and expert rule-based legal guidance when the API key is not configured.

---

## 3. Directory Structure

```
LawAI_Advisor/
│
├── app.py                  # Main Flask API backend and SPA route server
├── ai_advisor.py           # Core AI Legal Guidance Engine (11-section parser & statutory generator)
├── database.py             # SQLite database layer, schema migrations, and helper methods
├── legal_data.py           # Verified Indian statutes, official helplines, and document templates
├── requirements.txt        # Python dependency manifest
├── .env.example            # Environment variable template
├── .env                    # Local environment secrets (not committed to VCS)
├── lawai.db                # SQLite database (auto-created on startup)
│
├── static/
│   ├── index.html          # Semantic HTML shell containing all views, forms, and modals
│   ├── style.css           # Professional legal-tech design system and print stylesheets
│   └── app.js              # Client-side router, state store, and UI controllers
│
└── tests/
    └── test_lawai.py       # Comprehensive pytest test suite (Auth, Analysis, Actions, Isolation)
```

---

## 4. Setup & Installation Guide

### Windows (PowerShell)

1. **Verify Python 3.10+**:
   ```powershell
   python --version
   ```

2. **Create and Activate Virtual Environment (Recommended)**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   *(If script execution is disabled on PowerShell, run `Set-ExecutionPolicy -Scope Process Bypass` and activate again).*

3. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and configure your keys:
   ```powershell
   Copy-Item .env.example .env
   notepad .env
   ```

5. **Start Application**:
   ```powershell
   python app.py
   ```
   The platform will be live at: **`http://127.0.0.1:5000`**

---

### macOS / Linux

1. **Setup & Installation**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   nano .env
   python3 app.py
   ```

---

## 5. Environment Variables (`.env`)

| Variable | Default | Description |
| :--- | :--- | :--- |
| `OPENAI_API_KEY` | *(None)* | Your secret OpenAI API key (`sk-...`). When unset, the application automatically uses the verified Indian statutory rules engine. |
| `OPENAI_MODEL` | `gpt-4.1-mini` | Configurable OpenAI model identifier. |
| `SESSION_SECRET` | Auto-generated | Cryptographic secret for signing session cookies. |
| `PORT` | `5000` | Port on which the Flask server listens. |
| `LAWAI_DB` | `lawai.db` | Optional custom file path for the SQLite database. |

---

## 6. Running Automated Tests

Run the full automated test suite using `pytest`:

```powershell
python -m pytest -v
```

### Verified Test Coverage:
- `test_signup_validation`: Enforces email format, password length (>= 8 chars), confirm password match, and terms acceptance.
- `test_signup_and_login_flow`: Verifies registration, duplicate email rejection, session storage, and login authentication.
- `test_password_recovery_token`: Validates secure password reset token generation and credential update.
- `test_expert_guidance_structure`: Verifies presence and parsing of all 11 required sections (A through K).
- `test_emergency_alert_in_guidance`: Verifies immediate physical danger trigger and 112 emergency routing.
- `test_consultation_creation_and_action_item_update`: Tests intake form submission, action item creation, and status progression toggling.
- `test_document_drafting`: Validates pre-filled legal notice generation, editing, and updating.
- `test_cross_user_isolation`: Confirms strict authorization so users cannot view or delete another person's case records.

---

## 7. Official Indian Helplines Directory

- **National Emergency Response Support System**: Dial **112** (Police, Ambulance, Fire)
- **Citizen Financial Cyber Fraud Reporting System**: Dial **1930** / [cybercrime.gov.in](https://cybercrime.gov.in)
- **National Consumer Helpline (NCH)**: Dial **1915** / [consumerhelpline.gov.in](https://consumerhelpline.gov.in)
- **National Legal Services Authority (Free Legal Aid)**: Dial **15100** / [nalsa.gov.in](https://nalsa.gov.in)
- **e-Daakhil Online Consumer Commission Filing**: [edaakhil.nic.in](https://edaakhil.nic.in)

---

## 8. Legal Disclaimer

LawAI Advisor provides artificial intelligence-powered legal information and preliminary guidance for educational and planning purposes. It does not provide formal legal representation, practice law, or create an advocate-client relationship. Prior to taking irreversible legal steps or issuing formal notices, consult a licensed advocate registered with the Bar Council of India.
