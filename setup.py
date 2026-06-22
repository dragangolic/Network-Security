from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """Get the list of requirements from requirements.txt file."""
    
    requirement_lst: List[str]=[]
    try:
        with open("requirements.txt", "r") as file:
            # read lines from the file
            lines = file.readlines()
            # process each line
            for line in lines:
                requirement=line.strip()
                # skip empty lines and -e .
                if requirement and requirement!='-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found.")

setup(
    name="NetworkSecurity" ,
    version="0.0.1",
    author="GDSG",
    author_email="golicdragan0@mail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)