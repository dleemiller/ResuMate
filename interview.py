import logging
import sys

from tasks.interview_candidate import InterviewCandidate

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    job_listing = """
Machine Learning Engineer II
Save
Amazon.com Services LLC
Boulder, CO
Apply directly on Boulder, CO - Geebo
2 days ago
20–28 an hour
Full-time
Job highlights
Identified by Google from the original job post
Responsibilities
•
You will design and develop products that are at the heart of advertising - products that determine how billions of impressions are allocated to advertisers and how much advertisers pay for those impressions
•
You will have responsibility to help define requirements, create software designs, implement code to these specifications, define continuous integration testing and support products while deployed and used by our customers
•
You will have complete ownership of technology choices, architecture, testing of your features, code deployments into production environment and operations for the products you own
•
Your team will include machine learning scientists, product managers and other high performing engineers
	
Benefits
•
Estimated Salary: $20 to $28 per hour based on qualifications
Job description
Interested in green grass Machine Learning at internet scale?At Amazon Advertising, we are developing state-of-the-art large-scale computational advertising and machine learning applications using terabytes of data.
The Measurement And Data Science team develops algorithms and high performance, petabyte-scale distributed systems to measure outcomes of advertising.
Our systems process billions of ad impressions daily from across the internet to power our display advertising algorithms.
Our engineers work with machine learning scientists, economists and product managers creating measurement data for all of Amazon ad products.
You will design and develop products that are at the heart of advertising - products that determine how billions of impressions are allocated to advertisers and how much advertisers pay for those impressions.
You will have responsibility to help define requirements, create software designs, implement code to these specifications, define continuous integration testing and support products while deployed and used by our customers.
You will have complete ownership of technology choices, architecture, testing of your features, code deployments into production environment and operations for the products you own.
Your team will include machine learning scientists, product managers and other high performing engineers.
We're looking for SDEs interested in EMR / Spark, Sagemaker and other AWS, big-data, and ML technologies.
#madsjob.
Estimated Salary: $20 to $28 per hour based on qualifications
"""
    logger.info(job_listing)
    InterviewCandidate.interview(job_listing)
