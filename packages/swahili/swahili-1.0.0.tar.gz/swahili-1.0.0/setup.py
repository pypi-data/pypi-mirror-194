from setuptools import setup, find_packages

setup(
    name='swahili',
    version='1.0.0',
    description='Natural Language Processing (NLP) Library for Swahili (Kiswahili) Language',
    packages=find_packages(),
    author_email="emma.minga@yahoo.com",
    install_requires=[
        'numpy>=1.16.0',
        'pandas>=0.24.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
