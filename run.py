from app import create_app
from app.services.socket.socket import socketio

app, socketio  = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)
