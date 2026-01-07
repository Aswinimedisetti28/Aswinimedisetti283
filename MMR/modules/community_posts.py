# modules/community_posts.py
from datetime import datetime
import uuid

POSTS_DB = []   # Later MongoDB collection

def add_post(username, content, mood):
    post = {
        "id": str(uuid.uuid4()),
        "username": username,
        "content": content,
        "mood": mood,
        "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "comments": []
    }
    POSTS_DB.insert(0, post)
    return post


def get_all_posts():
    return POSTS_DB


def add_comment(post_id, username, comment):
    for post in POSTS_DB:
        if post["id"] == post_id:
            post["comments"].append({
                "username": username,
                "comment": comment,
                "time": datetime.now().strftime("%I:%M %p")
            })
            return True
    return False
