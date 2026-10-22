"""
LawAI Advisor - Authoritative Legal Knowledge Base & Official Statutory Directory (India)
Verified reference provisions, official portals, emergency helplines, and document templates.
"""

# Official Helplines and Emergency Portals in India
OFFICIAL_RESOURCES = {
    "emergency": {
        "title": "National Emergency Support Services",
        "number": "112",
        "description": "Unified 24x7 emergency helpline for police, fire, and ambulance across India.",
        "url": "https://112.gov.in",
        "verified": True
    },
    "cybercrime": {
        "title": "National Cyber Crime Reporting Portal & Financial Fraud Helpline",
        "number": "1930",
        "description": "Citizen Financial Cyber Fraud Reporting System to freeze fraudulent bank transfers immediately.",
        "url": "https://cybercrime.gov.in",
        "verified": True
    },
    "consumer": {
        "title": "National Consumer Helpline (NCH)",
        "number": "1915",
        "alternate": "1800-11-4000",
        "description": "Ministry of Consumer Affairs portal for consumer complaints, refunds, and deficiency of service.",
        "url": "https://consumerhelpline.gov.in",
        "portal_name": "e-Daakhil (Online Consumer Commission Filing)",
        "portal_url": "https://edaakhil.nic.in",
        "verified": True
    },
    "legal_aid": {
        "title": "National Legal Services Authority (NALSA)",
        "number": "15100",
        "description": "Free legal services and legal aid clinics for eligible citizens under Legal Services Authorities Act, 1987.",
        "url": "https://nalsa.gov.in",
        "portal_name": "Tele-Law Mobile App & Citizen Portal",
        "portal_url": "https://tele-law.in",
        "verified": True
    },
    "women": {
        "title": "National Women Helpline",
        "number": "181",
        "alternate": "1091",
        "description": "24/7 support for women facing harassment, violence, or domestic disputes.",
        "url": "https://ncw.nic.in",
        "verified": True
    },
    "labour": {
        "title": "Chief Labour Commissioner / Samadhan Portal",
        "number": "1800-180-1111",
        "description": "Conciliation and grievance portal for industrial and payment of wages disputes.",
        "url": "https://clc.gov.in",
        "portal_url": "https://samadhan.labour.gov.in",
        "verified": True
    }
}

# Verified Indian Statutory Framework Mapping
STATUTORY_PROVISIONS = {
    "cybercrime": [
        {
            "act": "Information Technology Act, 2000",
            "section": "Section 66C",
            "title": "Punishment for Identity Theft",
            "explanation": "Applies when someone fraudulently or dishonestly uses another person's password, digital signature, or electronic ID.",
            "source_url": "https://www.indiacode.nic.in/handle/123456789/1362",
            "verified": True
        },
        {
            "act": "Information Technology Act, 2000",
            "section": "Section 66D",
            "title": "Punishment for Cheating by Personation using Computer Resource",
            "explanation": "Penalizes cyber fraud, phishing, impersonation scams, and deceitful online money transfers.",
            "source_url": "https://www.indiacode.nic.in/handle/123456789/1362",
            "verified": True
        },
        {
            "act": "Bharatiya Nyaya Sanhita, 2023 (BNS) / erstwhile IPC",
            "section": "Section 318(4) BNS (formerly Section 420 IPC)",
            "title": "Cheating and Dishonestly Inducing Delivery of Property",
            "explanation": "Criminal sanction for inducing someone to transfer money or property through fraudulent or dishonest representations.",
            "source_url": "https://www.indiacode.nic.in",
            "verified": True
        }
    ],
    "consumer": [
        {
            "act": "Consumer Protection Act, 2019",
            "section": "Section 2(7)",
            "title": "Definition of Consumer",
            "explanation": "Protects individuals who buy goods or hire services for consideration, including online e-commerce transactions.",
            "source_url": "https://www.indiacode.nic.in/handle/123456789/15256",
            "verified": True
        },
        {
            "act": "Consumer Protection Act, 2019",
            "section": "Section 35 & Section 38",
            "title": "Manner in which Complaint shall be made to District Commission",
            "explanation": "Enables consumers to file complaints online via e-Daakhil against deficiency in service, unfair trade practices, or failure to refund.",
            "source_url": "https://edaakhil.nic.in",
            "verified": True
        },
        {
            "act": "Consumer Protection Act, 2019",
            "section": "Section 69",
            "title": "Limitation Period",
            "explanation": "Verified statutory deadline: Complaint must be filed within 2 years from the date on which the cause of action arose.",
            "source_url": "https://www.indiacode.nic.in/handle/123456789/15256",
            "verified": True
        }
    ],
    "employment": [
        {
            "act": "Payment of Wages Act, 1936",
            "section": "Section 15",
            "title": "Claims arising out of deductions from wages or delay in payment",
            "explanation": "Empowers employees to approach the Labour Authority for recovery of delayed or illegally deducted salary.",
            "source_url": "https://www.indiacode.nic.in/handle/123456789/2384",
            "verified": True
        },
        {
            "act": "Industrial Disputes Act, 1947",
            "section": "Section 2A & Section 33C(2)",
            "title": "Recovery of Money Due from an Employer",
            "explanation": "Enables workmen to approach the Labour Court for recovery of unpaid dues, severance, or wrongful termination compensation.",
            "source_url": "https://www.indiacode.nic.in/handle/123456789/15191",
            "verified": True
        },
        {
            "act": "State Shops and Establishments Acts",
            "section": "Applicable State Provision",
            "title": "Regulation of Service Conditions & Non-Payment of Salary",
            "explanation": "Provides summary complaint mechanisms before local Labour Commissioners for commercial office employees.",
            "source_url": "https://labour.gov.in",
            "verified": True
        }
    ],
    "property": [
        {
            "act": "Model Tenancy Act / State Rent Control Legislation",
            "section": "Security Deposit & Eviction Norms",
            "title": "Refund of Security Deposit & Prevention of Unlawful Eviction",
            "explanation": "Mandates refund of security deposit upon handover of premises after deducting legitimate dues, and bars arbitrary eviction without due process.",
            "source_url": "https://mohua.gov.in/upload/uploadfiles/files/Model_Tenancy_Act_English.pdf",
            "verified": True
        },
        {
            "act": "Indian Contract Act, 1872",
            "section": "Section 73",
            "title": "Compensation for Loss or Damage caused by Breach of Contract",
            "explanation": "Provides legal basis for recovering damages and withheld deposits where terms of a lease or rental agreement have been breached.",
            "source_url": "https://www.indiacode.nic.in/handle/123456789/2187",
            "verified": True
        }
    ],
    "financial": [
        {
            "act": "Negotiable Instruments Act, 1881",
            "section": "Section 138",
            "title": "Dishonour of Cheque for Insufficiency of Funds",
            "explanation": "Criminal sanction for bounced cheques. Strict procedural timeline: Statutory demand notice must be served within 30 days of receiving return memo; drawer has 15 days to pay; complaint must be filed in court within 30 days thereafter.",
            "source_url": "https://www.indiacode.nic.in/handle/123456789/2189",
            "verified": True
        },
        {
            "act": "Bharatiya Nyaya Sanhita, 2023 / IPC",
            "section": "Section 316 BNS (formerly Section 406 IPC)",
            "title": "Criminal Breach of Trust",
            "explanation": "Applies when money or property entrusted to someone is dishonestly misappropriated or converted to their own use.",
            "source_url": "https://www.indiacode.nic.in",
            "verified": True
        }
    ],
    "harassment": [
        {
            "act": "Bharatiya Nyaya Sanhita, 2023 / IPC",
            "section": "Section 78 BNS (formerly Section 354D IPC)",
            "title": "Stalking and Electronic Harassment",
            "explanation": "Monitors or contacts an individual persistently despite disinterest, or monitors internet, email or electronic communication.",
            "source_url": "https://www.indiacode.nic.in",
            "verified": True
        },
        {
            "act": "Bharatiya Nyaya Sanhita, 2023 / IPC",
            "section": "Section 351 BNS (formerly Section 506 IPC)",
            "title": "Criminal Intimidation",
            "explanation": "Threatening injury to person, reputation, or property with intent to cause alarm.",
            "source_url": "https://www.indiacode.nic.in",
            "verified": True
        },
        {
            "act": "POSH Act, 2013",
            "section": "Section 9",
            "title": "Complaint of Sexual Harassment at Workplace",
            "explanation": "Aggrieved woman can file a formal complaint with the Internal Committee (IC) within 3 months of the incident.",
            "source_url": "https://www.indiacode.nic.in/handle/123456789/2104",
            "verified": True
        }
    ]
}

# Legal Document Draft Templates with placeholders
DOCUMENT_TEMPLATES = {
    "legal_notice": {
        "title": "Formal Legal Demand Notice (For Advocate Review)",
        "description": "Standard pre-litigation demand notice putting the other party on formal notice before instituting court or consumer proceedings.",
        "category": "General Dispute / Contract / Recovery",
        "template": """LEGAL NOTICE / DEMAND LETTER
[DRAFT FOR ADVOCATE REVIEW — NOT A SUBSTITUTE FOR INDEPENDENT LEGAL COUNSEL]

Date: {date}
To:
{recipient_name}
{recipient_org}
{recipient_address}

From:
{user_name}
{user_address}
Contact Email: {user_email}

SUBJECT: FORMAL DEMAND NOTICE REGARDING {subject_summary}

Sir / Madam,

Under instructions and on behalf of myself, I hereby state and bring to your urgent attention the following facts:

1. FACTUAL BACKGROUND:
On or around {incident_date}, at {incident_location}, the following transaction or incident occurred:
{incident_facts}

2. THE GRIEVANCE AND BREACH:
Despite repeated reminders and requests, you have failed and neglected to fulfill your lawful obligations, specifically:
{grievance_details}
Amount in dispute / Claimed value: INR {dispute_amount} (Rupees {dispute_amount_words} only).

3. LEGAL CONSEQUENCES:
Your aforementioned acts and omissions constitute a serious breach of applicable legal provisions, including:
{applicable_laws_summary}
This has caused severe financial loss, mental agony, and disruption.

4. DEMAND AND TIMELINE:
I hereby call upon you to comply with the following demands within 15 (FIFTEEN) days from the receipt of this notice:
a) {specific_demand_1}
b) Pay the outstanding sum of INR {dispute_amount} along with appropriate interest / compensation.

5. RESERVATION OF RIGHTS:
Please take note that in the event you fail to comply within the stipulated 15-day period, I shall be constrained to initiate appropriate civil, consumer, or criminal legal proceedings against you before the competent forum or court having jurisdiction, entirely at your risk, cost, and legal consequence.

A copy of this notice is retained for our records and future court submission.

Yours faithfully,

_______________________________
{user_name}
(Complainant / Claimant)
Note: This draft has been generated for review. It is strongly advised to have a practicing advocate verify and sign formal legal notices before dispatch."""
    },
    "consumer_complaint": {
        "title": "Consumer Grievance / Formal Refund Demand",
        "description": "Notice addressed to a seller, vendor, or service provider under the Consumer Protection Act, 2019.",
        "category": "Consumer complaints",
        "template": """CONSUMER GRIEVANCE AND FORMAL NOTICE UNDER CONSUMER PROTECTION ACT, 2019
[DRAFT FOR COMPLAINANT SUBMISSION TO COMPANY / NATIONAL CONSUMER HELPLINE]

Date: {date}
To:
Customer Care / Grievance Redressal Officer
{recipient_org}
{recipient_address}
Email: {recipient_email}

Complainant Details:
Name: {user_name}
Address: {user_address}
Mobile / Email: {user_email}

SUBJECT: FORMAL GRIEVANCE REGARDING DEFICIENCY OF SERVICE / DEFECTIVE PRODUCT / REFUND REFUSAL
Reference / Order / Account No: {order_reference}

Dear Grievance Officer,

I am writing this formal grievance in my capacity as a 'Consumer' within the meaning of Section 2(7) of the Consumer Protection Act, 2019.

1. TRANSACTION PARTICULARS:
On {incident_date}, I purchased goods / booked services from your organization against consideration of INR {dispute_amount}.
Details of the transaction: {incident_facts}

2. PARTICULARS OF DEFECT / DEFICIENCY:
The product delivered / service rendered suffers from severe deficiency / defect as follows:
{grievance_details}

3. STEPS ALREADY TAKEN:
I have reached out to your support team on several occasions, but no satisfactory resolution or refund has been provided to date.

4. RELIEF SOUGHT:
In terms of the statutory rights provided to consumers under the Consumer Protection Act, 2019, I request you to:
1. Immediately process a full refund of INR {dispute_amount} to my original payment source.
2. Provide reimbursement for any incidental losses and inconvenience suffered.

5. NOTICE OF FORUM PROCEEDINGS:
If this grievance is not resolved within 7 (SEVEN) working days, I will register a formal complaint with the National Consumer Helpline (NCH / 1915) and initiate online proceedings through the e-Daakhil portal before the competent District Consumer Disputes Redressal Commission seeking refund, compensation for mental agony, and litigation costs.

Sincerely,

{user_name}
Enclosures:
1. Copy of Invoice / Payment Receipt
2. Communication Records / Screenshots of correspondence"""
    },
    "workplace_grievance": {
        "title": "Workplace Grievance & Unpaid Salary Demand Letter",
        "description": "Formal workplace communication to Management or HR demanding release of earned wages and full-and-final settlement.",
        "category": "Employment disputes",
        "template": """FORMAL WORKPLACE GRIEVANCE & DEMAND FOR OUTSTANDING WAGES
Date: {date}
To:
The Management / Human Resources Department
{recipient_org}
{recipient_address}

From:
Employee Name: {user_name}
Employee ID / Designation: {employee_id}
Department: {department}
Email: {user_email}

SUBJECT: FORMAL DEMAND FOR PAYMENT OF WITHHELD EARNED SALARY / DUES

Dear Sir / Madam,

I am writing to formally place on record my grievance regarding the non-payment of my earned salary and statutory dues in violation of the agreed employment contract and the Payment of Wages Act, 1936.

1. EMPLOYMENT TENURE AND WAGE DETAILS:
I have been employed with {recipient_org} as {designation}. I have diligently performed all my assigned duties during the employment period.

2. DETAILS OF WITHHELD AMOUNTS:
My salary / dues for the following period remain unpaid without lawful justification:
Period: {unpaid_period}
Total Outstanding Amount: INR {dispute_amount} (Rupees {dispute_amount_words} only).
Facts regarding the delay: {incident_facts}

3. STATUTORY AND CONTRACTUAL OBLIGATIONS:
Under the terms of employment and prevailing labour regulations, salary earned by an employee cannot be arbitrarily withheld, delayed, or deducted without lawful authority.

4. REQUEST FOR IMMEDIATE REMITTANCE:
I request the accounts and HR departments to credit the overdue sum of INR {dispute_amount} directly to my registered salary bank account within 7 (SEVEN) business days of this letter.

5. RESERVATION OF REMEDIES:
In the unfortunate event that this matter remains unaddressed, I will be compelled to submit a formal complaint before the competent Labour Commissioner / Conciliation Officer under the Payment of Wages Act and pursue appropriate statutory remedies.

Thank you for your prompt attention to resolving this matter amicably.

Sincerely,

{user_name}
Contact: {user_email}"""
    },
    "rent_deposit_notice": {
        "title": "Demand Notice for Refund of Rental Security Deposit",
        "description": "Formal notice to a landlord demanding the lawful return of a security deposit after vacating the rental premises.",
        "category": "Property & Tenancy",
        "template": """DEMAND NOTICE FOR REFUND OF RENTAL SECURITY DEPOSIT
Date: {date}
To:
{recipient_name} (Landlord / Property Owner)
Address: {recipient_address}
Mobile / Contact: {recipient_phone}

From:
{user_name} (Former Tenant)
Current Address: {user_address}
Contact Email: {user_email}

SUBJECT: DEMAND FOR REFUND OF RENTAL SECURITY DEPOSIT FOR PREMISES: {property_address}

Dear {recipient_name},

This notice is issued regarding the rental premises located at {property_address}, which was leased to me under the tenancy agreement dated {lease_date}.

1. VACATION AND HANDOVER OF PREMISES:
As per the mutually agreed terms, I lawfully vacated the premises on {vacation_date} and handed over keys and possession in good, habitable condition, subject only to reasonable wear and tear.

2. SECURITY DEPOSIT PARTICULARS:
At the commencement of tenancy, I deposited an interest-free refundable security deposit of INR {deposit_amount}.
After adjusting mutually agreed legitimate dues (if any), the net refundable sum due is INR {dispute_amount}.

3. DELAY IN REFUND:
More than {days_passed} days have elapsed since peaceful possession was delivered to you. Despite my repeated phone calls and messages on {reminder_dates}, you have unlawfully withheld the refund without providing any itemized justification.

4. FINAL DEMAND:
I hereby call upon you to refund the full balance amount of INR {dispute_amount} by electronic transfer to my bank account within 7 (SEVEN) days of receiving this notice.
Bank Account Details:
Account Holder: {user_name}
Bank Name: {bank_name}
Account No: [Provide in private communication]
IFSC: [Provide in private communication]

5. LEGAL REMEDIES:
Please note that withholding a refundable tenant deposit unlawfully constitutes a breach of contract and civil wrong under Section 73 of the Indian Contract Act, 1872. Should you fail to remit the funds within the specified timeframe, I shall proceed with filing a complaint before the local Rent Authority / Civil Court for recovery of the principal sum along with 18% per annum interest and litigation costs.

Sincerely,

{user_name}"""
    },
    "cybercrime_complaint": {
        "title": "Cyber Financial Fraud Incident Summary & Police Complaint Template",
        "description": "Structured complaint format to report online scams, UPI fraud, phishing, or identity theft to police and cyber cell.",
        "category": "Cybercrime & Online Fraud",
        "template": """COMPLAINT BEFORE THE STATION HOUSE OFFICER / CYBER CRIME POLICE STATION
[FOR SUBMISSION TO LOCAL CYBER CRIME CELL AND UPLOAD ON CYBERCRIME.GOV.IN]

Date: {date}
To:
The Officer-in-Charge / Superintendent of Police
Cyber Crime Cell / Police Station: {police_station}
District & State: {incident_location}

Complainant Information:
Full Name: {user_name}
Address: {user_address}
Mobile Number: {user_phone}
Email Address: {user_email}

SUBJECT: COMPLAINT AGAINST UNKNOWN / KNOWN PERSON(S) FOR CYBER FRAUD, CHEATING UNDER SECTION 66D OF IT ACT, 2000 AND SECTION 318(4) OF BHARATIYA NYAYA SANHITA (BNS)

Sir / Madam,

I wish to lodge a formal complaint regarding an incident of financial cyber fraud through which I was dishonestly defrauded of INR {dispute_amount}.

1. INCIDENT CHRONOLOGY:
Date & Time of Fraud: {incident_date}
Platform / Medium Used: {platform_name} (e.g. WhatsApp / Phone Call / Telegram / Website)
Suspect's Contact Number / ID: {suspect_details}
Description of Incident:
{incident_facts}

2. TRANSACTION DETAILS:
Amount Debited: INR {dispute_amount}
Complainant Bank Name: {complainant_bank}
Complainant Account / UPI ID: [Registered ID]
Fraudulent Transaction Reference / UTR Number(s): {utr_numbers}
Beneficiary Bank / Suspect UPI ID (if known): {beneficiary_details}

3. IMMEDIATE ACTION TAKEN:
- I immediately called the National Cybercrime Helpline 1930 on {call_date_time} and registered an incident acknowledgment: Acknowledgment No. {ack_number}.
- I reported the unauthorized debit to my bank's fraud prevention helpline and requested lien marking on the suspect recipient account.

4. PRAYER / RELIEF SOUGHT:
In light of the above facts, I respectfully request the police authorities to:
a) Register an FIR / GD Entry under Section 66C and 66D of the Information Technology Act, 2000, and Section 318(4) of Bharatiya Nyaya Sanhita, 2023.
b) Direct the concerned payment gateways / banks to trace the transaction trail, freeze the defrauded funds, and facilitate recovery.
c) Take strict penal action against the perpetrators.

I declare that the information provided above is true and correct to the best of my knowledge.

Yours faithfully,

_______________________________
{user_name}

Enclosures:
1. Bank Account Statement highlighting disputed transaction(s)
2. Screenshot of transaction confirmations / SMS alerts
3. Screenshots of chat transcripts / suspicious phone numbers
4. Cybercrime Portal (1930) acknowledgment slip"""
    }
}

