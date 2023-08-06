import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dsrf_finder",
    version="0.0.4_5",
    author="Anas bin hasan bhuiyan",
    author_email="dsrf.anas@gmail.com",
    description="This library intends to make parsing HTML (e.g. scraping the web) as simple, intuitive and make the scrape as fast as possible.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thedsrf/dsrf_finder",
    project_urls={
        "Bug Tracker": "https://github.com/thedsrf/dsrf_finder/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires= [
        "requests",
        "requests-html",
        "jsonpath-ng"
    ],
    python_requires=">=3.6",
) 