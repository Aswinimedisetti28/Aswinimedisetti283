# modules/profile_service.py

# TEMP storage (demo purpose)
USER_PROFILES = {}

def get_user_profile(username):
    if username not in USER_PROFILES:
        USER_PROFILES[username] = {
            "username": username,
            "email": f"{username}@melodymist.com",
            "joined": "Aug 2025",
            "account_type": "Local",
            "favorite_genre": "Lo-Fi",
            "top_mood": "Happy",
            "streak": 21,
            "accuracy": "92%",
            "last_login": "Just now"
        }
    return USER_PROFILES[username]



def update_user_profile(username, email, favorite_genre):
    if username in USER_PROFILES:
        USER_PROFILES[username]["email"] = email
        USER_PROFILES[username]["favorite_genre"] = favorite_genre
        return True
    return False
