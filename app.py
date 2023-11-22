import json
import logging
import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session
from flask import send_file, Response
from flask_socketio import SocketIO, emit

load_dotenv()

from tasks.parse_resume import ParseResume

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)
parser_logger = logging.getLogger("parser")

class SocketIOHandler(logging.Handler):
    def emit(self, record):
        parse_message = self.format(record)
        socketio.emit('parser_message', parse_message)

parser_logger.addHandler(SocketIOHandler())


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a random secret key
socketio = SocketIO(app)

@app.route('/')
def parse():
    return render_template('parse.html')

@app.route('/interview')
def interview():
    return render_template('interview.html')

@app.route('/revise')
def revise():
    return render_template('revise.html')

@app.route('/process_file', methods=['POST'])
def process_file():
    try:
        data = request.get_json()
        content = data.get('content', '')
        if not content:
            raise ValueError('File content is empty.')

        # Process the file content (add datetime information)
        processed_content = f"{datetime.now()} - {content}"

        # Store the processed content in the session
        session['processed_content'] = content

        return jsonify({'processed_content': processed_content})
    except Exception as e:
        import traceback
        parser_logger.error(traceback.format_exc())
        return jsonify({'error': str(traceback.format_exc())})

@socketio.on('connect')
def handle_connect():
    parser_logger.info('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    parser_logger.info('Client disconnected')

@socketio.on('parser_message')
def handle_parser_message(message):
    emit('parser_message', message)

@app.route('/run_code')
def run_code():
    try:
        resume_text = session.get('processed_content', '')

        parser_logger.info('Start parsing resume...')
        resume = ParseResume.parse(resume_text, parser_logger)
        parser_logger.info('Parsing completed successfully.')

        json_resume = resume.model_dump_json(indent=4)

        # Store the processed content in the session
        session['parsed_resume'] = json_resume

        return jsonify({'result': json_resume})
    except Exception as e:
        import traceback
        parser_logger.error(traceback.format_exc())
        return jsonify({'error': str(traceback.format_exc())})


@app.route('/download_parsed_resume')
def download_parsed_resume():
    json_data = session.get('parsed_resume')
    if json_data:
        result = json.dumps(json_data)
        return Response(
            result,
            mimetype="application/json",
            headers={"Content-Disposition": "attachment;filename=parsed_resume.json"}
        )
    else:
        return "No data found", 404


if __name__ == '__main__':
    socketio.run(app, debug=True)
