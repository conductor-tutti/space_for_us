# -*- coding: UTF-8 -*-
from flask import render_template, session, request, Flask, jsonify, redirect, url_for
from app import app, facebook
from datetime import datetime
from time import time
import pusher


@app.route('/')

@app.route('/index')
def index():
    return render_template("login.html")

@app.route("/login")
def login():
    return facebook.authorize(callback = url_for("oauth_authorized",
        next=request.args.get("next") or request.referrer or None,
        _external=True))

@app.route("/login/authorized")
@facebook.authorized_handler
def oauth_authorized(resp):
    if resp is None:
        # return "Access denied: reason=%s error=%s" % (
        #         request.args["error_reason"],
        #         request.args["error_description"]
        #     )
        return redirect(url_for("chat.html"))
    session["facebook_token"] = (
        resp["oauth_token"],
        resp["oauth_token_secret"]
    )
    me = facebook.get("/me")

    session["username"] = me.data("name")
    session["user_id"] = me.data("id")
    return redirect(url_for("chat"))

# OAuth uses a token and a secret
# to figure out who is connecting to the remote application.
# After authentication/authorization, this information is passed to a function on your side
# and it is your responsibility to remember it.
@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get("oauth_token")
