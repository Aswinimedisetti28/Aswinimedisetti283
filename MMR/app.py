from flask import Flask, render_template, request, redirect, session, url_for
from modules import auth_module, emotion_detector, music_recommender, history_tracker
import os
from modules.tts_output import speak
from modules.profile_service import get_user_profile, update_user_profile
import requests
from modules.community_service import join_community, is_member, get_member
from modules.community_posts import add_post, get_all_posts, add_comment





app = Flask(__name__)
app.secret_key = 'supersecretkey'



GITHUB_CLIENT_ID = "Ov23liPn8byG9DTJTuU7"
GITHUB_CLIENT_SECRET = "8cd2b144afb256e508ef167c78ba38c8010bde75"


@app.route("/auth/github")
def github_login():
    github_auth_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        "&scope=user:email"
    )
    return redirect(github_auth_url)


@app.route("/auth/github/callback")
def github_callback():
    code = request.args.get("code")

    # Exchange code for access token
    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
        },
    ).json()

    access_token = token_response.get("access_token")

    # Get user info
    user_response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    username = user_response.get("login")
    email = user_response.get("email") or f"{username}@github.com"

    # 🔑 Auto signup or login
    if not auth_module.user_exists(username):
        auth_module.signup(username, "github_oauth")

    session["username"] = username
    return redirect("/land")



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_module.login(username, password):
            session['username'] = username
            return redirect('/home')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    if auth_module.signup(username, password):
        session['username'] = username
        return redirect('/home')
    else:
        return render_template('login.html', error="Username already exists")

@app.route('/home', methods=['GET'])
def home():
    if 'username' not in session:
        return redirect('/')
    return render_template('land.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'username' not in session:
        return redirect('/')

    input_method = request.form.get('input_method')
    mood = "neutral"
    text_input = ""

    if input_method == "text":
        text_input = request.form.get('text_input', '')
        mood = emotion_detector.detect_text_mood(text_input)

    elif input_method == "voice":
        text_input = emotion_detector.voice_to_text()
        mood = emotion_detector.detect_text_mood(text_input)

    elif input_method == "face":
        mood = emotion_detector.detect_face_mood()

    history_tracker.save_mood(session['username'], mood)
    return render_template("result.html", mood=mood, spoken_text=text_input, songs=None, preference=None)


@app.route('/recommend', methods=['POST'])
def recommend():
    if 'username' not in session:
        return redirect('/')
    
    mood = request.form['mood']
    preference = request.form['preference']

    # Get songs based on preference
    songs = music_recommender.get_recommendations(mood, preference)

    return render_template("result.html", mood=mood, spoken_text="", songs=songs, preference=preference)



@app.route('/history')
def history():
    if 'username' not in session:
        return redirect('/')
    data, plot_path = history_tracker.get_history(session['username'])
    return render_template("history.html", mood_data=data, plot_path=plot_path)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    # Session check
    if 'username' not in session:
        return redirect('/')

    username = session['username']

    # Get profile data
    user_profile = get_user_profile(username)

    return render_template(
        'profile.html',
        username=user_profile['username'],
        email=user_profile['email'],
        joined=user_profile['joined'],
        account_type=user_profile['account_type'],
        favorite_genre=user_profile['favorite_genre'],
        top_mood=user_profile['top_mood'],
        streak=user_profile['streak'],
        accuracy=user_profile['accuracy'],
        last_login=user_profile['last_login']
    )

@app.route('/edit-profile', methods=['POST'])
def edit_profile():
    if 'username' not in session:
        return redirect('/')

    username = session['username']

    email = request.form.get('email')
    favorite_genre = request.form.get('favorite_genre')

    update_user_profile(username, email, favorite_genre)

    return redirect(url_for('profile'))

@app.route('/community')
def community():
    if 'username' not in session:
        return redirect('/')

    username = session['username']
    joined = is_member(username)
    member = get_member(username) if joined else None

    return render_template(
        'community.html',
        joined=joined,
        member=member,
        username=username
    )


@app.route('/join-community', methods=['POST'])
def join_community_route():
    if 'username' not in session:
        return redirect('/')

    interests = request.form.getlist('interests')
    join_community(session['username'], interests)

    return redirect('/community')


@app.route('/community-feed')
def community_feed():
    if 'username' not in session:
        return redirect('/')

    posts = get_all_posts()
    return render_template(
        'community_feed.html',
        posts=posts,
        username=session['username']
    )

@app.route('/add-post', methods=['POST'])
def add_post_route():
    if 'username' not in session:
        return redirect('/')

    content = request.form.get('content')
    mood = request.form.get('mood')

    if content:
        add_post(session['username'], content, mood)

    return redirect('/community-feed')

@app.route('/add-comment', methods=['POST'])
def add_comment_route():
    if 'username' not in session:
        return redirect('/')

    post_id = request.form.get('post_id')
    comment = request.form.get('comment')

    if comment:
        add_comment(post_id, session['username'], comment)

    return redirect('/community-feed')


if __name__ == "__main__":
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True)
