from .._abstract import AbstractScraper
from ..utils import scrape_page, Crawler, get_int_from_string

import re


class UniversityOfSydney(AbstractScraper):

    def __init__(self):
        self.name = "University of Sydney"
        super().__init__()

    @staticmethod
    def abbreviation():
        return "USYD"

    @property
    def programs(self):
        if self._programs is None:
            programs = []
            url = "https://mycourseguide.sydney.edu.au/search"
            crawler = Crawler(url)
            try:
                crawler.wait_for_element_to_load_by_id('search-results')

                for i, element in enumerate(crawler.find_elements(identifier='checkbox-module--input_checkbox--3aIJH', tag='input')):
                    if i == 0:
                        continue
                    element.location_once_scrolled_into_view
                    department_name = element.get_attribute('data-title')
                    element.click()
                    crawler.scroll_to_top()
                    crawler.scroll_through_first_visible('lazyload-placeholder')
                    source = crawler.page_source
                    element.click()

                    page = scrape_page(source, driver_source=True)
                    search_results = page.find('div', id='search-results')
                    if search_results is None:
                        continue

                    results = search_results.find_all('a')
                    for result in results:
                        if result.get('title', None):
                            program = dict(
                                department=department_name,
                                name=result['title']
                            )
                            programs.append(program)

                crawler.close()
                self._programs = programs

            except Exception:
                crawler.close()

        return self._programs

    @property
    def units(self):
        if self._units is None:
            units = []

            page = scrape_page(
                "https://www.sydney.edu.au/s/search.html?query=!Z&collection=Sydney-Curriculum_UOS&start_rank=1&form=simple&num_ranks=9999999"
            )
            raw_units = page.find('ol', id='search-results').find_all('li')[1:]
            for u in raw_units:
                raw_unit = u.find('dl')
                if raw_unit is None:
                    continue
                dt = raw_unit.find_all('dt')
                dd = raw_unit.find_all('dd')
                unit = {}
                for i in range(len(dt)):
                    if "uosCode" in dt[i].text:
                        unit['code'] = dd[i].text.strip()
                    elif "title" in dt[i].text:
                        unit['name'] = dd[i].text.strip()
                units.append(unit)
            self._units = units

        return self._units

    def program_detail(self, url):
        program_detail = {}

        if url is None or url == '':
            return {}

        page = scrape_page(url)

        semesters = page.find(id='semesters')
        tables = semesters.find_all('table', class_="t_b")
        year = 1
        units = []
        for i in range(len(tables)):
            table = tables[i]
            if i != 0 and i % 2 == 0:
                year += 1
            if i % 2 == 0:
                rows = table.find_all('tr')
                for j in range(1, len(rows)):
                    cols = rows[j].find_all('td')
                    match = re.match(r"(?P<code>\w{4}\d{4}):(?P<name>.*)", cols[2].find('a').text.strip())
                    if match:
                        units.append({
                            "year": year,
                            "term": "Semester 1",
                            "group": cols[0].text,
                            "cp": int(cols[1].text),
                            "code": match.group('code'),
                            "name": match.group('name').strip(),
                            "choice": False,
                            "multiple": False
                        })
                    elif int(cols[1].text) <= 6:
                        units.append({
                            "year": year,
                            "term": "Semester 1",
                            "group": cols[0].text,
                            "cp": int(cols[1].text),
                            "choice": True,
                            "multiple": False
                        })
                    else:
                        units.append({
                            "year": year,
                            "term": "Semester 1",
                            "group": cols[0].text,
                            "cp": int(cols[1].text),
                            "choice": False,
                            "multiple": True
                        })
            else:
                rows = table.find_all('tr')
                for j in range(1, len(rows)):
                    cols = rows[j].find_all('td')
                    match = re.match(r"(?P<code>\w{4}\d{4}):(?P<name>.*)", cols[2].find('a').text.strip())
                    if match:
                        units.append({
                            "year": year,
                            "term": "Semester 2",
                            "group": cols[0].text,
                            "cp": int(cols[1].text),
                            "code": match.group('code'),
                            "name": match.group('name').strip(),
                            "choice": False,
                            "multiple": False
                        })
                    elif int(cols[1].text) <= 6:
                        units.append({
                            "year": year,
                            "term": "Semester 2",
                            "group": cols[0].text,
                            "cp": int(cols[1].text),
                            "choice": True,
                            "multiple": False
                        })
                    else:
                        units.append({
                            "year": year,
                            "term": "Semester 2",
                            "group": cols[0].text,
                            "cp": int(cols[1].text),
                            "choice": False,
                            "multiple": True
                        })

        program_detail['schedule'] = units

        groups = []
        unit_tables = page.find(id='tables_accordion').find_all(recursive=False)
        group_detail = dict()

        for i in range(len(unit_tables)):
            if i % 2 == 0:
                group_detail.clear()
                table_header = unit_tables[i]
                header_formatted = ' '.join(table_header.text.split()).split("- ")[1]
                group_detail["name"] = header_formatted
                if "(" in header_formatted:
                    match = re.match(r'(?P<name>.*) \(', header_formatted)
                    if match:
                        group_detail["name"] = match.group('name')
                    match = re.findall(r'\d+', header_formatted)
                    if match:
                        if len(match) == 2:
                            group_detail["min"] = int(match[0])
                            group_detail["max"] = int(match[1])
                        else:
                            group_detail["min"] = int(match[0])
            else:
                table_content = unit_tables[i]
                rows = table_content.find_all('tr')
                units = []
                for j in range(1, len(rows)):
                    row = rows[j].find_all('td')
                    found_sessions = [session.text.strip("\n") for session in row[3].find_all('a')]
                    filtered_sessions = filter(lambda session: (session == "Semester 1" or session == "Semester 2"), found_sessions)
                    if filtered_sessions:
                        units.append({
                            "code": row[0].text.strip("\n"),
                            "name": row[1].text.strip("\n"),
                            "cp": int(row[2].text),
                            "sessions": list(filtered_sessions)
                        })
                group_detail["units"] = units
                groups.append(group_detail.copy())

        program_detail['groups'] = groups

        overview = page.find(id="overview").find_all('tr')
        for row in overview:
            row_content = row.find_all('td')
            header = row_content[0].text.lower()
            content = row_content[1]

            if "cp required" in header:
                program_detail["cp_required"] = int(content.text.strip())
            elif "ft duration" in header:
                program_detail["min_duration"] = get_int_from_string(content.text)
            elif "requirements" in header:
                program_detail["requirements"] = [requirement.strip() for requirement in re.findall(r"►(.*?)<br/>", str(content))]

        return program_detail

    def unit_detail(self, identifier):

        unit_detail = {}

        if identifier is None or identifier == '':
            return {}

        url = "https://www.sydney.edu.au/units/{}".format(identifier)
        crawler = Crawler(url)

        if url == crawler.url:
            page_source = crawler.page_source
            unit_page = scrape_page(page_source, driver_source=True)

            title_text = unit_page.find('h1', class_='pageTitle').text
            title = title_text.split(": ")
            unit_detail['code'] = title[0]
            unit_detail['name'] = title[1]

            academic_details = unit_page.find('div', id='academicDetails')
            credit_points = academic_details.find_all('tr')[2]
            unit_detail['credit_points'] = int(credit_points.find('td').text)

            enrolment_rules = unit_page.find('div', id='enrolmentRules').find_all('tr')
            keys = ['pre-requisites', 'co-requisites', 'prohibitions', 'assumed-knowledge']
            for i in range(len(enrolment_rules)):
                text = enrolment_rules[i].find('td').text.strip()
                if keys[i] == 'pre-requisites':
                    unit_detail[keys[i]] = text if "None" not in text else None
                else:
                    unit_detail[keys[i]] = text if "None" not in text else None

            sessions = unit_page.find('div', id='currentOutlines').find_all('li')
            unit_detail['sessions'] = [session.text.split(",")[0].strip() for session in sessions]

            for session in sessions:
                if session.find('a'):
                    crawler.click_element(custom='//a[contains(text(), "Semester")]')
                    page_source = crawler.page_source
                    crawler.close()
                    unit_page = scrape_page(page_source, driver_source=True)
                    raw_assessments = unit_page.find('table', id='assessment-table').find_all('tbody')
                    assessments = []
                    for assessment in raw_assessments:
                        content = assessment.find_all('tr', class_='primary')
                        if not content:
                            continue
                        content = content[0].find_all('td')
                        is_group = False
                        img = content[0].find('img', alt=True)
                        if img:
                            match = re.search(r'alt="(.*?)"', str(img))
                            if match:
                                is_group = 'group' in match.group()
                        assessments.append(dict(
                            name=content[1].find('b').text.strip().title(),
                            group=is_group,
                            weight=float(get_int_from_string(content[2].text.strip())),
                        ))
                    unit_detail['assessments'] = assessments
                    break

            if not unit_detail.get('assessments', None):
                crawler.close()
        else:
            crawler.close()

        return unit_detail
