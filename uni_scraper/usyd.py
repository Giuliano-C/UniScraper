from ._abstract import AbstractScraper
from ._utils import scrape_page

from urllib.request import urlopen
from urllib.error import HTTPError
import re

findings = list()
def course_dfs(current, parent):
    page = scrape_page("https://cusp.sydney.edu.au/students/view-degree-programs-tree-node-ajax/did//degree_program_id//node_pid/%d" % int(re.search(r'\d+', current.get('id')).group()))
    for li in page.find_all('li'):
        if li.get('id', None):
            course_dfs(li, current)
        else:
            a_tag = li.find('a')
            findings.append({
                "link_id": int(re.search(r'\d+', a_tag.get('href')).group()),
                "name": a_tag.text.strip(),
                "parent": parent.text.strip()
            })        

class UniversityOfSydney(AbstractScraper):

    def __init__(self):
        self.name = "University of Sydney"
        super().__init__()

    @classmethod
    def abbreviation(cls):
        return "USYD"

    def courses(self):
        try:
            page = scrape_page("https://cusp.sydney.edu.au/students/view-degree-programs-tree-node-ajax/did//degree_program_id//node_pid")
            departments = page.find_all('li')
            courses = []
            for department in departments:
                department_dict = {}
                department_dict['department'] = department.text.strip()
                course_dfs(department, None)
                department_programs = findings.copy()
                findings.clear()
                department_dict['programs'] = department_programs
                courses.append(department_dict)
            return courses
        except Exception as e:
            raise e

    def units(self):
        try:
            page = scrape_page("https://cusp.sydney.edu.au/students/view-units-page/did//get_table/1")
            units = []
            links = page.find_all('a')
            for i in range(1, len(links), 2):
                code = links[i-1].text
                name = links[i].text
                href = links[i]['href']
                units.append({
                    "link_id": re.search(r"\d+", href).group(),
                    "code": re.search(r'\w+', code).group(),
                    "name": re.sub(r"[^a-zA-Z0-9\s]+", "", name)
                })
            return units
        except Exception as e:
            raise e

    def course_detail(self, **kwargs):
        course = kwargs.get('course', None)
        page = scrape_page("https://cusp.sydney.edu.au/students/view-degree-page/degree_id/%d" % course)
        course_detail = {}
        semesters = page.find(id='semesters')
        tables = semesters.find_all('table', class_="t_b")
        planner = {}
        year = 1
        terms = []
        for i in range(len(tables)):
            table = tables[i]
            if i != 0 and i % 2 == 0:
                year += 1
                terms = []
            if i % 2 == 0:
                rows = table.find_all('tr')
                units = []
                for j in range(1, len(rows)):
                    row = rows[j].find_all('td')
                    name = ""
                    if len(row[2].text.split(":")):
                        name = row[2].text.split(":")[0]
                    else:
                        name = row[2].text
                    units.append({
                        "block": row[0].text,
                        "cp": int(row[1].text),
                        "name": name
                    })
                terms.append({
                    "term": "SEM1",
                    "units": units
                })
            else:
                rows = table.find_all('tr')
                units = []
                for j in range(1, len(rows)):
                    row = rows[j].find_all('td')
                    name = ""
                    if len(row[2].text.split(":")):
                        name = row[2].text.split(":")[0]
                    else:
                        name = row[2].text
                    units.append({
                        "block": row[0].text,
                        "cp": int(row[1].text),
                        "name": name
                    })
                terms.append({
                    "term": "SEM2",
                    "units": units
                })
                planner[year] = terms

        course_detail['planner'] = planner

        blocks = []
        unit_tables = page.find(id='tables_accordion').find_all(recursive=False)
        block_detail = dict()

        for i in range(len(unit_tables)):
            if i % 2 == 0:
                block_detail.clear()
                table_header = unit_tables[i]
                header_formatted = ' '.join(table_header.text.split()).split("- ")[1]
                block_detail["name"] = header_formatted
                min_cp = None
                max_cp = None
                if "(" in header_formatted:
                    match = re.match(r'(?P<name>.*) \(', header_formatted)
                    if match:
                        block_detail["name"] = match.group('name')
                    match = re.findall(r'\d+', header_formatted)
                    if match:
                        if len(match) == 2:
                            block_detail["min"] = int(match[0])
                            block_detail["max"] = int(match[1])
                        else:
                            block_detail["min"] = int(match[0])
            else:
                table_content = unit_tables[i]
                rows = table_content.find_all('tr')
                units = []
                for j in range(1, len(rows)):
                    row = rows[j].find_all('td')
                    sessions = list(filter(lambda session : (session == "Semester 1" or session == "Semester 2"), [session.text.strip("\n") for session in row[3].find_all('a')]))
                    if sessions:
                        units.append({
                            "code": row[0].text.strip("\n"),
                            "name": row[1].text.strip("\n"),
                            "cp": int(row[2].text),
                            "sessions": sessions
                        })
                block_detail["units"] = units
                blocks.append(block_detail.copy())

        course_detail['blocks'] = blocks

        overview = page.find(id="overview").find_all('tr')
        for row in overview:
            row_content = row.find_all('td')
            header = row_content[0].text.lower()
            content = row_content[1]

            if "cp required" in header:
                course_detail["cp_required"] = int(content.text.strip())
            elif "ft duration" in header:
                course_detail["min_duration"] = int(re.match(r'\d+',content.text).group(0))
            elif "requirements" in header:
                formatted_requirements = str(content).split("<br><br>")
                formatted_requirements = [requirement.replace("<td>", "") for requirement in formatted_requirements]
                formatted_requirements = [requirement.replace("</td>", "") for requirement in formatted_requirements]
                formatted_requirements = [requirement.replace("</br>", "") for requirement in formatted_requirements]
                course_detail["requirements"] = formatted_requirements
    
        return course_detail

    def unit_detail(self, **kwargs):
        name = kwargs.get('name', None)
        link_id = kwargs.get('link_id', None)

        unit_detail = {}
        try:
            link = "https://www.sydney.edu.au/units/%s" % name
            unit_page = scrape_page(link)
        
            title_text = unit_page.find('h1', class_='pageTitle').text
            title = title_text.split(": ")
            unit_detail['url'] = link
            unit_detail['code'] = title[0]
            unit_detail['name'] = title[1]

            unit_detail['summary'] = unit_page.find('div', class_='b-summary').text.strip()

            academic_details = unit_page.find('div', id='academicDetails')
            credit_points = academic_details.find_all('tr')[2]
            unit_detail['credit_points'] = int(credit_points.find('td').text)

            enrolment_rules = unit_page.find('div', id='enrolmentRules').find_all('tr')
            keys = ['pre-requisites', 'co-requisites', 'prohibitions', 'assumed-knowledge']
            for i in range(len(enrolment_rules)):
                text = enrolment_rules[i].find('td').text.strip()
                if keys[i] == 'pre-requisites':
                    unit_detail[keys[i]] = text if not "None" in text else None
                else:
                    unit_detail[keys[i]] = text if not "None" in text else None

            sessions = unit_page.find('div', id='currentOutlines').find_all('li')
            unit_detail['sessions'] = [session.text.split(",")[0].strip() for session in sessions]

            detail_link = None
            for session in sessions:
                if session.find('a'):
                    detail_link = "https://www.sydney.edu.au%s" % session.find('a')['href']
            
            if detail_link:
                unit_page = scrape_page(detail_link)
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
                        weight=float(re.search(r"\d+", content[2].text.strip()).group()),
                    ))
                unit_detail['assessments'] = assessments

        except HTTPError:
            link = "https://cusp.sydney.edu.au/students/view-unit-page/uos_id/%s" % link_id
            unit_page = scrape_page(link)

            unit_detail['url'] = link

            overview = unit_page.find('div', id='overview').find_all('tr')

            main_content = overview[0].find_all('td')[1].text.strip()
            match = re.match(r"(?P<code>\w+):(?P<name>.*)\((?P<cp>\d+)", main_content)
            unit_detail['code'] = match.group('code').strip()
            unit_detail['name'] = match.group('name').strip()
            unit_detail['credit_points'] = int(match.group('cp').strip())

            sessions = overview[6].find_all('td')[1].text.strip()
            unit_detail['sessions'] = sessions

            handbook = unit_page.find('div', id='handbook').find_all('tr')
            for content in handbook:
                row = content.find_all('td')
                name = row[0].text.strip()
                content = re.sub(r"\s{2,}", " ", row[1].text.strip())
                
                if 'Pre-Requisites' in name:
                    unit_detail['pre-requisites'] = content if not 'None' in content else None
                elif 'Co-requisites' in name:
                    unit_detail['co-requisites'] = content if not 'None' in content else None
                elif 'Prohibitions' in name:
                    unit_detail['prohibitions'] = content if not 'None' in content else None
                elif 'Assumed Knowledge' in name:
                    unit_detail['assumed-knowledge'] = content if not 'None' in content else None
                elif 'Description' in name:
                    unit_detail['summary'] = content if not 'None' in content else None

            raw_assessments = unit_page.find('div', id='assessment').find(class_='t_b').find_all('tr')[1:]
            assessments = []
            for assessment in raw_assessments:
                content = assessment.find_all('td')
                assessments.append(dict(
                    name=re.sub(r"\*", "", content[1].text.strip()).title(),
                    group=content[2].text.strip() == "Yes",
                    weight=float(content[3].text.strip()),
                ))
            unit_detail['assessments'] = assessments

            raw_teaching = unit_page.find('div', id='teaching').find(class_='t_b').find_all('tr')[1:]
            activities = []
            for activity in raw_teaching:
                content = activity.find_all('td')
                activities.append(dict(
                    name=content[1].text.strip() if content[1].text != '' else None,
                    hours_per_week=float(content[2].text.strip()) if content[2].text != '' else None,
                    sessions_per_week=int(content[3].text.strip()) if content[3].text != '' else None,
                    weeks_per_semester=int(content[4].text.strip()) if content[4].text != '' else None,
                ))
            unit_detail['teaching'] = activities

        except Exception as e:
            print(e)

        return unit_detail