from textblob import TextBlob
import random
from modules.face_detector import detect_emotion_from_face
from modules.voice_input import record_voice_to_text

# Enhanced mood detection with keyword mapping
#mood_keywords = {
    #"happy": ["happy", "joy", "glad", "cheerful", "delighted"],
    #"sad": ["sad", "depressed", "unhappy", "miserable", "down"],
    #"relaxed": ["relaxed", "calm", "peaceful", "chill", "laid-back"],
    #"excited": ["excited", "thrilled", "eager", "ecstatic", "hyped"],
    #"romantic": ["romantic", "love", "in love", "affection", "flirty"],
    #"anxious": ["anxious", "nervous", "worried", "stressed"],
    #"fear": ["fear", "afraid", "scared", "terrified"],
    #"disgust": ["disgust", "gross", "nasty", "repulsed"],
    #"surprised": ["surprised", "shocked", "amazed", "astonished"]
#}

mood_keywords = {

    "happy": [
        "happy", "joy", "joyful", "glad", "cheerful", "delighted",
        "smiling", "content", "pleased", "positive", "good mood",
        "awesome", "great", "feeling good", "so nice", "excited inside"
    ],

    "sad": [
        "sad", "depressed", "unhappy", "miserable", "down",
        "low", "cry", "crying", "tearful", "heartbroken",
        "lost", "lonely", "empty", "not feeling good",
        "feeling low", "bad day"
    ],

    "relaxed": [
        "relaxed", "calm", "peaceful", "chill", "laid-back",
        "comfortable", "stress free", "at ease",
        "cool", "slow", "easy", "normal mood"
    ],

    "excited": [
        "excited", "thrilled", "eager", "ecstatic", "hyped",
        "energetic", "pumped", "can't wait",
        "very happy", "overjoyed"
    ],

    "romantic": [
        "romantic", "love", "in love", "affection", "flirty",
        "crush", "missing you", "feeling close",
        "heart", "bond", "relationship"
    ],

    "anxious": [
        "anxious", "nervous", "worried", "stressed",
        "panic", "pressure", "tense", "overthinking",
        "fearful about future", "uneasy"
    ],

    "fear": [
        "fear", "afraid", "scared", "terrified",
        "panic attack", "horror", "danger",
        "shaking", "unsafe", "nightmare"
    ],

    "disgust": [
        "disgust", "gross", "nasty", "repulsed",
        "dirty", "hate it", "awful", "sickening"
    ],

    "surprised": [
        "surprised", "shocked", "amazed", "astonished",
        "unexpected", "wow", "can't believe",
        "suddenly", "unbelievable"
    ],

    "neutral": [
        "okay", "fine", "normal", "nothing special",
        "same as usual", "average", "not sure"
    ]
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
