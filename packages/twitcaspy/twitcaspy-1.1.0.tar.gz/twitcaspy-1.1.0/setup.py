# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

import re
from setuptools import find_packages, setup

with open("README.md", encoding='utf-8') as file:
    long_description = file.read()

tests_require = [
    "nose>=1.3.7,<2",
    "vcrpy>=4.1.1,<5",
    "python-dotenv>=0.19.0,<1",
]

setup(
    long_description=long_description,
    project_urls={
        "Documentation": "https://twitcaspy.alma-field.com/",
        "Issue Tracker": "https://github.com/Alma-field/twitcaspy/issues",
        "Source Code": "https://github.com/Alma-field/twitcaspy",
    },
    packages=find_packages(exclude=["tests", "webhook", "realtime"]),
    install_requires=[
        "requests>=2.26.0,<3",
        "requests_oauthlib>=1.3.0,<2",
    ],
    tests_require=tests_require,
    extras_require={
        "test": tests_require,
        "webhook": ["flask>=2.0.1,<3"],
        "realtime": ["websocket-client>=1.2.1,<2"]
    },
    test_suite="nose.collector",
    keywords="twitcasting library",
    python_requires=">=3.7"
)
