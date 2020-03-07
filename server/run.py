from app import app,socketio,client

if __name__ == '__main__':
    client.loop_start()
    client.subscribe('zzz-adios')
    socketio.run(app,port=5000)


