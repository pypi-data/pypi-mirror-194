from setuptools import setup, find_packages


PACKAGE_NAME = "cli_msg"
PACKAGE_VERSION = "4.1.0"


def requirements(filename="requirements.txt"):
    return open(filename.strip()).readlines()



with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author="Bleuzkernel",
    author_email="your@email.com",
    description="CLI Messages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/your_username/your_project",
    include_package_data=True,
    py_modules=['hello'],
    install_requires=[
        "click",
        "rich",
    ],
    entry_points={  # Specify the name of the main file for your project here
        "console_scripts": [
            "cli_msg = hello:cli",
        ]
    },
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.9",
)