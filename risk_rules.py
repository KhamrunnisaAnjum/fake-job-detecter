def get_risk_flags(title, description, salary_range, company_profile, telecommuting):
    flags = []

    if not salary_range or salary_range.strip() == "":
        flags.append("No salary range provided")

    if not company_profile or len(company_profile.strip()) < 30:
        flags.append("Very little or no company information given")

    urgent_words = ["urgent", "immediate joining", "limited seats", "act now", "hurry"]
    text = (description or "").lower()
    if any(word in text for word in urgent_words):
        flags.append("Uses urgency-pressure language")

    money_words = ["registration fee", "processing fee", "pay to apply", "deposit required"]
    if any(word in text for word in money_words):
        flags.append("Asks for payment from applicant (major red flag)")

    if len(description or "") < 50:
        flags.append("Job description is unusually short")

    return flags