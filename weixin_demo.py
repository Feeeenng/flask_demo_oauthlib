#coding=utf-8
from __future__ import unicode_literals


from flask import Flask
from flask import Markup
from flask import redirect
from flask import request
from flask import jsonify
from weixin.client import WeixinAPI
from weixin.oauth2 import OAuth2AuthExchangeError
app = Flask(__name__)


APP_ID = ''
APP_SECRET = ''

#假设我本地的IP为192.168.0.50， 微信开放平台填写192.168.0.50,而这里的回调地址就是http://192.168.0.50/authorization,并且一定要以http:// or https://打头
REDIRECT_URI = 'http://192.168.0.50/authorization'

@app.route("/authorization")
def authorization():
    code = request.args.get('code')
    api = WeixinAPI(appid=APP_ID,
	    app_secret=APP_SECRET,
	    redirect_uri=REDIRECT_URI)
    auth_info = api.exchange_code_for_access_token(code=code)
    api = WeixinAPI(access_token=auth_info['access_token'])
    resp = api.user(openid=auth_info['openid'])
    return jsonify(resp)

@app.route("/login")
def login():
    api = WeixinAPI(appid=APP_ID,
	    app_secret=APP_SECRET,
	    redirect_uri=REDIRECT_URI)
    redirect_uri = api.get_authorize_login_url(scope=("snsapi_login",))
    return redirect(redirect_uri)
@app.route("/")
def hello():
    return Markup('<a href="%s">weixin login!</a>') % '/login'
if __name__ == "__main__":
    app.run(debug=True)
