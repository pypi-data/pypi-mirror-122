from setuptools import setup, find_packages
import os


VERSION = '2.0.3'
DESCRIPTION = 'Just Hacking is a Python CLI script that stimulates as you are hacking.'


# Setting up
setup(
    name="justhacking",
    version=VERSION,
    author="Divinemonk",
    author_email="<v1b7rc8eb@relay.firefox.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['rich'],
    keywords=['python', 'justhacking', 'divinemonk', 'hacking stimulation', 'cli', 'python hacking', 'console'],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "justhacking=justhacking.__main__:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "License :: OSI Approved :: MIT License"
    ]
)