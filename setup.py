# setup.py
from setuptools import setup, find_packages

setup(
    name="scienceplotter",
    version="0.1.0",
    description="Scientific Plotting Tool for Researchers",
    author="Vermosh",
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'pandas>=1.0',
        'matplotlib>=3.0',
        'seaborn>=0.11',
        'openpyxl>=3.0',   
        'Pillow>=8.0',     
    ],
    extras_require={
        'test': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'coverage>=5.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'scienceplotter=cli_demo:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
