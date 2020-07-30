[![Build Status](https://travis-ci.org/Giuliano-C/UniScraper.svg?branch=master)](https://travis-ci.org/Giuliano-C/UniScraper)
[![Version](https://img.shields.io/pypi/v/uni-scrapers.svg?)](https://pypi.org/project/uni-scrapers/)
[![License](https://img.shields.io/github/license/Giuliano-C/UniScraper)](https://github.com/Giuliano-C/UniScraper/blob/master/LICENSE)

# A simple web scraping tool for recipe sites.

```bash
pip install recipe-scrapers
```

then:

```python
from uni_scrapers import available, load

# Get list of available universities
print(available())

# Give the abbreviation as a string, from the list of available universities
scraper = load('USYD)

scraper.courses()
scraper.units()

# Details can be retrieved for a certain course or unit using the respective kwargs
scraper.course_detail(...)
scraper.unit_detail(...)

# Can save to json or output to stdout
scraper.save_json(out_file=None)
scraper.stdout()
```

# Scrapers available for:

- https://www.sydney.edu.au/

# Contribute

Part of the reason I want this open sourced is because if a university makes a design change, the scraper for it should be modified.

If you spot a design change (or something else) that makes the scraper unable to work for a given site - please fire an [issue](https://github.com/Giuliano-C/UniScraper/issues/new?assignees=&labels=&template=bug_report.md&title=) ASAP.

If you are a programmer, PRs with fixes are warmly welcomed and acknowledged with a virtual :beer:


# If you want a scraper for a new university added

- Open an [Issue](https://github.com/Giuliano-C/UniScraper/issues/new?assignees=&labels=&template=new_scraper.md&title=) providing us the university name, as well as the direction on how to get the neccessary details

    - Unit details
    - Course/Program details

- You are a developer and want to code the scraper on your own feel free to make a PR for us to review :)

# For Devs / Contribute

Assuming you have ``python3`` installed, navigate to the directory where you want this project to live in and drop these lines

```bash
    git clone https://github.com/Giuliano-C/UniScraper.git &&
    cd UniScaper &&
    pip install pipenv &&
    pipenv shell &&
    pipenv install &&
    python -m coverage run -m unittest
```

## Acknowledgement

Project was built with reference to https://github.com/hhursev/recipe-scrapers
