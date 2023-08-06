#  License: GNU GPLv3+, Rodrigo Schwencke (Copyleft)

import os
import sys
from setuptools import find_packages, setup

username = os.getenv('TWINE_USERNAME')
password = os.getenv('TWINE_PASSWORD')

VERSION = '0.0.5'
GIT_MESSAGE_FOR_THIS_VERSION ="""Initial Plugin Commit
"""

if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep build"):
        print("'build' is not installed.\nUse `pip install build`.\nExiting.")
        sys.exit()
    if os.system("pip freeze | grep twine"):
        print("'twine' is not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python -m build")
    if ((username is not None) and (password is not None)):
        os.system(f"python -m twine upload dist/* -u {username} -p {password}")
    else:
        os.system(f"python -m twine upload dist/*")
    print(f"You probably also want to git push project, create v{VERSION} tag, and push it too :\n")
    gitExport=input("Do you want to do it right now? [y(default) / n]")
    if gitExport=="y" or gitExport=="":
        os.system(f"git add . && git commit -m 'v{VERSION} : {GIT_MESSAGE_FOR_THIS_VERSION}' && git push")
        os.system(f"git tag -a {VERSION} -m 'v{VERSION}'")
        os.system(f"git push --tags")
    else:
        print("You may still consider adding the following new tag later on :")
        print(f"git tag -a {VERSION} -m 'v{VERSION}'")
        print(f"git push --tags")
    sys.exit()

file = open("README.md", "r")
LONG_DESCRIPTION = file.read()
print("FOUND README.m, LONG_DESCRIPTION=", LONG_DESCRIPTION)
file.close()

del file

# file = open("requirements.txt", "r")
# DEPENDENCIES = file.readlines()
DEPENDENCIES = ["mkdocs>=1.0", "GitPython", "babel>=2.7.0"]
print("FOUND DEPENDENCIES=", DEPENDENCIES)
# file.close()

# del file

setup(
    name="mkdocs-revealjs",
    version=VERSION,
    description="Mkdocs plugin that enables displaying a Revealjs Presentation directly from an (mkdocs) markdown file.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    keywords="mkdocs revealjs presentation plugin",
    url="https://gitlab.com/rod2ik/mkdocs-revealjs",
    author="Rod2ik, aka Rodrigo Schwencke",
    author_email="rod2ik.dev@gmail.com",
    include_package_data=True,
    license="GPLv3+",
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 10',
    ],
    install_requires=DEPENDENCIES,
    packages=find_packages(),
    entry_points={
        "mkdocs.plugins": [
            "mkdocs-revealjs = mkdocs_revealjs.plugin:RevealjsPlugin"
        ]
    },
)

