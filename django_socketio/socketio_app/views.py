# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
async_mode = None

import os

from django.http import HttpResponse, JsonResponse
import socketio


basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(async_mode=async_mode, cors_allowed_origins="*")
thread = None


def index(request):
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)

    # with open(os.path.join(basedir, "index.html")) as f:
    #     return JsonResponse({"status": f.read()})
    # return HttpResponse(open(os.path.join(basedir, "static/index.html")))
    # return JsonResponse()
    # send rest api for sending messages to clients
    return JsonResponse({"status": "ok"})


# rest api for sending messages to clients
def send_message(request):
    rep = sio.emit("my_response", {"data": "Server generated event"}, namespace="/test")
    return JsonResponse({"status": rep})


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        sio.emit("my_response", {"data": "Server generated event"}, namespace="/test")


@sio.event
def my_event(sid, message, auth):
    print("message:", message)
    print("auth:", auth)
    sio.emit("my_event", {"data": "ola", "auth": auth})


@sio.event
def ping(sid):
    sio.emit("pong", {"data": "ola"}, room=sid)


@sio.event
def my_broadcast_event(sid, message):
    sio.emit("my_response", {"data": message["data"]})


@sio.event
def join(sid, message):
    sio.enter_room(sid, message["room"])
    sio.emit("my_response", {"data": "Entered room: " + message["room"]}, room=sid)


@sio.event
def leave(sid, message):
    sio.leave_room(sid, message["room"])
    sio.emit("my_response", {"data": "Left room: " + message["room"]}, room=sid)


@sio.event
def close_room(sid, message):
    sio.emit(
        "my_response",
        {"data": "Room " + message["room"] + " is closing."},
        room=message["room"],
    )
    sio.close_room(message["room"])


@sio.event
def my_room_event(sid, message):
    sio.emit("my_response", {"data": message["data"]}, room=message["room"])


@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)


@sio.event
def connect(sid, environ, auth):
    # get user name from session
    print("auth", auth)

    sio.emit("my_response", {"data": "Connected", "count": 0}, room=sid)


@sio.event
def disconnect(sid):
    print("Client disconnected")
