![Build Status](https://github.com/giulianocelani/UniScraper/workflows/Tests/badge.svg)
[![Version](https://img.shields.io/pypi/v/university_scraper.svg?)](https://pypi.org/project/university_scraper/)
[![License](https://img.shields.io/github/license/giulianocelani/UniScraper)](https://github.com/giulianocelani/UniScraper/blob/master/LICENSE)

# A simple web scraping/crawler tool for university sites.

```bash
pip install university_scraper
```

then:

```python
from university_scraper import available, init

# Get list of available universities
print(available())

# Give the abbreviation as a string, from the list of available universities
scraper = init('USYD')

scraper.programs
scraper.units

# Details can be retrieved for a certain program or unit using the respective kwargs
scraper.program_detail(...)
scraper.unit_detail(...)

```

# Scrapers available for:

- https://www.sydney.edu.au/

# Contribute

Part of the reason I want this open sourced is because if a university makes a design change, the scraper for it should be modified.

If you spot a design change (or something else) that makes the scraper unable to work for a given site - please fire an [issue](https://github.com/giulianocelani/UniScraper/issues/new?assignees=&labels=&template=bug_report.md&title=) ASAP.

If you are a programmer, PRs with fixes are warmly welcomed and acknowledged with a virtual :beer:


# If you want a scraper for a new university added

- Open an [Issue](https://github.com/giulianocelani/UniScraper/issues/new?assignees=&labels=&template=new_scraper.md&title=) providing us the university name, as well as the direction on how to get the neccessary details

    - Unit details
    - Program details

- You are a developer and want to code the scraper on your own feel free to make a PR for us to review :)

# For Devs / Contribute

Assuming you have ``python3`` installed, navigate to the directory where you want this project to live in and drop these lines

```bash
    git clone https://github.com/giulianocelani/UniScraper.git &&
    cd UniScaper &&
    pip install pipenv &&
    pipenv shell &&
    pipenv install &&
    python -m unittest -v
```

## Acknowledgement

Project was built with reference to https://github.com/hhursev/recipe-scrapers
