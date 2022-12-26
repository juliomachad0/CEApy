from setuptools import find_packages, setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="CEApy",
    version="1.0.0",
    install_requires=[
            "pandas>=1.5.2",
    ],
    author="Julio C. R. Machado",
    author_email="julioromac@outlook.com",
    description="Library to automate analyzes in CEA NASA - Under development",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/juliomachad0/CEApy.git",
    packages=find_packages(include=['CEApy']),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
    ],
    python_requires=">=3.10",
    include_package_data=True,
    package_data={'': ['cea-exec/*']},
)
