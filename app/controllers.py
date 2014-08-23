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
        sesion["oauth_token"] = (resp["access_token"], "")
        me = facebook.get("/me")
        return str(me.data)

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get("oauth_token")


# @app.route("/login", methods=["POST"])
# def login():
#     if "nickname" in request.form:
#         nickname = request.form.get("nickname")
#         session["nickname"] = nickname
#         data = {"nickname": nickname, "success": True, "message": "반가워요!"}
#         return jsonify(data)
#     else:
#         return jsonify(success=False)

# @app.route("/pusher/auth", methods=["POST"])
# def authenticate():
#     p = pusher.Pusher(
#         app_id='86072',
#         key='9f04d3ecab45dc1b9f18',
#         secret='faf0e19b31b53cfa4b60'   
#     )
#     socket_id = request.form.get("socket_id")
#     channel_name = request.form.get("channel_name")
#     authentication_name = session["nickname"]

#     channel_data = {"user_info": {"username": authentication_name}}
#     channel_data["user_id"] = authentication_name # should be something unique!
#     response = p[channel_name].authenticate(socket_id, channel_data)

#     return jsonify(response)

# @app.route("/new_message", methods=["POST"])
# def new_message():
#     p = pusher.Pusher(
#         app_id='86072',
#         key='9f04d3ecab45dc1b9f18',
#         secret='faf0e19b31b53cfa4b60'   
#     )
#     username = session["nickname"]
#     message = request.form.get("message")
#     t = time()
#     time_record = datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S")
#     p["presence-miniming"].trigger("new_message", {"username": username, "message": message, "time": time_record})
#     return jsonify(success=True)

# @app.route("/send")
# def send():
#     name = request.args.get("username")
#     message = request.args.get("usermessage")

#     p = pusher.Pusher(
#         app_id='86072',
#         key='9f04d3ecab45dc1b9f18',
#         secret='faf0e19b31b53cfa4b60'   
#     )

#     p['jeungmin_seulki'].trigger('my_event',
#         {'name': name, 'message': message })
#     return "jeungmin"