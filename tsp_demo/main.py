from flask import Flask
from flask import request
from flask import render_template,session, request, copy_current_request_context
from flask import jsonify
from threading import Lock
from flask_socketio import SocketIO, emit, join_room, leave_room,close_room, rooms, disconnect

import json
import random
import json_graph as graph
import sa_tsp as graph

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/draw_nodes")
def draw_nodes():
    maule_graph=graph.data_loader('static/maule.geojson')
    return jsonify(maule_graph.draw_nodes())

@socketio.on('connect')  
def test_connect():
    print('hola')

#@app.route("/draw_path",methods = ['GET','POST'])
@socketio.on('solve')
def draw_path():
    #eta = int(request.form['eta'])
    maule_graph=graph.data_loader('static/maule.geojson')
    step=0
    for tour,temperature,fitness in maule_graph.solver():
        if(step % 1000 == 0):
            #emit('update',temperature)
            emit('update',{'temperature':temperature,'fitness':fitness})
            #print('tour',tour)
            #print('length:',fitness)
        step=step+1
    emit('tour', maule_graph.draw_path(tour),json=True)
    return tour,temperature,fitness

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    #app.run(port=5000, debug=True)
    socketio.run(app,port=5000)