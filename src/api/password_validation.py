# ~/reddit_sentiment_tracker/src/api/password_validation.py

from zxcvbn import zxcvbn

def validate_password_strength(password: str, min_score: int = 3):
    """ 
    evaluate password strength with zxcvbn and setting minimum score to 3

    Password strength scale
        0 — very weak
        1 — weak
        2 — fair
        3 — good
        4 — strong
    """

    result = zxcvbn(password)
    score = result["score"]
    feedback = result["feedback"]

    if score < min_score:
        suggestions = feedback.get("suggestions", [])
        warning = feedback.get("warning", "")
        # Combine all feedback into a readable message
        message = " ".join([warning] + suggestions).strip()

        raise ValueError(f"Weak password: {message or 'Try a longer or more complex password.'}")

    return True
