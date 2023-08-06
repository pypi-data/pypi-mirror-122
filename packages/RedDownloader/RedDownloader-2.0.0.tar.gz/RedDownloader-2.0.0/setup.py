import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RedDownloader",
    version="2.0.0",
    author="Arnav Bajaj",
    author_email="arnavbajaj9@gmail.com",
    description="A small example package to install reddit videos with sound without ffmpeg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JackhammerYT/RedVidDownloader",
    project_urls={
        "Bug Tracker": "https://github.com/JackhammerYT/RedVidDownloader/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=['requests' , 'praw' , 'tqdm==4.62.3' , 'moviepy', 'pillow'],
    python_requires=">=3.6",
)