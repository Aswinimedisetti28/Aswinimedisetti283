from textblob import TextBlob
import random
from modules.face_detector import detect_emotion_from_face
from modules.voice_input import record_voice_to_text

# Enhanced mood detection with keyword mapping
mood_keywords = {
    "happy": ["happy", "joy", "glad", "cheerful", "delighted"],
    "sad": ["sad", "depressed", "unhappy", "miserable", "down"],
    "angry": ["angry", "furious", "mad", "irritated", "annoyed"],
    "relaxed": ["relaxed", "calm", "peaceful", "chill", "laid-back"],
    "excited": ["excited", "thrilled", "eager", "ecstatic", "hyped"],
    "romantic": ["romantic", "love", "in love", "affection", "flirty"],
    "anxious": ["anxious", "nervous", "worried", "stressed"],
    "fear": ["fear", "afraid", "scared", "terrified"],
    "disgust": ["disgust", "gross", "nasty", "repulsed"],
    "surprised": ["surprised", "shocked", "amazed", "astonished"]
}

def detect_text_mood(text):
    text_lower = text.lower()
    blob = TextBlob(text_lower)
    polarity = blob.sentiment.polarity

    # First: Match against keywords
    for mood, keywords in mood_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            return mood

    # Fallback: Use polarity
    if polarity > 0.5:
        return "excited"
    elif polarity > 0.2:
        return "happy"
    elif polarity < -0.5:
        return "angry"
    elif polarity < -0.2:
        return "sad"
    else:
        return "neutral"

def detect_face_mood():
    try:
        return detect_emotion_from_face()
    except Exception:
        return random.choice(list(mood_keywords.keys()) + ["neutral"])

def voice_to_text():
    try:
        return record_voice_to_text()
    except Exception:
        return "I couldn't hear you properly"
