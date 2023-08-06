from setuptools import setup, find_packages

setup(
    name="YISYKS",
    version="0.1.0",
    author="TheTechyKid",
    author_email="thefriendlyhacker44@gmail.com",
    description="YIS (YouTube Info Search) is a Python desktop application that allows you to search for and download YouTube videos using their URLs.",
    url="https://github.com/TheTechyKid/YIS",
    packages=find_packages(),
    install_requires=[
        "pytube>=12.1.2",
        "setuptools>=65.5.0",
        "fast-youtube-search>=0.0.8",
        "customtkinter>=5.1.2",
        # Add other dependencies here
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)