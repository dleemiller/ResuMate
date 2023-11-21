import logging
import sys

from tasks.parse_resume import ParseResume

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    resume_text = """
Advanced D. Graduate
1234 Spring Street, Davis, California 95616
(530) 555-223 adgraduate@ucdavis.edu
http://www.linkedin.com/in/advancedgraduate
OBJECTIVE: Project Manger, General Electric Power Systems
Mechanical Engineering Ph.D. (June 20XX) with 4 years industry experience in project management, strategic planning, research
and development. Expertise in power systems and distributed grid infrastructure. Management and training experience in production
and use of technology for engineers and customers. Interested in globalization and international issues. Additional skills include:
• SolidWorks (CAD)
• COMSOL (FEM/FEA)
• MS Office Suite and database
• Labview
• Oral & written presentations
• Matlab
• Vibration test/analysis
• L-edit (CAD)
• Mathcad
• Machine shop/fabrication
• Origin
• Speak basic German
EDUCATION
PhD in Mechanical Engineering – University of California, Davis, June 20XX
Master of Business Administration in Finance & International Management – University of California, Davis, June 20XX
Bachelor of Science in Mechanical Engineering – University of California, Davis, June 20XX
PROFESSIONAL EXPERIENCE
Manager, Business Development
Anuvu, Inc. – Sacramento, California September 20XX- present
• Managed technological/financial development of PEM hydrogen fuel cell applications in power systems.
• Created complex engineering models and financial programs for technology/investment valuation.
• Presented grid infrastructure engineering/financial model to domestic and foreign business partners.
• Wrote business plan for a $4.5 M OEM hydrogen fuel cell contract.
• Negotiated contract for product testing and integration with OEM partner and State Testing Group.
• Developed network and relationship with Original Equipment Manufacturer (OEM) customers.
Research and Development Engineer
Medtronic Vascular, Inc. – Santa Rosa, California June 20XX- September 20XX
• Patented mechanical design of device and led project from inception to successful International clinical use.
• Developed processes, equipment, and trained personnel for market release of medical device product lines.
• Managed production line and personnel while creating and fabricating support tooling and equipment.
• Coordinated joint R&D/Manufacturing efforts to effectively meet company production deadlines.
• Wrote procedures for processes and data collection for GMP and ISO-900X quality systems.
Total Quality Manager – Intern
Hunter Innovations Inc. – Sacramento, California June 20XX- December 20XX, June 20XX- December 20XX
• Organized and led training of Hunter Associates in Quality Control and GMP systems.
• Wrote and implemented Good Manufacturing Practice (GMP) System for FDA regulatory approval of artificial
hip joint implant sales and manufacturing.
• Designed and programmed components of CNC lathe and mill manufacturing resulting in sales estimated at
$10,000/month for these components.
Project Engineer – Intern
Ames Co./Fluid Control Systems – Woodland, California June 20XX- September 20XX
• Leader of “Introduction to Production” team and responsible for vendor communications.
• Created and maintained engineering documentation, bill of materials, and bill of operations.
• Researched and designed prototype backflow check valves and led pilot production.
PATENTS/PUBLICATIONS
List patents and publications here
PROFESSIONAL AFFILIATIONS/COMMUNITY SERVICE
Institute of Industrial Engineering - Engineers Without Borders
"""
    logger.info(resume_text)
    skills = ParseResume.parse(resume_text)
    print(skills)
