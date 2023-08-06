from setuptools import setup, find_packages

setup(
    name="Neo1",
    version="2.2.0",
    author="TheTechyKid",
    author_email="thefriendlyhacker44@gmail.com",
    description="Hoi ther!",
    packages=find_packages(),
    install_requires=[
        "customtkinter>=5.1.2",
        "fast-youtube-search>=0.0.8",
        "pytube>=12.1.2"
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