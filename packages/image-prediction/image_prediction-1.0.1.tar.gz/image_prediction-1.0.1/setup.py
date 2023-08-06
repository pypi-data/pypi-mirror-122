import setuptools

with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="image_prediction",
    version="1.0.1",
    author="Dipesh Shrestha",
    author_email="dipesh@example.com",
    description="A simple image prediction package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)