import os
from setuptools import setup, find_packages

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(
    os.path.join(here, "uni_scraper", "__version__.py"), "r", encoding="utf-8"
) as f:
    exec(f.read(), about)

README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="uni_scrapers",
    url="https://github.com/Giuliano-C/UniScraper/",
    version=about['__version__'],
    author="Giuliano Celani",
    description="Python package for scraping university information",
    keywords="python uni university scraper uni-scraper",
    long_description=README,
    install_requires=[
        "beautifulsoup4>=4.9.0",
        "requests>=2.23.0",
        "lxml>=4.5.0",
        "tabulate>=0.8.7"
    ],
    packages=find_packages(),
    package_data={"": ["LICENSE"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.6'
)