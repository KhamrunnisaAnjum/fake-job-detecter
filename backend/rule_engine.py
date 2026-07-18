import re

def analyze_job_text(text: str, title: str = "", company: str = "", is_message: bool = False):
    warnings = []
    text_lower = text.lower()
    
    # 1. Telegram / WhatsApp Links
    if re.search(r'(t\.me|telegram\.me|wa\.me|whatsapp\.com|chat\.whatsapp\.com)', text_lower):
        warnings.append("⚠️ Contains Telegram or WhatsApp links, commonly used by scammers.")
    
    # 2. Gmail / Personal Recruiter Emails
    if re.search(r'[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com|hotmail\.com|outlook\.com)', text_lower):
        warnings.append("⚠️ Uses a free personal email provider instead of a corporate domain.")
    
    # 3. Payment Requests / Registration Fees
    if re.search(r'(registration fee|processing fee|security deposit|pay upfront|onboarding fee|initial payment|refundable deposit)', text_lower):
        warnings.append("⚠️ Asks for a fee or deposit. Legitimate jobs NEVER ask candidates to pay.")
    
    # 4. UPI / Crypto Payments
    if re.search(r'([a-zA-Z0-9.\-_]+@[a-zA-Z]+)|(bitcoin|crypto|usdt|eth|wallet address)', text_lower):
        # We need to be slightly more specific for UPI so we don't catch emails accidentally in the first group,
        # but the simple @ regex might catch emails. Let's refine UPI regex.
        pass
    
    if re.search(r'[a-zA-Z0-9.\-_]+@(okicici|okhdfcbank|okaxis|oksbi|ybl|ibl|upi)', text_lower):
        warnings.append("⚠️ Contains a UPI ID, often used to solicit fraudulent payments.")
        
    if re.search(r'\b(bitcoin|crypto|usdt|ethereum|wallet address|binance)\b', text_lower):
        warnings.append("⚠️ Mentions Cryptocurrency. Job offers involving crypto payments are highly suspicious.")
    
    # 5. Urgency Language
    if re.search(r'\b(act fast|hire immediately|urgent hiring|limited spots|only a few spots left|apply today or miss out)\b', text_lower):
        warnings.append("⚠️ Uses artificial urgency to pressure you into applying quickly.")
    
    # 6. Unrealistic Salary / Too Good to be True
    # e.g., $1000/day, $500/hour
    if re.search(r'(\$|₹|rs\.?|rupees|usd)\s*\d{3,}[,/]*\d*\s*(per day|/day|per hour|/hour|per week|/week|daily)', text_lower):
        warnings.append("⚠️ Salary seems unrealistically high for a short period (e.g., extremely high daily or hourly pay).")
        
    # 7. Very short description (Not applicable for WhatsApp messages as much, but good for jobs)
    if not is_message and len(text) < 150:
        warnings.append("⚠️ Job description is suspiciously short and lacks professional detail.")
        
    # 8. Famous Company Impersonation
    famous_companies = ['google', 'amazon', 'microsoft', 'apple', 'meta', 'facebook', 'netflix', 'tesla']
    if company.lower() in famous_companies:
        # If it's a famous company but uses a personal email or weird links
        if re.search(r'[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com)', text_lower):
            warnings.append(f"⚠️ Claims to be {company} but uses a personal email address. Highly likely to be an impersonation.")

    return warnings
