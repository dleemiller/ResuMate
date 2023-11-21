import logging
import sys

from tasks.models.resume import Resume
from tasks.interview_candidate import InterviewCandidate

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    with open("example_job.txt", "r") as fh:
        job_listing = fh.read()

    with open("resume.json", "r") as fh:
        import json

        resume_json = json.load(fh)

    print(dir(Resume))
    resume = Resume.model_validate_json(resume_json)

    logger.info(job_listing)
    logger.info(resume.short_version())
    InterviewCandidate.interview(resume, job_listing)
