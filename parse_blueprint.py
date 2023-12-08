from flask import Blueprint, request, jsonify, session, Response
import os
import traceback
import json
from werkzeug.utils import secure_filename
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from tasks.parse_resume import ParseResume


parse_bp = Blueprint('parse', __name__)

@parse_bp.route("/process_file", methods=["POST"])
def process_file() -> tuple:
    """Processes a file by adding current date and time to its content.

    Returns:
        A JSON object with the processed content or an error message if any exception occurred.
    """
    try:
        data = request.get_json()  # type: dict
        content = data.get("content", "")  # type: str
        if not content:
            raise ValueError("File content is empty.")

        # Process the file content (add datetime information)
        processed_content = f"{datetime.now()} - {content}"  # type: str

        # Store the processed content in the session
        session["processed_content"] = content  # type: str

        return jsonify({"processed_content": processed_content}), 200
    except Exception as e:
        import traceback

        parser_logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@parse_bp.route("/process_json", methods=["POST"])
def process_json() -> tuple:
    """Processes a JSON file by adding to a session variable called `parsed_resume`.

    Returns:
        A JSON object with the processed content or an error message if any exception occurred.
    """
    try:
        data = request.get_json()  # type: dict

        if not data:
            raise ValueError("JSON data is empty.")

        # Process and store the parsed JSON in the session variable `parsed_resume`
        session["parsed_resume"] = data

        return jsonify({"processed_content": data}), 200
    except Exception as e:
        import traceback

        parser_logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500



@parse_bp.route("/run_code")
def run_code():
    try:
        resume_text = session.get("processed_content", "")

        parser_logger.info("Start parsing resume...")
        resume = ParseResume.parse(resume_text, parser_logger)
        parser_logger.info("Parsing completed successfully.")

        json_resume = resume.model_dump_json(indent=4)

        # Store the processed content in the session
        session["parsed_resume"] = json_resume

        return jsonify({"result": json_resume})
    except Exception as e:
        import traceback

        parser_logger.error(traceback.format_exc())
        return jsonify({"error": str(traceback.format_exc())})


@parse_bp.route("/download_parsed_resume")
def download_parsed_resume():
    """
    This function handles the route for downloading a JSON file of parsed resume data.

    It retrieves 'parsed_resume' from the session, converts it to json if exists and
    returns it as a response with mimetype "application/json". If no data is found, it will return
    a message saying "No data found" along with status code 404.

    Returns:
        A JSON file or an error message (str), with appropriate HTTP status code (int).
    """

    json_data = session.get("parsed_resume")
    if json_data:
        result = json.dumps(json_data)
        return Response(
            result,
            mimetype="application/json",
            headers={"Content-Disposition": "attachment;filename=parsed_resume.json"},
        )
    else:
        return "No data found", 404


@parse_bp.route("/save_parsed_resume", methods=["POST"])
def save_parsed_resume():
    """
    This function handles the route for saving a JSON file of parsed resume data.

    It retrieves 'parsed_resume' from the session, converts it to json if exists and
    saves it to disk in the cache folder.

    Returns:
        successful http code from flask
    """
    try:
        parsed_resume = session.get("parsed_resume")
        cache_dir = os.getenv("RESUMATE_CACHE_DIR", "cache")

        if parsed_resume:
            filename = secure_filename("parsed_resume.json")

            with open(os.path.join(cache_dir, filename), "w") as write_file:
                json.dump(
                    parsed_resume, write_file, indent=4
                )  # Dump directly to file without converting to string
        return jsonify({"status": "success"}), 200

    except Exception as e:
        logger.exception("An error occurred while saving parsed resume")
        return (
            jsonify({"error": "Failed to save parsed resume", "message": str(e)}),
            500,
        )

