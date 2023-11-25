from flask_socketio import SocketIO

socketio = None

def init_socket(app):
    global socketio
    socketio = SocketIO(app)
    
    @socketio.on('message')
    def handle_message(data):
        print('received message: ' + data)


