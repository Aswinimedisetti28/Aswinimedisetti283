# modules/community_service.py

COMMUNITY_DB = {}

def join_community(username, interests):
    COMMUNITY_DB[username] = {
        "username": username,
        "interests": interests,
        "joined": True
    }
    return True


def is_member(username):
    return username in COMMUNITY_DB


def get_member(username):
    return COMMUNITY_DB.get(username)
