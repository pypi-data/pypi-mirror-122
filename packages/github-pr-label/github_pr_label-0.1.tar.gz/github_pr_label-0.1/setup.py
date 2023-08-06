import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
# README = (f"{pathlib.Path(__file__).parent}/README.md").read_text()

# This call to setup() does all the work
setup(
    name="github_pr_label",
    version="0.1",
    description="use define labels in json file and run by executing the script in your logic",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://www.github.com/cove9988/github_pr_label",
    author="paulg",
    author_email="cove9988@gamil.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["github_pr_label"],
    include_package_data=True,
    install_requires=["pygithub"],
    entry_points={
        "console_scripts": [
            "github_pr_label=github_pr_label.__main__:main",
        ]
    },
)