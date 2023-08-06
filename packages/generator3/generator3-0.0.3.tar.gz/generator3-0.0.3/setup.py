import setuptools

long_description = open('README.md', encoding='utf-8').read()
setuptools.setup(
    name="generator3",
    version="0.0.3",
    author="themysticsavages",
    author_email="someemail@emailprovider.com",
    description="Parse Scratch's large project JSONs and convert it to scratchblocks notation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/themysticsavages/generator3",
    project_urls={
        "Bug Tracker": "https://github.com/themysticsavages/generator3/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
      "flask", 
      "requests"
    ]
)