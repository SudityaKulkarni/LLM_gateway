"""
Setup configuration for llm-safety-guard package
"""
from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README_PACKAGE.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nebula',
    version='0.1.0',
    author='Suditya Kulkarni',
    author_email='sudityaKulkarni7@gmail.com',  # Update this
    description='Comprehensive safety guardrails for LLM applications with detection for toxicity, jailbreaks, PII, and more',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SudityaKulkarni/LLM_gateway',
    packages=find_packages(exclude=['frontend', 'frontend.*', 'tests', 'tests.*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=[
        'torch>=2.0.0',
        'transformers>=4.30.0',
        'detoxify>=0.5.0',
        'pydantic>=2.0.0',
        'fastapi>=0.100.0',
        'uvicorn>=0.22.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-asyncio>=0.21.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
        ],
        'api': [
            'fastapi>=0.100.0',
            'uvicorn>=0.22.0',
        ],
    },
    keywords='llm safety guardrails toxicity jailbreak prompt-injection pii-detection ai-safety',
    project_urls={
        'Bug Reports': 'https://github.com/SudityaKulkarni/LLM_gateway/issues',
        'Source': 'https://github.com/SudityaKulkarni/LLM_gateway',
    },
)
