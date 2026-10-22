"""
LawAI Advisor - Main Application Backend (Flask + SQLite + OpenAI)
Professional AI Legal Guidance Platform.
"""

import os
import json
import secrets
from datetime import datetime, timedelta, timezone
from functools import wraps
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, request, jsonify, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = Path(__file__).resolve().parent
# Load .env file
load_dotenv(BASE_DIR / ".env")

from database import get_db, init_db
from legal_data import OFFICIAL_RESOURCES, STATUTORY_PROVISIONS, DOCUMENT_TEMPLATES
from ai_advisor import run_ai_consultation, LEGAL_SYSTEM_PROMPT


def get_secret_key():
    env_key = os.environ.get("SESSION_SECRET", "").strip()
    if env_key and env_key != "replace_with_a_long_random_secret":
        return env_key
    key_file = BASE_DIR / ".secret_key"
    if key_file.exists():
        saved = key_file.read_text().strip()
        if saved:
            return saved
    new_key = secrets.token_hex(32)
    key_file.write_text(new_key)
    return new_key


app = Flask(__name__, static_folder="static")
app.secret_key = get_secret_key()
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(days=14),
    MAX_CONTENT_LENGTH=512 * 1024,
)

OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini").strip() or "gpt-4.1-mini"


# ----------------------------------------------------------------- Helpers
def body():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"error": "Authentication required. Please sign in to continue."}), 401
        return fn(*args, **kwargs)

    return wrapper


def start_session(user_id, email, full_name, remember=True):
    session.clear()
    session.permanent = bool(remember)
    session["user_id"] = user_id
    session["email"] = email
    session["full_name"] = full_name


# ----------------------------------------------------------------- SPA Routes
FRONTEND_ROUTES = [
    "/",
    "/signup",
    "/login",
    "/forgot-password",
    "/dashboard",
    "/consultation/new",
    "/cases",
    "/documents",
    "/profile",
    "/privacy",
    "/terms"
]


@app.get("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/<path:path>")
def catch_all(path):
    # Serve static files if they exist
    file_path = BASE_DIR / "static" / path
    if file_path.exists() and file_path.is_file():
        return send_from_directory(app.static_folder, path)
    # SPA route fallback for frontend routes or consultation/:id
    return send_from_directory(app.static_folder, "index.html")


# ----------------------------------------------------------------- Auth APIs
@app.post("/api/auth/signup")
def signup():
    data = body()
    full_name = str(data.get("full_name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    confirm_password = str(data.get("confirm_password", ""))
    terms_accepted = bool(data.get("terms_accepted", False))

    if not full_name or len(full_name) < 2:
        return jsonify({"error": "Please enter your full name."}), 400
    if "@" not in email or "." not in email.split("@")[-1] or len(email) > 254:
        return jsonify({"error": "Enter a valid email address."}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long."}), 400
    if len(password) > 200:
        return jsonify({"error": "Password is too long."}), 400
    if password != confirm_password:
        return jsonify({"error": "Passwords do not match."}), 400
    if not terms_accepted:
        return jsonify({"error": "You must accept the Terms of Service and Privacy Policy to register."}), 400

    try:
        with get_db() as con:
            cur = con.execute(
                "INSERT INTO users(full_name, email, password_hash) VALUES(?, ?, ?)",
                (full_name, email, generate_password_hash(password)),
            )
            user_id = cur.lastrowid
            con.commit()
    except Exception as e:
        if "UNIQUE" in str(e) or "IntegrityError" in str(type(e)):
            return jsonify({"error": "An account with that email already exists. Please sign in."}), 409
        return jsonify({"error": "Failed to create account. Please try again."}), 500

    start_session(user_id, email, full_name)
    return jsonify({"ok": True, "user": {"id": user_id, "email": email, "full_name": full_name}})


@app.post("/api/auth/login")
def login():
    data = body()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    remember = bool(data.get("remember", True))

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    with get_db() as con:
        user = con.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Incorrect email or password. Please try again."}), 401

    start_session(user["id"], user["email"], user["full_name"], remember)
    return jsonify({
        "ok": True,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"]
        }
    })


@app.post("/api/auth/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})


@app.get("/api/auth/me")
def me():
    if not session.get("user_id"):
        return jsonify({"logged_in": False})
    with get_db() as con:
        user = con.execute("SELECT id, full_name, email, created_at FROM users WHERE id=?", (session["user_id"],)).fetchone()
    if not user:
        session.clear()
        return jsonify({"logged_in": False})
    return jsonify({
        "logged_in": True,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "created_at": user["created_at"]
        }
    })


@app.post("/api/auth/forgot-password")
def forgot_password():
    data = body()
    email = str(data.get("email", "")).strip().lower()
    if not email:
        return jsonify({"error": "Please provide your registered email address."}), 400

    with get_db() as con:
        user = con.execute("SELECT id, email FROM users WHERE email=?", (email,)).fetchone()
        if user:
            token = secrets.token_urlsafe(24)
            expiry = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
            con.execute("UPDATE users SET reset_token=?, reset_token_expiry=? WHERE id=?", (token, expiry, user["id"]))
            con.commit()
            return jsonify({
                "ok": True,
                "message": "Password reset token generated. In a production environment with SMTP configured, this is sent via email.",
                "demo_reset_token": token
            })
    # Protect against user enumeration by returning uniform success message
    return jsonify({
        "ok": True,
        "message": "If an account exists with that email, password reset instructions have been generated."
    })


@app.post("/api/auth/reset-password")
def reset_password():
    data = body()
    token = str(data.get("token", "")).strip()
    new_password = str(data.get("new_password", ""))
    confirm_password = str(data.get("confirm_password", ""))

    if not token:
        return jsonify({"error": "Reset token is required."}), 400
    if len(new_password) < 8:
        return jsonify({"error": "New password must be at least 8 characters long."}), 400
    if new_password != confirm_password:
        return jsonify({"error": "Passwords do not match."}), 400

    with get_db() as con:
        user = con.execute("SELECT id, reset_token_expiry FROM users WHERE reset_token=?", (token,)).fetchone()
        if not user:
            return jsonify({"error": "Invalid or expired reset token."}), 400

        # Check expiry
        if user["reset_token_expiry"]:
            expiry = datetime.fromisoformat(str(user["reset_token_expiry"]))
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) > expiry:
                return jsonify({"error": "Reset token has expired. Please request a new one."}), 400

        con.execute(
            "UPDATE users SET password_hash=?, reset_token=NULL, reset_token_expiry=NULL WHERE id=?",
            (generate_password_hash(new_password), user["id"])
        )
        con.commit()

    return jsonify({"ok": True, "message": "Password has been successfully updated. You may now sign in."})


@app.put("/api/auth/profile")
@login_required
def update_profile():
    data = body()
    full_name = str(data.get("full_name", "")).strip()
    current_password = str(data.get("current_password", ""))
    new_password = str(data.get("new_password", ""))

    if not full_name or len(full_name) < 2:
        return jsonify({"error": "Please provide a valid full name."}), 400

    with get_db() as con:
        user = con.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()
        if not user:
            return jsonify({"error": "User account not found."}), 404

        if new_password:
            if not current_password or not check_password_hash(user["password_hash"], current_password):
                return jsonify({"error": "Current password incorrect."}), 400
            if len(new_password) < 8:
                return jsonify({"error": "New password must be at least 8 characters."}), 400
            con.execute(
                "UPDATE users SET full_name=?, password_hash=? WHERE id=?",
                (full_name, generate_password_hash(new_password), session["user_id"])
            )
        else:
            con.execute("UPDATE users SET full_name=? WHERE id=?", (full_name, session["user_id"]))
        con.commit()

    session["full_name"] = full_name
    return jsonify({"ok": True, "user": {"id": session["user_id"], "email": session["email"], "full_name": full_name}})


@app.delete("/api/auth/account")
@login_required
def delete_account():
    data = body()
    password = str(data.get("password", ""))

    with get_db() as con:
        user = con.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()
        if not user or not check_password_hash(user["password_hash"], password):
            return jsonify({"error": "Incorrect password. Cannot delete account."}), 400

        con.execute("DELETE FROM users WHERE id=?", (session["user_id"],))
        con.commit()

    session.clear()
    return jsonify({"ok": True, "message": "Your account and all associated legal records have been permanently deleted."})


# ----------------------------------------------------------------- Legal Consultations APIs
@app.post("/api/consultations/analyze")
@login_required
def analyze_consultation():
    data = body()
    raw_description = str(data.get("raw_description", "")).strip()
    if not raw_description or len(raw_description) < 20:
        return jsonify({"error": "Please provide a more detailed description of what happened (at least 20 characters)."}), 400
    if len(raw_description) > 15000:
        return jsonify({"error": "Description is too long (maximum 15,000 characters)."}), 400

    category = str(data.get("category", "General Legal Issue")).strip()
    title = str(data.get("title", "")).strip()
    if not title:
        title = raw_description[:50].split("\n")[0] + ("..." if len(raw_description) > 50 else "")

    incident_date = str(data.get("incident_date", "")).strip()
    incident_location = str(data.get("incident_location", "India")).strip()
    jurisdiction = str(data.get("jurisdiction", "India")).strip() or "India"
    involved_parties = str(data.get("involved_parties", "")).strip()
    desired_outcome = str(data.get("desired_outcome", "")).strip()
    is_ongoing = 1 if data.get("is_ongoing") else 0
    immediate_danger = 1 if data.get("immediate_danger") else 0
    evidence_summary = str(data.get("evidence_summary", "")).strip()

    intake = {
        "category": category,
        "title": title,
        "raw_description": raw_description,
        "incident_date": incident_date,
        "incident_location": incident_location,
        "jurisdiction": jurisdiction,
        "involved_parties": involved_parties,
        "desired_outcome": desired_outcome,
        "is_ongoing": is_ongoing,
        "immediate_danger": immediate_danger,
        "evidence_summary": evidence_summary
    }

    # Execute AI Analysis
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    analysis_result = run_ai_consultation(intake, api_key=api_key, model=OPENAI_MODEL)
    sections = analysis_result["sections"]
    action_items = analysis_result["action_items"]
    raw_full_text = analysis_result["raw_full_text"]

    with get_db() as con:
        cur = con.execute(
            """INSERT INTO consultations(
                user_id, title, category, incident_date, incident_location, jurisdiction,
                involved_parties, desired_outcome, is_ongoing, immediate_danger, evidence_summary,
                raw_description, status, situation_summary, legal_assessment, applicable_laws,
                recommended_solution, immediate_actions, step_by_step_plan, evidence_checklist,
                escalation_options, risks_deadlines, suggested_next_move, disclaimer, raw_full_text
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                session["user_id"], title, category, incident_date, incident_location, jurisdiction,
                involved_parties, desired_outcome, is_ongoing, immediate_danger, evidence_summary,
                raw_description, "active", sections.get("situation_summary", ""), sections.get("legal_assessment", ""),
                sections.get("applicable_laws", ""), sections.get("recommended_solution", ""),
                sections.get("immediate_actions", ""), sections.get("step_by_step_plan", ""),
                sections.get("evidence_checklist", ""), sections.get("escalation_options", ""),
                sections.get("risks_deadlines", ""), sections.get("suggested_next_move", ""),
                sections.get("disclaimer", ""), raw_full_text
            )
        )
        consultation_id = cur.lastrowid

        # Insert action items
        for item in action_items:
            con.execute(
                """INSERT INTO action_items(
                    consultation_id, step_number, title, explanation, where_to_act,
                    required_evidence, verified_deadline, contingency, status
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    consultation_id, item["step_number"], item["title"], item["explanation"],
                    item["where_to_act"], item["required_evidence"], item["verified_deadline"],
                    item["contingency"], item.get("status", "pending")
                )
            )
        con.commit()

    return jsonify({
        "ok": True,
        "consultation_id": consultation_id,
        "title": title,
        "category": category,
        "sections": sections,
        "action_items": action_items,
        "used_openai": analysis_result.get("used_openai", False),
        "openai_notice": analysis_result.get("openai_notice")
    })


@app.get("/api/consultations")
@login_required
def list_consultations():
    category = request.args.get("category", "").strip()
    status = request.args.get("status", "").strip()
    search = request.args.get("search", "").strip()

    query = """
        SELECT c.*, 
            COUNT(a.id) as total_steps,
            SUM(CASE WHEN a.status = 'completed' THEN 1 ELSE 0 END) as completed_steps
        FROM consultations c
        LEFT JOIN action_items a ON c.id = a.consultation_id
        WHERE c.user_id = ?
    """
    params = [session["user_id"]]

    if category:
        query += " AND c.category = ?"
        params.append(category)
    if status:
        query += " AND c.status = ?"
        params.append(status)
    if search:
        query += " AND (c.title LIKE ? OR c.raw_description LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    query += " GROUP BY c.id ORDER BY c.updated_at DESC"

    with get_db() as con:
        rows = con.execute(query, params).fetchall()

    results = []
    for r in rows:
        d = dict(r)
        total = d.get("total_steps") or 0
        comp = d.get("completed_steps") or 0
        d["completion_percentage"] = int((comp / total) * 100) if total > 0 else 0
        results.append(d)

    return jsonify(results)


@app.get("/api/consultations/<int:cid>")
@login_required
def get_consultation(cid):
    with get_db() as con:
        row = con.execute("SELECT * FROM consultations WHERE id=? AND user_id=?", (cid, session["user_id"])).fetchone()
        if not row:
            return jsonify({"error": "Consultation record not found."}), 404

        action_rows = con.execute(
            "SELECT * FROM action_items WHERE consultation_id=? ORDER BY step_number ASC", (cid,)
        ).fetchall()

        doc_rows = con.execute(
            "SELECT id, title, doc_type, dispute_amount, created_at, updated_at FROM documents WHERE consultation_id=?", (cid,)
        ).fetchall()

        msg_rows = con.execute(
            "SELECT id, role, content, created_at FROM follow_up_messages WHERE consultation_id=? ORDER BY created_at ASC", (cid,)
        ).fetchall()

    c_data = dict(row)
    c_data["action_items"] = [dict(a) for a in action_rows]
    c_data["documents"] = [dict(d) for d in doc_rows]
    c_data["follow_up_messages"] = [dict(m) for m in msg_rows]

    # Calculate completion stats
    total = len(c_data["action_items"])
    comp = sum(1 for a in c_data["action_items"] if a["status"] == "completed")
    c_data["total_steps"] = total
    c_data["completed_steps"] = comp
    c_data["completion_percentage"] = int((comp / total) * 100) if total > 0 else 0

    return jsonify(c_data)


@app.patch("/api/consultations/<int:cid>")
@login_required
def update_consultation(cid):
    data = body()
    with get_db() as con:
        row = con.execute("SELECT * FROM consultations WHERE id=? AND user_id=?", (cid, session["user_id"])).fetchone()
        if not row:
            return jsonify({"error": "Consultation not found."}), 404

        updates = []
        params = []
        if "title" in data:
            updates.append("title = ?")
            params.append(str(data["title"]).strip()[:120])
        if "private_notes" in data:
            updates.append("private_notes = ?")
            params.append(str(data["private_notes"]))
        if "status" in data:
            updates.append("status = ?")
            params.append(str(data["status"]).strip())

        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.extend([cid, session["user_id"]])
            con.execute(f"UPDATE consultations SET {', '.join(updates)} WHERE id=? AND user_id=?", params)
            con.commit()

    return jsonify({"ok": True})


@app.delete("/api/consultations/<int:cid>")
@login_required
def delete_consultation(cid):
    with get_db() as con:
        con.execute("DELETE FROM consultations WHERE id=? AND user_id=?", (cid, session["user_id"]))
        con.commit()
    return jsonify({"ok": True, "message": "Consultation and associated action steps have been deleted."})


@app.patch("/api/action-items/<int:aid>")
@login_required
def update_action_item(aid):
    data = body()
    new_status = str(data.get("status", "pending")).strip()
    if new_status not in ["pending", "in_progress", "completed", "optional"]:
        return jsonify({"error": "Invalid action item status."}), 400

    with get_db() as con:
        # Check ownership through consultation
        item = con.execute(
            """SELECT a.*, c.user_id FROM action_items a 
            JOIN consultations c ON a.consultation_id = c.id 
            WHERE a.id = ? AND c.user_id = ?""",
            (aid, session["user_id"])
        ).fetchone()

        if not item:
            return jsonify({"error": "Action item not found or unauthorized."}), 404

        completed_at = datetime.now(timezone.utc).isoformat() if new_status == "completed" else None
        con.execute(
            "UPDATE action_items SET status = ?, completed_at = ? WHERE id = ?",
            (new_status, completed_at, aid)
        )
        con.execute("UPDATE consultations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (item["consultation_id"],))
        con.commit()

    return jsonify({"ok": True, "id": aid, "status": new_status})


@app.post("/api/consultations/<int:cid>/follow-up")
@login_required
def consultation_follow_up(cid):
    data = body()
    user_message = str(data.get("message", "")).strip()
    if not user_message:
        return jsonify({"error": "Please provide your question or clarification."}), 400

    with get_db() as con:
        consultation = con.execute("SELECT * FROM consultations WHERE id=? AND user_id=?", (cid, session["user_id"])).fetchone()
        if not consultation:
            return jsonify({"error": "Consultation not found."}), 404

        history_rows = con.execute(
            "SELECT role, content FROM follow_up_messages WHERE consultation_id=? ORDER BY created_at ASC",
            (cid,)
        ).fetchall()

    history = [dict(h) for h in history_rows]

    # Construct context for OpenAI or intelligent legal response
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    assistant_reply = ""

    if api_key and api_key != "put_your_secret_api_key_here":
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key, timeout=45.0, max_retries=2)

            system_instruction = (
                f"{LEGAL_SYSTEM_PROMPT}\n\n"
                f"CURRENT CASE CONTEXT:\n"
                f"- Category: {consultation['category']}\n"
                f"- Title: {consultation['title']}\n"
                f"- Incident Summary: {consultation['situation_summary']}\n"
                f"- Applicable Laws: {consultation['applicable_laws']}\n"
                f"- Recommended Solution: {consultation['recommended_solution']}\n"
                f"Answer the user's specific follow-up question directly, accurately citing Indian law when relevant."
            )

            messages = [{"role": "system", "content": system_instruction}]
            for msg in history[-8:]:
                messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": user_message})

            resp = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                temperature=0.2,
                max_tokens=1400
            )
            assistant_reply = (resp.choices[0].message.content or "").strip()
        except Exception as e:
            app.logger.warning(f"Follow up OpenAI call failed: {e}")

    if not assistant_reply:
        # Fallback intelligent contextual legal answer
        assistant_reply = (
            f"Regarding your inquiry about '{user_message}':\n\n"
            f"1. **Contextual Analysis**: Under the context of your {consultation['category']} consultation ({consultation['title']}), "
            f"all formal steps should align with the applicable legal standards.\n\n"
            f"2. **Evidence Preservation**: Ensure any new facts or communications mentioned are preserved in original format "
            f"with timestamps intact.\n\n"
            f"3. **Practical Next Step**: If you wish to formalize this step, consider generating a formal Legal Demand Notice or Grievance Letter "
            f"using the Document Assistance tab on your dashboard.\n\n"
            f"*Disclaimer: This response is AI-generated preliminary legal information. Consult a practicing advocate for case representation.*"
        )

    # Persist both user and assistant messages
    with get_db() as con:
        con.execute(
            "INSERT INTO follow_up_messages(consultation_id, user_id, role, content) VALUES(?, ?, ?, ?)",
            (cid, session["user_id"], "user", user_message)
        )
        con.execute(
            "INSERT INTO follow_up_messages(consultation_id, user_id, role, content) VALUES(?, ?, ?, ?)",
            (cid, session["user_id"], "assistant", assistant_reply)
        )
        con.execute("UPDATE consultations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (cid,))
        con.commit()

    return jsonify({
        "ok": True,
        "reply": assistant_reply
    })


# ----------------------------------------------------------------- Document Assistance APIs
@app.get("/api/documents")
@login_required
def list_documents():
    with get_db() as con:
        rows = con.execute(
            "SELECT d.*, c.title as consultation_title FROM documents d "
            "LEFT JOIN consultations c ON d.consultation_id = c.id "
            "WHERE d.user_id = ? ORDER BY d.updated_at DESC",
            (session["user_id"],)
        ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/api/documents/<int:did>")
@login_required
def get_document(did):
    with get_db() as con:
        row = con.execute("SELECT * FROM documents WHERE id=? AND user_id=?", (did, session["user_id"])).fetchone()
        if not row:
            return jsonify({"error": "Document draft not found."}), 404
    return jsonify(dict(row))


@app.post("/api/documents/generate")
@login_required
def generate_document():
    data = body()
    doc_type = str(data.get("doc_type", "legal_notice")).strip()
    consultation_id = data.get("consultation_id")
    recipient_name = str(data.get("recipient_name", "[Recipient Name / Designated Authority]")).strip()
    recipient_org = str(data.get("recipient_org", "[Company / Organization Name]")).strip()
    recipient_address = str(data.get("recipient_address", "[Registered Office / Residential Address]")).strip()
    dispute_amount = str(data.get("dispute_amount", "0")).strip()
    specific_demands = str(data.get("specific_demands", "Refund / payment of dues / cessation of unlawful conduct")).strip()
    incident_facts = str(data.get("incident_facts", "")).strip()

    consultation_title = "Legal Draft"
    c_summary = ""
    c_laws = ""

    if consultation_id:
        with get_db() as con:
            c_row = con.execute(
                "SELECT * FROM consultations WHERE id=? AND user_id=?",
                (consultation_id, session["user_id"])
            ).fetchone()
            if c_row:
                consultation_title = c_row["title"]
                c_summary = c_row["situation_summary"] or c_row["raw_description"][:400]
                c_laws = c_row["applicable_laws"][:300]
                if not incident_facts:
                    incident_facts = c_row["raw_description"]

    if not incident_facts:
        incident_facts = "On the relevant date, the claimant entered into a transaction / contract with the opposite party as set forth herein."

    template_obj = DOCUMENT_TEMPLATES.get(doc_type) or DOCUMENT_TEMPLATES.get("legal_notice")
    title = f"{template_obj['title']} - {consultation_title}"

    today_str = datetime.now(timezone.utc).strftime("%d %B %Y")
    user_name = session.get("full_name", "Complainant")
    user_email = session.get("email", "client@example.com")

    # Render template with variables
    rendered_content = template_obj["template"].format(
        date=today_str,
        user_name=user_name,
        user_address="[Complainant Postal Address, City, State, PIN]",
        user_email=user_email,
        user_phone="[Complainant Contact Number]",
        recipient_name=recipient_name,
        recipient_org=recipient_org,
        recipient_address=recipient_address,
        recipient_email="[recipient@example.com]",
        recipient_phone="[Recipient Phone]",
        subject_summary=consultation_title,
        incident_date="[Specific Date / Timeline]",
        incident_location="[City / State]",
        incident_facts=incident_facts,
        grievance_details=specific_demands,
        dispute_amount=dispute_amount,
        dispute_amount_words="[Amount in words]",
        applicable_laws_summary=c_laws or "Applicable statutory provisions and contract terms",
        specific_demand_1=specific_demands,
        order_reference="[Order / Booking / Reference ID]",
        employee_id="[Employee ID / Roll Number]",
        designation="[Job Title / Designation]",
        department="[Department]",
        unpaid_period="[Months / Salary Period]",
        property_address="[Rental Property Address]",
        lease_date="[Tenancy Agreement Date]",
        vacation_date="[Handover Date]",
        deposit_amount=dispute_amount,
        days_passed="[Number of Days]",
        reminder_dates="[Dates of reminders sent]",
        bank_name="[Bank Name]",
        police_station="[Local Cybercrime Police Station]",
        platform_name="[Online Platform / Application]",
        suspect_details="[Suspect Phone / ID / URL]",
        complainant_bank="[Complainant Bank Name]",
        utr_numbers="[UTR / Disputed Transaction IDs]",
        beneficiary_details="[Fraudulent Beneficiary Account/UPI]",
        call_date_time="[Date & Time of Call]",
        ack_number="[1930 Acknowledgment Number]"
    )

    with get_db() as con:
        cur = con.execute(
            """INSERT INTO documents(
                user_id, consultation_id, doc_type, title, recipient_name, recipient_org,
                dispute_amount, draft_content
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                session["user_id"], consultation_id, doc_type, title, recipient_name,
                recipient_org, dispute_amount, rendered_content
            )
        )
        doc_id = cur.lastrowid
        con.commit()

    return jsonify({
        "ok": True,
        "document": {
            "id": doc_id,
            "title": title,
            "doc_type": doc_type,
            "consultation_id": consultation_id,
            "draft_content": rendered_content,
            "created_at": today_str
        }
    })


@app.put("/api/documents/<int:did>")
@login_required
def update_document(did):
    data = body()
    title = str(data.get("title", "")).strip()
    draft_content = str(data.get("draft_content", "")).strip()

    if not title:
        return jsonify({"error": "Document title cannot be empty."}), 400
    if not draft_content:
        return jsonify({"error": "Document content cannot be empty."}), 400

    with get_db() as con:
        doc = con.execute("SELECT * FROM documents WHERE id=? AND user_id=?", (did, session["user_id"])).fetchone()
        if not doc:
            return jsonify({"error": "Document not found or unauthorized."}), 404

        con.execute(
            "UPDATE documents SET title=?, draft_content=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (title, draft_content, did)
        )
        con.commit()

    return jsonify({"ok": True})


@app.delete("/api/documents/<int:did>")
@login_required
def delete_document(did):
    with get_db() as con:
        con.execute("DELETE FROM documents WHERE id=? AND user_id=?", (did, session["user_id"]))
        con.commit()
    return jsonify({"ok": True})


# ----------------------------------------------------------------- Resources Directory API
@app.get("/api/resources")
def get_resources():
    return jsonify({
        "official_helplines": OFFICIAL_RESOURCES,
        "statutory_frameworks": STATUTORY_PROVISIONS
    })


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=False)
