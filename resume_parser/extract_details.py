import re

SKILLS = [
    "Python", "Java", "SQL", "Machine Learning",
    "TensorFlow", "PyTorch", "NLP",
    "Computer Vision", "Django", "Flask",
    "Spring Boot", "Hibernate", "MySQL",
    "Git", "DSA", "Cisco", "Routing",
    "Switching", "TCP/IP", "Firewall"
]


def extract_details(text):

    details = {}

    # Name
    name = re.search(r"Name:\s*(.*)", text)

    if name:
        details["Name"] = name.group(1)

    # Email
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)

    if email:
        details["Email"] = email.group()

    # Phone
    phone = re.search(r"\d{10}", text)

    if phone:
        details["Phone"] = phone.group()

    # Skills
    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text.lower():
            found_skills.append(skill)

    details["Skills"] = found_skills

    return details