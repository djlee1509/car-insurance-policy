from flask import Flask, render_template, session, g, request, redirect, url_for
from model import User
import requests
from werkzeug.security import safe_str_cmp


users = [
    User(user_id=1, username='jacob', password='secretword'),
    User(user_id=2, username='testuser', password='EbpucVzUP5cvsYha0E9i')
]

app = Flask(__name__)
app.secret_key = 'minidemo'


def get_policy_details(username, password):
    """
    Returns policy details in json form given username and password.
    """

    auth_url = "https://api.bybits.co.uk/auth/token"
    policy_url = "https://api.bybits.co.uk/policys/details"

    post_body = {
        "username": username,
        "password": password,
        "type": "USER_PASSWORD_AUTH"
    }

    auth_headers = {"environment": "mock"}
    auth_response = requests.post(auth_url, data=post_body, headers=auth_headers).json()

    access_token = auth_response["access_token"]
    authorization_header = f"Bearer {access_token}"

    policy_headers = {"environment": "mock", "Authorization": authorization_header}

    policy_req = requests.get(policy_url, headers=policy_headers)
    policy_json = policy_req.json()

    return policy_json


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if safe_str_cmp(x.id, session['user_id'])][0]
        g.user = user


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Redirects to policy page after user authenticated.
    If user is failed to authenticate, it stays at login page for another try.
    """
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form.get('username', None)
        password = request.form.get('password', None)

        current_users = [x for x in users if safe_str_cmp(x.username, username)]

        if not current_users:
            return redirect(url_for('login'))

        current_user = current_users[0]
        if current_user and safe_str_cmp(current_user.password, password):
            session['user_id'] = current_user.id
            return redirect(url_for('policy'))

    return render_template('login.html')


@app.route('/policy', methods=['GET'])
def policy():
    """
    Render Policy templates with data.
    """
    if not g.user:
        return redirect(url_for('login'))

    policy_detail = get_policy_details(g.user.username, g.user.password)

    policy_dict = policy_detail['policy']
    car = policy_detail['vehicle']
    address = policy_dict['address']

    return render_template('policy.html', policy=policy_dict, vehicle=car, address=address)


if __name__ == "__main__":
    app.run()