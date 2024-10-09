from flask_socketio import SocketIO, emit
def ws(application):
    socketio = SocketIO(application)
    return socketio