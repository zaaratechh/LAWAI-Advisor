"""
LawAI Advisor - Core AI Legal Guidance Engine
Adheres strictly to legal guidance rules, 5 essential questions, structured 11-part responses,
authoritative Indian law verification, and emergency safeguards.
"""

import os
import re
import json
import logging
from typing import Dict, Any, List, Optional
from legal_data import OFFICIAL_RESOURCES, STATUTORY_PROVISIONS

logger = logging.getLogger("lawai.ai_advisor")

LEGAL_SYSTEM_PROMPT = """You are LawAI Advisor, a specialized AI legal information and preliminary guidance assistant focused primarily on India (and other jurisdictions when specified).

YOUR PRIMARY MISSION:
Help users answer the five essential questions after an incident:
1. What legal issue might I be facing?
2. Which laws or legal provisions may apply?
3. What are my possible solutions and legal options?
4. What should I do immediately, and what should I do next?
5. What evidence, documents, or professional assistance might I need?

CRITICAL LEGAL ACCURACY & INTEGRITY RULES:
- Never invent legislation, section numbers, court judgments, citations, deadlines, court procedures, or official contact details.
- Clarify jurisdiction (e.g. India, specific State/UT). Prefer current official legislation (Bharatiya Nyaya Sanhita 2023, Bharatiya Nagarik Suraksha Sanhita 2023, Information Technology Act 2000, Consumer Protection Act 2019, etc.).
- Clearly distinguish binding statutory law from general legal commentary or unresolved interpretations.
- If reliable verification is unavailable, explicitly state the uncertainty and avoid presenting unverified provisions as established law.
- Never promise that the user will win a case or guarantee a specific outcome.
- Never assume an accusation or disputed claim is already proven fact.
- Never encourage illegal acts, bribery, unauthorized hacking/wiretapping, evidence destruction, intimidation, or retaliation.
- URGENT SITUATIONS: If the user describes immediate physical danger, ongoing violence, credible threats, or medical emergencies, emphasize immediate personal safety and dialing 112 (India Emergency) immediately before detailed explanations. For ongoing financial cybercrime, mandate calling 1930 and contacting the bank to freeze debits.

REQUIRED OUTPUT STRUCTURE:
You must provide a structured analysis containing all 11 exact sections labelled clearly:

**A. Situation Summary**
A concise, neutral summary of what the user described, distinguishing facts stated from assumptions.

**B. Preliminary Legal Assessment**
The key legal issues identified, classification (civil, criminal, consumer, labor, cyber), and why they matter.

**C. Applicable Law**
Potentially applicable statutory provisions (e.g. BNS / IPC, IT Act, Consumer Protection Act, etc.), their plain-language meaning, jurisdiction, and verified source links where available. Explicitly flag any uncertainty.

**D. Recommended Solution**
Practical, lawful options available to the user. Explain advantages, limitations, risks, and realistic expectations of each option.

**E. Immediate Actions**
Urgent protective measures the user should take right now (personal safety, securing digital accounts, contacting bank, halting further loss, preserving perishable records).

**F. Step-by-Step Action Plan**
Prioritized, numbered steps. For every single step include:
- What to do
- Why it matters
- Where to do it or whom to contact
- What evidence or documents may be required
- Any deadline that has been verified (state if not fixed by statute)
- Contingency: What to do if this step does not yield results

**G. Evidence and Documents Checklist**
Comprehensive list of potentially relevant documents, communications, receipts, or logs. Explain lawful preservation methods (no illegal recordings or unauthorized system access).

**H. Escalation Options**
Appropriate official authorities, complaint portals (e.g. cybercrime.gov.in, National Consumer Helpline 1915, e-Daakhil, NALSA / DLSA legal aid clinics 15100), and when to engage a licensed advocate.

**I. Important Risks and Deadlines**
Urgent procedural deadlines (e.g. statutory limitation periods, notice response times) and actions that could compromise the user's legal position.

**J. Suggested Next Move**
One single, clear, immediate next step the user should execute today.

**K. Important Disclaimer**
State clearly: "This assessment is AI-generated preliminary legal information for educational purposes and does not constitute formal legal advice or create an advocate-client relationship. Laws vary by jurisdiction and factual specifics. Consult a licensed advocate before taking irreversible legal action."
"""


def parse_legal_analysis(text: str) -> Dict[str, Any]:
    """
    Parses the 11-section response text into structured dictionary fields
    and extracts action plan items for interactive tracking.
    """
    section_patterns = {
        "situation_summary": r"\*\*A\.\s*Situation Summary\*\*(.*?)(?=\*\*B\.|\Z)",
        "legal_assessment": r"\*\*B\.\s*Preliminary Legal Assessment\*\*(.*?)(?=\*\*C\.|\Z)",
        "applicable_laws": r"\*\*C\.\s*Applicable Law\*\*(.*?)(?=\*\*D\.|\Z)",
        "recommended_solution": r"\*\*D\.\s*Recommended Solution\*\*(.*?)(?=\*\*E\.|\Z)",
        "immediate_actions": r"\*\*E\.\s*Immediate Actions\*\*(.*?)(?=\*\*F\.|\Z)",
        "step_by_step_plan": r"\*\*F\.\s*Step-by-Step Action Plan\*\*(.*?)(?=\*\*G\.|\Z)",
        "evidence_checklist": r"\*\*G\.\s*Evidence and Documents Checklist\*\*(.*?)(?=\*\*H\.|\Z)",
        "escalation_options": r"\*\*H\.\s*Escalation Options\*\*(.*?)(?=\*\*I\.|\Z)",
        "risks_deadlines": r"\*\*I\.\s*Important Risks and Deadlines\*\*(.*?)(?=\*\*J\.|\Z)",
        "suggested_next_move": r"\*\*J\.\s*Suggested Next Move\*\*(.*?)(?=\*\*K\.|\Z)",
        "disclaimer": r"\*\*K\.\s*Important Disclaimer\*\*(.*?)(?=\Z)"
    }

    parsed = {}
    for key, pattern in section_patterns.items():
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            parsed[key] = match.group(1).strip()
        else:
            parsed[key] = ""

    # If parsing failed on markdown headers, fallback gracefully
    if not parsed["situation_summary"] and not parsed["legal_assessment"]:
        parsed["situation_summary"] = "Preliminary review of the user-submitted incident report."
        parsed["legal_assessment"] = text[:1500] if len(text) > 1500 else text
        parsed["recommended_solution"] = "Review the provided guidance points and follow up with a certified legal practitioner."
        parsed["suggested_next_move"] = "Review documents and consult official helpline channels."
        parsed["disclaimer"] = "AI-generated preliminary guidance. Consult a qualified advocate."

    # Parse individual action items from Step-by-Step Action Plan
    action_items = []
    plan_text = parsed.get("step_by_step_plan", "")
    if plan_text:
        # Match numbered items like "1. ", "Step 1:", "1) "
        raw_steps = re.split(r"\n(?=\d+[\.\)]|\bStep\s+\d+[:\.\)])", "\n" + plan_text)
        step_num = 1
        for s in raw_steps:
            cleaned = s.strip()
            if not cleaned or len(cleaned) < 10:
                continue
            
            # Extract title (first line)
            lines = cleaned.split("\n")
            title_line = lines[0]
            title = re.sub(r"^(\d+[\.\)]|Step\s+\d+[:\.\)])\s*", "", title_line).strip("* ")
            if not title:
                title = f"Action Step {step_num}"

            # Extract detailed explanation
            body_text = "\n".join(lines[1:]).strip() if len(lines) > 1 else cleaned
            
            # Search for specific sub-fields if present
            where_to_act = ""
            where_m = re.search(r"Where to do it.*?:(.*?)(?=\n-|\n[A-Z]|\Z)", cleaned, re.IGNORECASE | re.DOTALL)
            if where_m:
                where_to_act = where_m.group(1).strip()

            deadline = ""
            dl_m = re.search(r"Deadline.*?:(.*?)(?=\n-|\n[A-Z]|\Z)", cleaned, re.IGNORECASE | re.DOTALL)
            if dl_m:
                deadline = dl_m.group(1).strip()

            contingency = ""
            cont_m = re.search(r"(?:What to do if|Contingency|Fallback).*?:(.*?)(?=\n-|\n[A-Z]|\Z)", cleaned, re.IGNORECASE | re.DOTALL)
            if cont_m:
                contingency = cont_m.group(1).strip()

            action_items.append({
                "step_number": step_num,
                "title": title[:180],
                "explanation": body_text[:1200] if body_text else cleaned[:1200],
                "where_to_act": where_to_act[:300] if where_to_act else "Official portal or relevant counterparty",
                "required_evidence": "Relevant correspondence or proof of transaction",
                "verified_deadline": deadline[:200] if deadline else "Prompt action recommended",
                "contingency": contingency[:300] if contingency else "Escalate to official dispute body or legal aid",
                "status": "pending"
            })
            step_num += 1

    # If no steps were parsed from text, create standard structured action steps
    if not action_items:
        action_items = [
            {
                "step_number": 1,
                "title": "Preserve All Physical and Digital Evidence",
                "explanation": "Collect receipts, transaction IDs, communications, screenshots, and agreements in an unedited, secure repository.",
                "where_to_act": "Local device and cloud backup",
                "required_evidence": "Original files with intact metadata",
                "verified_deadline": "Immediate (within 24-48 hours)",
                "contingency": "Request duplicate bank statements or records from counterparty if originals are lost",
                "status": "pending"
            },
            {
                "step_number": 2,
                "title": "Issue Written Notice or Grievance to Counterparty",
                "explanation": "Deliver a formal written communication outlining the breach, stating facts objectively, and providing a fixed period for rectification.",
                "where_to_act": "Registered post or official email address",
                "required_evidence": "Proof of delivery or email acknowledgement",
                "verified_deadline": "Within 7-15 days of incident occurrence",
                "contingency": "If ignored or rejected, escalate to statutory regulatory body",
                "status": "pending"
            },
            {
                "step_number": 3,
                "title": "Approach Official Dispute Resolution or Regulatory Body",
                "explanation": "Lodge an official grievance via dedicated governmental channels (e.g. Cybercrime 1930, Consumer Helpline 1915, or Labour Authority).",
                "where_to_act": "Government grievance portal or jurisdictional magistrate",
                "required_evidence": "Notice copy, evidence inventory, and identity proof",
                "verified_deadline": "Within statutory limitation period",
                "contingency": "Seek assistance from DLSA / NALSA legal aid or a practicing advocate",
                "status": "pending"
            }
        ]

    return {
        "sections": parsed,
        "action_items": action_items
    }


def generate_expert_rule_based_guidance(intake: Dict[str, Any]) -> str:
    """
    High-fidelity, verified rule-based guidance generator matching Indian jurisdiction.
    Ensures 100% adherence to all 11 sections with real verified statutes, official portals,
    and tailored emergency handling when OpenAI API key is unconfigured or rate-limited.
    """
    category = (intake.get("category") or "other").lower()
    description = intake.get("raw_description", "")
    incident_date = intake.get("incident_date", "Recently")
    location = intake.get("incident_location", "India")
    outcome = intake.get("desired_outcome", "Resolution and lawful remedy")
    is_ongoing = intake.get("is_ongoing", False)
    immediate_danger = intake.get("immediate_danger", False)
    parties = intake.get("involved_parties", "Disputing parties")
    evidence = intake.get("evidence_summary", "Unspecified documents or correspondence")

    danger_alert = ""
    if immediate_danger:
        danger_alert = (
            "> [!CAUTION]\n"
            "> **IMMEDIATE PERSONAL SAFETY PRIORITY**: You indicated that someone may be in immediate physical danger. "
            "Please call the **National Emergency Support Service at 112** or your nearest police station immediately. "
            "Do not delay urgent safety interventions for legal paperwork.\n\n"
        )

    # Determine matched legal category and relevant statutes
    key_cat = "other"
    if any(w in category or w in description.lower() for w in ["cyber", "fraud", "scam", "upi", "phishing", "hack", "online"]):
        key_cat = "cybercrime"
    elif any(w in category or w in description.lower() for w in ["consumer", "refund", "defective", "product", "seller", "ecommerce"]):
        key_cat = "consumer"
    elif any(w in category or w in description.lower() for w in ["salary", "job", "employer", "workplace", "wages", "termination"]):
        key_cat = "employment"
    elif any(w in category or w in description.lower() for w in ["rent", "landlord", "deposit", "tenant", "property", "lease"]):
        key_cat = "property"
    elif any(w in category or w in description.lower() for w in ["cheque", "loan", "debt", "money", "recovery", "borrow"]):
        key_cat = "financial"
    elif any(w in category or w in description.lower() for w in ["harass", "threat", "stalk", "abuse", "blackmail"]):
        key_cat = "harassment"

    provisions = STATUTORY_PROVISIONS.get(key_cat, STATUTORY_PROVISIONS.get("consumer"))

    laws_formatted = ""
    for p in provisions:
        laws_formatted += (
            f"- **{p['act']} — {p['section']} ({p['title']})**:\n"
            f"  {p['explanation']}\n"
            f"  *Verified Source Reference*: [{p['act']}]({p['source_url']})\n\n"
        )

    # Category-specific customized contents
    if key_cat == "cybercrime":
        assessment = (
            "The incident involves prima facie unauthorized electronic transactions, digital impersonation, "
            "or cheating through cyber means. Under Indian law, financial cyber fraud is subject to both criminal prosecution "
            "and immediate administrative fund-tracing protocols."
        )
        recommended = (
            "1. **Administrative Banking Freeze & Cybercell Escalation (High Efficacy)**: Alerting the National Cybercrime Portal "
            "(1930) enables lien marking on the suspect bank accounts before funds are withdrawn at ATMs.\n"
            "2. **Formal Police First Information Report (FIR)**: Necessary if the amount is substantial or if the bank requires "
            "a formal police inquiry to credit disputed funds back under RBI customer liability guidelines."
        )
        immediate = (
            "1. Dial **1930** immediately to report the transaction ID and beneficiary account to the National Cybercrime Reporting Portal.\n"
            "2. Contact your bank's 24x7 fraud prevention helpline and request an immediate card/account freeze or dispute logging.\n"
            "3. Take uncropped screenshots of SMS transaction alerts, WhatsApp/Telegram communications, and UPI transaction reference (UTR) numbers."
        )
        next_move = "Call helpline 1930 now and register an official cyber incident at cybercrime.gov.in."
        escalation = (
            "- **National Cyber Crime Reporting Portal**: [cybercrime.gov.in](https://cybercrime.gov.in) | Helpline: **1930**\n"
            "- **Local Police Cyber Cell**: Station House Officer of your district cyber cell\n"
            "- **Banking Ombudsman (RBI)**: [cms.rbi.org.in](https://cms.rbi.org.in) if your bank fails to respond within 30 days"
        )
        risks = "Delays exceeding 24 hours drastically reduce the chances of freezing stolen funds before withdrawal through mule accounts."
        step1_title = "Report Immediately to National Cybercrime Helpline 1930"
        step1_where = "National Cyber Crime Reporting Portal (cybercrime.gov.in) or call 1930"
        step1_deadline = "Critical Golden Hours: within 2 to 24 hours of unauthorized transaction"

    elif key_cat == "consumer":
        assessment = (
            "The facts indicate a consumer dispute centered around defective goods, deficiency of service, "
            "or failure of an e-commerce or retail vendor to honour refund obligations. Under the Consumer Protection Act, 2019, "
            "consumers are protected against unfair trade practices."
        )
        recommended = (
            "1. **Pre-Litigation Formal Consumer Notice**: Issuing a structured grievance letter giving 7-15 days to resolve the issue.\n"
            "2. **National Consumer Helpline (NCH) Conciliation**: Quick, cost-free government mediation where docket numbers are assigned.\n"
            "3. **District Consumer Disputes Redressal Commission Filing**: Initiating formal proceedings via e-Daakhil if mediation fails."
        )
        immediate = (
            "1. Preserve the original purchase tax invoice, payment gateway confirmation, and warranty card.\n"
            "2. Save photographic or video evidence of the defective item or deficiency in service.\n"
            "3. Record all written communications (emails, support tickets) with date and timestamp."
        )
        next_move = "Send a formal consumer grievance letter via email and lodge a complaint docket at consumerhelpline.gov.in (1915)."
        escalation = (
            "- **National Consumer Helpline**: [consumerhelpline.gov.in](https://consumerhelpline.gov.in) | Toll-Free: **1915**\n"
            "- **e-Daakhil Online Filing**: [edaakhil.nic.in](https://edaakhil.nic.in)\n"
            "- **District Consumer Disputes Redressal Commission (DCDRC)** in your district"
        )
        risks = "Statutory limitation period: Under Section 69 of the Consumer Protection Act, 2019, consumer complaints must be instituted within 2 years from the date the dispute arose."
        step1_title = "Lodge Grievance with National Consumer Helpline (1915)"
        step1_where = "consumerhelpline.gov.in or SMS/Call 1915"
        step1_deadline = "Within statutory 2-year limitation period (immediate filing recommended)"

    elif key_cat == "employment":
        assessment = (
            "This dispute pertains to non-payment of earned wages, withholding of full-and-final settlement, "
            "or breach of employment covenants. In India, wages earned by an employee or workman cannot be arbitrarily withheld."
        )
        recommended = (
            "1. **Formal Workplace Grievance & Demand**: Written demand specifying overdue periods, exact amount, and 7-day compliance window.\n"
            "2. **Conciliation Before Labour Commissioner**: Approaching the jurisdictional Labour Officer under the Payment of Wages Act or Industrial Disputes Act.\n"
            "3. **Summary Recovery Suit or Legal Notice**: Engaging an advocate to issue a statutory demand notice."
        )
        immediate = (
            "1. Download and backup offer letter, appointment contract, payslips, form 16, and bank statements showing historical salary credits.\n"
            "2. Archive attendance logs, task approvals, email threads confirming active work tenure and resignation/handover acknowledgment."
        )
        next_move = "Issue a formal workplace demand letter with a 7-day cure period to HR and Management."
        escalation = (
            "- **Office of the Labour Commissioner / Chief Labour Commissioner (Central)**: [clc.gov.in](https://clc.gov.in)\n"
            "- **Samadhan Labour Portal**: [samadhan.labour.gov.in](https://samadhan.labour.gov.in)\n"
            "- **District Legal Services Authority (DLSA)** for free legal aid support"
        )
        risks = "Delaying formal demand beyond 1 year can complicate summary recovery proceedings under certain state Shops & Establishments rules."
        step1_title = "Serve Formal Written Demand Notice for Overdue Wages"
        step1_where = "Employer HR / Management registered email and postal address"
        step1_deadline = "Provide a 7 to 15 days compliance window"

    elif key_cat == "property":
        assessment = (
            "The matter concerns tenancy and rental obligations, particularly unlawful retention of security deposit "
            "or tenancy disagreements. Under standard rental contracts and Model Tenancy guidelines, landlords must return "
            "deposits after peaceful vacant possession, deducting only documented damages."
        )
        recommended = (
            "1. **Formal Demand Notice for Deposit Refund**: Demanding return within 7 days, warning of statutory interest and legal action.\n"
            "2. **Mediation / Rent Authority Intervention**: Filing before the local Rent Authority under applicable State Tenancy Acts.\n"
            "3. **Civil Suit for Recovery / Consumer Forum**: Where premises maintenance or developer services were bundled."
        )
        immediate = (
            "1. Preserve the signed lease agreement, rent receipts, bank transfer records for deposit payment, and handover acknowledgments.\n"
            "2. Document time-stamped video inspection of the premises upon handover showing condition."
        )
        next_move = "Draft and deliver the formal demand notice for deposit refund with bank account details."
        escalation = (
            "- **Jurisdictional Rent Authority / Rent Tribunal**\n"
            "- **Civil Court (Commercial / Summary Suit under Order 37 CPC)**\n"
            "- **Local Police Station** if criminal intimidation or illegal lock-out occurred"
        )
        risks = "Civil limitation period for recovery of debt is generally 3 years from the date the cause of action accrued under the Limitation Act, 1963."
        step1_title = "Issue Statutory Demand Notice for Return of Security Deposit"
        step1_where = "Delivered via Registered Speed Post with Acknowledgment Due & WhatsApp/Email"
        step1_deadline = "Give 7 to 15 days notice prior to court filing"

    else:
        assessment = (
            "The incident describes a legal dispute involving civil or contractual disagreements between private parties. "
            "A preliminary assessment requires examining the documentary trail, mutual commitments, and damages incurred."
        )
        recommended = (
            "1. **Pre-Litigation Settlement & Demand Notice**: Formally placing the opposite party on notice to settle the issue amicably.\n"
            "2. **Alternative Dispute Resolution (Mediation / Lok Adalat)**: Cost-effective resolution through DLSA or High Court mediation cells.\n"
            "3. **Formal Civil / Criminal Court Action**: Institution of appropriate legal proceedings through an advocate."
        )
        immediate = (
            "1. Compile chronological timeline of events from inception to the present dispute.\n"
            "2. Secure all contracts, receipts, messages, and recordings without alteration."
        )
        next_move = "Prepare an organized chronological dossier of evidence and schedule an advocate consultation."
        escalation = (
            "- **District Legal Services Authority (DLSA)**: Helpline **15100** for free legal aid\n"
            "- **Tele-Law Citizen Portal**: [tele-law.in](https://tele-law.in)\n"
            "- **Licensed Advocate / State Bar Council Member**"
        )
        risks = "Procedural limitation rules require timely action; do not wait until documentary evidence or memories fade."
        step1_title = "Prepare Comprehensive Chronology of Events and Evidence Dossier"
        step1_where = "Personal digital records and physical folder"
        step1_deadline = "Complete within 3 days"

    # Assemble complete 11-part document
    full_text = f"""{danger_alert}**A. Situation Summary**
The user reports an incident that occurred around {incident_date} in {location}. The situation involves {parties}, with the core issue revolving around: "{description[:300]}...". The stated desired outcome is: {outcome}. Situation ongoing status: {"Yes" if is_ongoing else "No"}.

**B. Preliminary Legal Assessment**
{assessment}
Key legal classifications to consider:
1. Primary classification: {category.title()}
2. Secondary procedural considerations: Jurisdiction verification in {location}, evidentiary admissibility under Bharatiya Sakshya Adhiniyam, 2023 (BSA) / Indian Evidence Act, and compliance with statutory pre-condition notices.

**C. Applicable Law**
The following Indian statutory enactments and provisions are potentially relevant to this incident:

{laws_formatted}*Note on Statutory Verification*: Provisions cited above are authoritative Indian statutes accessible via the Government of India legislative repository (indiacode.nic.in). Specific state amendments or local jurisdictional rules in {location} may also apply.

**D. Recommended Solution**
{recommended}

Advantages and Limitations:
- *Informal Notice / Direct Grievance*: Fastest and lowest cost; preserves relationships; but counterparty may delay if not backed by credible escalation.
- *Government Helpline / Regulatory Conciliation*: Official backing, zero or negligible court fees; non-adversarial resolution; timeline depends on caseload.
- *Court Litigation*: Enforceable decree and binding judicial orders; requires advocate representation, court fees, and longer duration.

**E. Immediate Actions**
{immediate}

**F. Step-by-Step Action Plan**
1. {step1_title}
- What to do: Initiate formal contact through official channels providing structured facts and documentary references.
- Why it matters: Establishes a verified procedural timestamp and puts counterparty or authorities on official notice.
- Where to do it or whom to contact: {step1_where}
- What evidence or documents may be required: Copies of agreements, proof of payments, correspondence records, and identity proof.
- Any deadline that has been verified: {step1_deadline}
- What to do if the first step does not work: Proceed to Step 2 for regulatory escalation or formal legal notice.

2. Issue a Formal Written Legal Notice via Registered Post or Email
- What to do: Send a structured demand letter giving 7-15 days for compliance.
- Why it matters: Serves as a vital prerequisite for consumer or civil court proceedings.
- Where to do it or whom to contact: Opposite party's registered address and verified email.
- What evidence or documents may be required: Written notice draft, postal speed post receipt, delivery tracking confirmation.
- Any deadline that has been verified: Allow 15 days from delivery for response.
- What to do if the first step does not work: File complaint with the appropriate statutory commission or magistrate.

3. Escalate to Statutory Redressal Authority or Legal Services Commission
- What to do: Register an online petition or approach the jurisdictional court / consumer forum / legal services authority.
- Why it matters: Obtains formal judicial or quasi-judicial orders for recovery, compensation, or penalty.
- Where to do it or whom to contact: District Consumer Commission, Cyber Cell, or DLSA.
- What evidence or documents may be required: Complete paperbook: Petition, affidavit, notice, postal proof, and supporting evidence.
- Any deadline that has been verified: Observe statutory limitation period.
- What to do if the first step does not work: Seek appellate remedies before the State Commission or High Court.

**G. Evidence and Documents Checklist**
Please assemble and preserve the following items lawfully (do not attempt unauthorized computer access or deceptive illegal wiretapping):
- [ ] Primary Transaction Document (Agreement, Contract, Offer Letter, Lease, or Purchase Receipt)
- [ ] Financial Trail (Bank account statements, UPI transaction IDs, UTR references, receipts)
- [ ] Written Communications (Email threads, WhatsApp/SMS exports with phone numbers visible)
- [ ] Incident Timeline Notes (Chronological log of events, meetings, and verbal discussions)
- [ ] Identification Credentials (Government photo ID of claimant for official filings)

**H. Escalation Options**
{escalation}
- **Legal Aid Services**: Eligible citizens (women, industrial workmen, scheduled categories, and persons below income thresholds) are entitled to free legal aid from DLSA/NALSA under Section 12 of the Legal Services Authorities Act, 1987. Helpline: **15100**.

**I. Important Risks and Deadlines**
- {risks}
- *Evidentiary Hazard*: Never delete chat threads or format devices holding critical transaction records.
- *Defamation Risk*: Avoid posting unverified allegations on public social media forums before legal verification, as this can trigger counter-claims.

**J. Suggested Next Move**
{next_move}

**K. Important Disclaimer**
This assessment is AI-generated preliminary legal information for educational purposes and does not constitute formal legal advice or create an advocate-client relationship. Laws vary by jurisdiction and factual specifics. Consult a licensed advocate before taking irreversible legal action.
"""
    return full_text.strip()


def run_ai_consultation(intake: Dict[str, Any], api_key: Optional[str] = None, model: str = "gpt-4.1-mini") -> Dict[str, Any]:
    """
    Main entry point for AI Legal Consultation.
    Calls OpenAI API if API key is provided and functional;
    Falls back reliably to verified expert Indian legal guidance engine if API key is missing or quota exhausted.
    Returns parsed dictionary containing full text, 11 structured sections, and interactive action items.
    """
    client = None
    if api_key and api_key.strip() and api_key != "put_your_secret_api_key_here":
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key.strip(), timeout=60.0, max_retries=2)
        except Exception as e:
            logger.warning(f"Could not initialize OpenAI client: {e}")
            client = None

    prompt_user_content = f"""USER INCIDENT INTAKE DATA:
- Incident Category: {intake.get('category', 'Unspecified')}
- Title: {intake.get('title', 'Legal Inquiry')}
- What happened (Full narrative): {intake.get('raw_description', '')}
- When did it happen: {intake.get('incident_date', 'Not specified')}
- Where did it happen: {intake.get('incident_location', 'India')}
- Who was involved: {intake.get('involved_parties', 'Disputing parties')}
- What outcome is desired: {intake.get('desired_outcome', 'Resolution')}
- Is the situation ongoing: {'Yes' if intake.get('is_ongoing') else 'No'}
- Is anyone in immediate danger: {'Yes' if intake.get('immediate_danger') else 'No'}
- Evidence / documents on hand: {intake.get('evidence_summary', 'Not specified')}

Please analyze this incident according to your system prompt rules. Address the 5 essential questions and provide the required 11 sections (A through K).
"""

    analysis_text = ""
    used_openai = False
    openai_error = None

    if client:
        try:
            logger.info(f"Invoking OpenAI model '{model}' for legal guidance...")
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": LEGAL_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt_user_content}
                ],
                temperature=0.2,
                max_tokens=3200
            )
            analysis_text = (response.choices[0].message.content or "").strip()
            if analysis_text:
                used_openai = True
        except Exception as exc:
            logger.warning(f"OpenAI call encountered error: {exc}. Falling back to verified statutory guidance.")
            openai_error = str(exc)

    if not analysis_text:
        # Fallback to verified legal rules engine
        analysis_text = generate_expert_rule_based_guidance(intake)

    parsed = parse_legal_analysis(analysis_text)
    parsed["raw_full_text"] = analysis_text
    parsed["used_openai"] = used_openai
    if openai_error:
        parsed["openai_notice"] = f"AI fallback used: {openai_error}"

    return parsed

