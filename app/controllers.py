# -*- coding: UTF-8 -*-
from flask import render_template, session, request, Flask, jsonify, redirect, url_for
from app import app, facebook
from datetime import datetime
from time import time
import pusher


@app.route('/')

@app.route('/index')
def chat():
    return render_template("chat.html")

@app.route("/login", methods=["POST"])
def login():
    return facebook.authorize(callback = url_for("facebook_authorized",
        next=request.args.get("next") or request.referrer or None, _external=True))

@app.route("/login/authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        # return "Access denied: reason=%s error=%s" % (
        #         request.args["error_reason"],
        #         request.args["error_description"]
        #     )
        return redirect(url_for("chat.html"))
    session["oauth_token"] = (resp["access_token"], "")
    me = facebook.get("/me")

    session["username"] = me.data("name")
    session["user_id"] = me.data("id")
    return redirect(url_for("chat"))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get("oauth_token")
