import re

def analyze_job_text(text: str, title: str = "", company: str = "", is_message: bool = False, source: str = "Unknown"):
    warnings = []
    risk_breakdown = {
        "urgency_flags": 0,
        "financial_flags": 0,
        "platform_flags": 0,
        "unrealistic_flags": 0
    }
    
    text_lower = text.lower()
    
    # 1. Platform Flags (Telegram, WhatsApp, Google Form)
    if re.search(r'\b(telegram|whatsapp|google form|t\.me|telegram\.me|wa\.me|chat\.whatsapp\.com|contact on telegram|dm on whatsapp)\b', text_lower):
        warnings.append("⚠️ Uses informal platforms (Telegram/WhatsApp/Google Forms) which are highly unusual for legitimate hiring.")
        risk_breakdown["platform_flags"] += 25
    
    # 2. Financial Flags (Fees, UPI, Crypto)
    if re.search(r'\b(registration fee|processing fee|security deposit|pay upfront|onboarding fee|initial payment|refundable deposit|upi|crypto|bitcoin|usdt|eth|wallet address|investment required|training fee|certificate guaranteed)\b', text_lower):
        warnings.append("⚠️ Requests payment, fees, or mentions crypto/UPI. Legitimate jobs NEVER ask candidates to pay.")
        risk_breakdown["financial_flags"] += 45
    
    # 3. Urgency Flags
    if re.search(r'\b(act fast|hire immediately|urgent hiring|limited spots|only a few spots left|apply today|immediate joining|limited seats|join now|click link)\b', text_lower):
        warnings.append("⚠️ Uses artificial urgency or pressure tactics to force quick applications.")
        risk_breakdown["urgency_flags"] += 15
    
    # 4. Unrealistic Claims
    if re.search(r'\b(earn ₹5000 daily|work from home|no interview|no experience required|easy money|no skills required)\b', text_lower):
        warnings.append("⚠️ Contains 'Too Good To Be True' claims (e.g., massive daily pay, no interview, no experience needed).")
        risk_breakdown["unrealistic_flags"] += 25
        
    # 5. Famous Company Impersonation
    famous_companies = ['google', 'amazon', 'microsoft', 'apple', 'meta', 'facebook', 'netflix', 'tesla']
    if company.lower() in famous_companies:
        if re.search(r'[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com)', text_lower):
            warnings.append(f"⚠️ Claims to be {company} but uses a personal email address. Highly likely to be an impersonation.")
            risk_breakdown["platform_flags"] += 20

    # 6. Source Mismatch & Suspicious Formats (Only for messages)
    if is_message:
        words = text.strip().split()
        has_link = bool(re.search(r'http[s]?://', text_lower) or re.search(r'\b(bit\.ly|tinyurl|igsh=)\b', text_lower))
        
        # Bare URLs masquerading as messages
        if len(words) <= 3 and has_link:
            warnings.append("⚠️ Contains only a bare link without context. This is highly suspicious behavior typical of spam or phishing.")
            risk_breakdown["platform_flags"] += 40
            
        # Source Mismatch
        if source == "Email" and len(text) < 150 and has_link:
            warnings.append("⚠️ Source mismatch: Selected 'Email' but content looks like a short messaging link (e.g. WhatsApp/SMS). Phishing risk.")
            risk_breakdown["platform_flags"] += 30
            
        if source == "LinkedIn" and re.search(r'(wa\.me|t\.me|telegram\.me)', text_lower):
            warnings.append("⚠️ Source mismatch: A LinkedIn message directing you immediately to WhatsApp or Telegram is a classic scam tactic.")
            risk_breakdown["platform_flags"] += 40
            
    # Calculate Total Risk Score Added by Heuristics
    total_heuristic_risk = sum(risk_breakdown.values())
    
    # Generate Explanation
    if total_heuristic_risk >= 40:
        explanation = "The text contains multiple severe red flags typical of employment scams, such as requests for money, suspicious platforms, or unrealistic promises."
        recommended_action = "Do not engage. Block the sender and report the listing."
    elif total_heuristic_risk > 0:
        explanation = "The text contains some suspicious patterns. Proceed with extreme caution and verify the employer's official website."
        recommended_action = "Proceed with caution. Do not share personal or financial details."
    else:
        explanation = "No major heuristic red flags were detected, but always remain vigilant."
        recommended_action = "Safe to proceed, but perform standard due diligence."

    return {
        "warnings": warnings,
        "risk_breakdown": risk_breakdown,
        "total_heuristic_risk": total_heuristic_risk,
        "explanation": explanation,
        "recommended_action": recommended_action
    }
