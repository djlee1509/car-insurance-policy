from flask import Flask, render_template, session, g, request, redirect, url_for
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


@app.route('/login', methods=['Get', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form.get('username', None)
        password = request.form.get('password', None)

        current_users = [x for x in users if x.username == username]

        if not current_users:
            return redirect(url_for('login'))

        current_user = current_users[0]
        if current_user and current_user.password == password:
            session['user_id'] = current_user.id
            return redirect(url_for('policy'))

    return render_template('login.html')


@app.route('/policy')
def policy():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('policy.html')


if __name__ == "__main__":
    app.run(debug=True)