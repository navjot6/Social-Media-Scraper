def classify_category(text): 
    text = text.lower() 
    if "renewal" in text: 
        return "Renewal" 
    elif "appointment" in text: 
        return "Appointments" 
    elif "tatkal" in text: 
        return "Tatkal" 
    elif "visa" in text: 
        return "Visa" 
    elif "travel" in text: 
        return "Travel Issues" 
    elif "government" in text: 
        return "Government Announcements" 
    elif "fraud" in text or "scam" in text: 
        return "Scams/Fraud" 
    return "News"