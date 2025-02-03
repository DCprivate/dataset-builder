# Software/DataHarvester/services/data_ingestion/setup.py

from setuptools import setup, find_packages

setup(
    name="data-ingestion",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "yt-dlp>=2023.11.16",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.1",
        "pymongo>=4.6.1",
        "ffmpeg-python>=0.2.0",
        "pytube>=15.0.0",
        "youtube-transcript-api>=0.6.1",
        "feature-engine>=1.6.0",
        "pyjanitor>=0.26.0",
        "nltk>=3.8.1",
        "spacy>=3.7.2",
        "presidio-analyzer>=2.2.33",
        "presidio-anonymizer>=2.2.33",
        "pandas>=2.1.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0"
    ],
) 