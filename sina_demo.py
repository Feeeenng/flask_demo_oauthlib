from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
import json

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

weibo = oauth.remote_app(
    'weibo',
    consumer_key='你的key',
    consumer_secret='你的secret',
    request_token_params={'scope': 'email'},
    base_url='https://api.weibo.com/2/',
    authorize_url='https://api.weibo.com/oauth2/authorize',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://api.weibo.com/oauth2/access_token',
    # since weibo's response is a shit, we need to force parse the content
    content_type='application/json',
)


@app.route('/')
def index():
    if 'oauth_token' in session:
        access_token = session['oauth_token'][0]
        u_id = session['uid']

	data = {"access_token":access_token,"uid":u_id}
	resp = weibo.get('users/show.json',data)
	#resp = weibo.get('users/show.json',data={"access_token":access_token})
	return jsonify(resp.data)
    return redirect(url_for('login'))


@app.route('/l')
def login():
    return weibo.authorize(callback='你需要填写的回调地址', _external=True)


@app.route('/logout')
def logout():
    session.pop('oauth_token', None)
    return redirect(url_for('index'))

#这里一般就是你在新浪填写的回调地址
@app.route('/login')
@app.route('/login/authorized')
def authorized():
    print u'sdfasd'
    resp = weibo.authorized_response()
    print resp
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    session['uid'] = resp['uid']
    return redirect(url_for('index'))


@weibo.tokengetter
def get_weibo_oauth_token():
    return session.get('oauth_token')


def change_weibo_header(uri, headers, body):
    """Since weibo is a rubbish server, it does not follow the standard,
    we need to change the authorization header for it."""
    auth = headers.get('Authorization')
    if auth:
        auth = auth.replace('Bearer', 'OAuth2')
        headers['Authorization'] = auth
    return uri, headers, body

weibo.pre_request = change_weibo_header


if __name__ == '__main__':
    app.run(port=81, host='0.0.0.0')
