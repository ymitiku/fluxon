from setuptools import setup, find_packages

setup(
    name="fluxon",
    version="0.0.3",
    description="A Python library for crafting structured prompts and parsing structured outputs with a focus on JSON.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mitiku Yohannes",
    author_email="se.mitiku.yohannes@gmail.com",
    url="https://github.com/ymitiku/fluxon",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "jsonschema>=4.0.0",
        "pydantic>=1.10.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
        ]
    },
)
