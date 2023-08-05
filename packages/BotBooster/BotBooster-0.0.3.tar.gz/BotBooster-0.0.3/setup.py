from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="BotBooster",
    version="0.0.3",
    description="for replit bots",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://tiktok.com/@noteason",
    author="noteason",
    author_email="tiktoknoteason@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["BotBooster"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "BotBooster=botbooster.cli:main",
        ]
    },
)