import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

history_file = "mood_history.csv"

def save_mood(username, mood):
    entry = {
        'Username': username,
        'Mood': mood,
        'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    df = pd.DataFrame([entry])
    if os.path.exists(history_file):
        df.to_csv(history_file, mode='a', header=False, index=False)
    else:
        df.to_csv(history_file, index=False)

def get_history(username):
    if not os.path.exists(history_file):
        return [], None

    df = pd.read_csv(history_file)
    user_data = df[df['Username'] == username]

    if user_data.empty:
        return [], None

    # ✅ Ensure static/ folder exists before saving image
    static_dir = "static"
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    plot_path = f"{static_dir}/{username}_history.png"
    mood_counts = user_data['Mood'].value_counts()
    mood_counts.plot(kind='bar', title='Mood Frequency')
    plt.xlabel('Mood')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    return user_data.to_dict(orient='records'), plot_path
