"""
Aim is to create a webpage that is constantly updated with logs from a background python process.
"""

from flask_socketio import SocketIO, emit
from flask import Flask, render_template
from time import sleep
from threading import Thread, Event
import subprocess,os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

thread = Thread()
thread_stop_event = Event()

# Last modified time of log file (initially set to 0)
LAST_MODIFIED = 0.0

class LastLine(Thread):
    def __init__(self):
        self.delay = 1
        super(LastLine, self).__init__()

    def last_line(self):
        global LAST_MODIFIED

        #infinite loop of checking logs
        while not thread_stop_event.isSet():
            modified = os.path.getmtime("logs.txt")

            if modified != LAST_MODIFIED:
                LAST_MODIFIED = modified
                line = subprocess.check_output(['tail', '-1', "logs.txt"])
                # printing last line of log file
                print(line)
                socketio.emit('newnumber', {'number': str(line)}, broadcast = False ,namespace='/test')

            sleep(self.delay)

    def run(self):
        self.last_line()


@app.route('/')
def index():
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')


# for testing/demonstration purpose... you can append data to end of log file using this end point(url)
@app.route('/append/<text>', methods=['GET'])
def append_text(text):
    with open("logs.txt", "a") as myfile:
        myfile.write("%s\n" % text)

    return "'%s' appended at the end of file" % text


@socketio.on('my_event', namespace='/test')
def test_message(message):
    emit('my_response', {'data': message['data']}, broadcast = False)


@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global object and variables
    global thread

    print('Client connected')

    line = subprocess.check_output(['tail', '-1', "logs.txt"])
    emit('my_response', {'data': str(line)}, broadcast = False)

    if not thread.isAlive():
        print("Starting Thread")
        thread = LastLine()
        thread.start()


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
