from setuptools import find_packages, setup

setup(
    name="CEApy",
    version="0.0.1",
    install_requires=[
        "setuptools>=65.5.0",
            "numpy>=1.23.5",
            "pandas>=1.5.2",
            "matplotlib>=3.6.2"
    ],
    author="Julio C. R. Machado",
    author_email=["julioromac@outlook.com", "machado.juliocr@gmail.com"],
    description="Library to automate analyzes in CEA NASA",
    url="https://github.com/juliomachad0/CEApy.git",
    packages=find_packages(include=['CEApy']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    include_package_data=True,
    package_data={'': ['cea-exec/*']},
)

"""
- julio machado, julioromac@outlook.com, git: juliomachad0
- linkedin: 
- Portuguese: lista de especies disponíveis na biblioteca thermo.inp
- English: list of species available in the thermo.inp library
"""