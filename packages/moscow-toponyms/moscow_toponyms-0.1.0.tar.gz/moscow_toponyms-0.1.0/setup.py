from setuptools import setup

def long_desc():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name="moscow_toponyms",
    version="0.1.0",
    author="Diana Esaian",
    author_email="diana.esaian@gmail.com",
    description="Moscow toponym extractor for Russian texts",
    long_description=long_desc(),
    long_description_content_type="text/markdown",
    packages=['moscow_toponyms'],
    url="https://github.com/diana-esaian/moscow_toponyms",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Natural Language :: Russian",
        "Topic :: Text Processing"
    ],
    python_requires='>=3.6',
    license="MIT",
    install_requires=[
        'spacy>=3.0.0,<4.0.0',
        'natasha>=1.5.0',
        'pymorphy2>=0.9.1',
        'pymorphy2-dicts>=2.4.393442.3710985'
    ],
    include_package_data=True
)
