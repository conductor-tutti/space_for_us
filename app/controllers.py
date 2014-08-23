# -*- coding: UTF-8 -*-
from flask import render_template, session, request, Flask, jsonify
from app import app, facebook
from datetime import datetime
from time import time
import pusher

app.secret_key = "You will never know this key"

@app.route('/')

@app.route('/index')
def index():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return facebook.authorize(callback = url_for("facebook_authorized",
        next=request.args.get("next") or request.referrer or None, _external=True))

@app.route("/login/authorized")
@facebook.authorized_handler
def facebook_authorized_handler(resp):
    if resp is None:
        return "Access denied: reason=%s error=%s" % (
                request.args["error_reason"],
                request.args["error_description"]
            )
    session["oauth_token"] = (resp["access_token"], "")
    me = facebook.get("/me")
    return str(me.data)

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get("oauth_token")
