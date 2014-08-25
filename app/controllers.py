# -*- coding: UTF-8 -*-
from flask import render_template, session, request, Flask, jsonify, redirect, url_for
from flask_oauth import OAuth
from app import app, facebook
from datetime import datetime
from time import time
import pusher

import logging

@app.route('/')

@app.route('/index')
def index():
    return render_template("login.html")

@app.route("/login")
def login():
    return facebook.authorize(callback = url_for("facebook_authorized",
        next=request.args.get("next") or request.referrer or None,
        _external=True))

@app.route("/login/authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return redirect(url_for("chat.html"))
    session["oauth_token"] = (resp["access_token"], "")
    me = facebook.get("/me")
    logging.debug(me.data)

    session["username"] = me.data["name"]
    session["user_id"] = me.data["id"]
    return redirect(url_for("chat"))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get("oauth_token")

@app.route("/chat")
def chat():
    return render_template("chat.html")
