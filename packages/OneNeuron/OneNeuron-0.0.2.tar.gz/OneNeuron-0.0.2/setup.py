import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

PROJECT_NAME = "OneNeuron"
USER_NAME = "Amit Kumar Pradhan"
USER_EMAIL = "amitpradhands@gmail.com"

setuptools.setup(
    name=f"{PROJECT_NAME}",
    version="0.0.2",
    author=USER_NAME,
    author_email=USER_EMAIL,
    description="OneNeuron Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pradhami/Perceptron",
    project_urls={
        "Bug Tracker": "https://github.com/pradhami/Perceptron/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['numpy']
)