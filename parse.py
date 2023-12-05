import logging
import sys

from tasks.parse_resume import ParseResume

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    with open("examples/example_resume.txt", "r") as fh:
        resume_text = fh.read()

    logger.info(resume_text)
    resume = ParseResume.parse(resume_text, logger)
    with open("examples/resume.json", "w") as fh:
        import json

        json.dump(resume.json(), fh, indent=4)
