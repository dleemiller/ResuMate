import json
import logging
import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session
from flask import send_file, Response
from flask_socketio import SocketIO, emit
import os
from werkzeug.utils import secure_filename

from parse_blueprint import parse_bp


load_dotenv()


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)
parser_logger = logging.getLogger("parser")


class SocketIOHandler(logging.Handler):
    """
    A logging handler that streams logs over a websocket connection using the flask-socketio library.

    This class extends the logging.Handler base class and overrides the emit method to send log records as messages through a socket.io connection.
    It is designed to be used with Flask applications, which allows for real-time streaming of logs from the server to connected clients over websockets.

    Attributes:
        None

    Methods:
        emit(record) - Sends log records through a socket.io connection.
    """

    def emit(self, record):
        """
        Overrides the logging.Handler's emit method to send log records as messages over a websocket.

        The method formats a log record into a message using the format method inherited from the base class,
        and then emits this message on the 'parser_message' channel of the socketio connection.

        Args:
            record (logging.LogRecord): A log record to be formatted and sent.

        Returns:
            None
        """
        parse_message = self.format(record)
        socketio.emit("parser_message", parse_message)


parser_logger.addHandler(SocketIOHandler())


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("RESUMATE_SECRET_KEY")
socketio = SocketIO(app)

app.register_blueprint(parse_bp, url_prefix="/parse")

@app.route("/")
def parse():
    return render_template("parse.html")


@app.route("/interview")
def interview():
    return render_template("interview.html")

@app.route("/start-interview", methods=["POST"])
def start_interview():
    print("interview click")
    return jsonify({"message": "started"}), 200


@app.route("/revise")
def revise():
    return render_template("revise.html")

@socketio.on("connect")
def handle_connect():
    parser_logger.info("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    parser_logger.info("Client disconnected")

@socketio.on("parser_message")
def handle_parser_message(message):
    emit("parser_message", message)


if __name__ == "__main__":
    socketio.run(app, debug=True)
