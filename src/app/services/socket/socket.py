from flask_socketio import SocketIO

socketio = SocketIO()


def init_socket(app):
    socketio.init_app(app)


@socketio.on("loading_config")
def loadingConfig(message):
    socketio.emit("loading_config", message)
