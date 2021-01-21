from flask import Flask, render_template, session, g
from model import User


users = []
users.append(User(user_id=1, username='jacob', password='secretword'))
users.append(User(user_id=2, username='testuser', password='EbpucVzUP5cvsYha0E9i'))

app = Flask(__name__)
app.secret_key = 'minidemo'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/policy')
def policy():
    return render_template('policy.html')


if __name__ == "__main__":
    app.run(debug=True)