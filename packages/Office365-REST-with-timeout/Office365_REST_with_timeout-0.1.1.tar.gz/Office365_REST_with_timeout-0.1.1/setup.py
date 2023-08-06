import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Office365_REST_with_timeout",
    version="0.1.1",
    author="Office365",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mmitjansc/Office365-REST-with-timeout",
    project_urls={
        "Bug Tracker": "https://github.com/mmitjansc/Office365-REST-with-timeout",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.xml'],
    },
)