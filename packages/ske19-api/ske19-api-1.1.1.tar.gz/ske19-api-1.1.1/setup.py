import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ske19-api",
    version="1.1.1",
    author="SKE19",
    author_email="pawitchaya.ch@ku.th",
    description="A wrapper for SKE19 API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SKE19/SKE19-API-Wrappers/tree/main/python3",
    project_urls={
        "Issues": "https://github.com/SKE19/SKE19-API-Wrappers/issues?q=is:issue+is:open+label:python3"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search"
    ],
    package_dir={
        "": "src"
    },
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "requests"
    ]
)
