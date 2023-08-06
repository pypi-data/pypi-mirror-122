# coding: utf-8
import setuptools, os
import sys
import re

packagename= "termpix"
programname= "termpix.py"
homepage="https://github.com/Ericrus/termpix"
project_urls={"Maintainer Repository":"https://github.com/tjnh05/termpix"}
short_description="This program play video by tty and capable to output video into text file."
keywords = ['termpix','terminal', 'tty', 'video']
version = "0.5.2"
package_data={
        'termpix': ['termpix.py', 'demo.png', 'demo.py', 'today.sh', 'requirements.txt']
    }
entry_points = {
        "console_scripts": [
            "termpix=termpix.termpix:main"
        ]
    }

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, packagename, programname)) as f:
    for line in f.readlines():
        if "__author__" in line:
            author, mail = re.split('[<>]',
                               line.strip().replace('"', '').split('=')[-1])[:-1]
        if "__version__" in line:
            version = line.strip().replace('"', '').split()[-1]
            break


path = os.path.join(os.getcwd(),packagename, "README.md")
requiredments = os.path.join(os.getcwd(),packagename, "requirements.txt")

with open(path, "r", encoding='utf-8') as fh:
    long_description = ''.join(fh.readlines()[:-1])

with open(requiredments, "r", encoding='utf-8') as fh:
    requiredpackages = [ line.strip() for line in fh.readlines() ]


setuptools.setup(
    name=packagename,
    version=version,
    author=author.strip(),
    author_email=mail.strip(),
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=homepage,
    project_urls=project_urls,
    #license = 'MIT',
    license = 'Apache',
    keywords = keywords,
    platforms = ['any'],
    packages=setuptools.find_packages(),
    package_data=package_data,
    entry_points =entry_points,
    install_requires=requiredpackages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5.2',
)
