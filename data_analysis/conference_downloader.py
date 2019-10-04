from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import json
import time
import uuid
import argparse
from urllib.parse import urlsplit, urlunsplit, quote
from posixpath import basename, dirname, join
from collections import defaultdict

parser = argparse.ArgumentParser(
    description='Adds metadata to a json file')
parser.add_argument('conference')
parser.add_argument('year')
args = parser.parse_args()

conference = args.conference
year = int(args.year)
LOG_PER = 10


def getNewPaperId():
    return uuid.uuid4().hex[:8]


def initData():
    return {
        "name": None,  # string
        "id": getNewPaperId(),  # uuid
        "pdf_link": None,  # URL
        "metadata": {
            'words': []    # words to be associated with this paper
        },
        "authors": [],  # list of strings
        "conference": None,  # string,
        "year": None
    }


def getSubLink(elem):
    return elem.find_element_by_tag_name('a').get_attribute('href')


paper_data = []


# Supports NIPS
def get_nips(year):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("https://papers.nips.cc/")
    nips_link = driver.find_element_by_xpath(
        f"//*[contains(text(), '{year}')]")
    nips_link.click()

    conf_data = []
    papers = driver.find_elements_by_css_selector(
        'body > div.main-container > div > ul > li')
    print(f"Processsing NIPS {year} with {len(papers)} papers")
    for paper in papers:
        if len(conf_data) % LOG_PER == 0:
            print(len(conf_data))
        data = initData()
        pdf_link = paper.find_element_by_tag_name('a')
        data['pdf_link'] = pdf_link.get_attribute('href') + '.pdf'
        data['name'] = pdf_link.get_attribute('innerHTML')
        data['conference'] = 'nips'
        data['year'] = year
        try:
            paper.find_element_by_class_name('author')
            authors = paper.find_elements_by_class_name('author')
            for author in authors:
                data['authors'].append(author.get_attribute('innerHTML'))
        except:
            pass
        conf_data.append(data)
    return conf_data


# Supports CVPR, ICCV, and (ECCV >= 2018)
def get_openaccesscvf(conference, year):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(f"http://openaccess.thecvf.com/{conference.upper()}{year}.py")
    conf_data = []
    titles = driver.find_elements_by_class_name('ptitle')
    authors = driver.find_elements_by_tag_name('dd')[0::2]
    info = driver.find_elements_by_tag_name('dd')[1::2]
    print(f"Processsing {conference} {year} with {len(titles)} papers")
    for idx, title in enumerate(titles):
        if len(conf_data) % LOG_PER == 0:
            print(len(conf_data))
        data = initData()
        data['conference'] = conference
        data['name'] = title.find_element_by_tag_name(
            'a').get_attribute('innerHTML')
        data['year'] = year
        data['pdf_link'] = getSubLink(info[idx])
        cur_authors = authors[idx].find_elements_by_tag_name('a')
        for author in cur_authors:
            data['authors'].append(author.get_attribute('text'))
        conf_data.append(data)
    return conf_data


# Supports ICLR year>=2018
def get_iclr(year):
    conference = "iclr"
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(
        f"https://openreview.net/group?id=ICLR.cc/{year}/Conference")
    conf_data = []

    def process(papers):
        print(f"Processsing {conference} {year} with {len(papers)} papers")
        for paper in papers:
            if len(conf_data) % LOG_PER == 0:
                print(len(conf_data))
            data = initData()
            data['conference'] = conference
            data['year'] = year
            pdf_link = paper.find_element_by_tag_name('a')
            data['name'] = pdf_link.get_attribute('text').strip()
            data['pdf_link'] = pdf_link.get_attribute(
                'href').replace('forum', 'pdf')
            authors = paper.find_element_by_class_name(
                'note-authors').find_elements_by_tag_name('a')
            for author in authors:
                data['authors'].append(author.get_attribute('text'))
            conf_data.append(data)
    orals = driver.find_element_by_id('accepted-oral-papers')
    process(orals.find_elements_by_class_name('note'))

    posters = driver.find_element_by_id('accepted-poster-papers')
    driver.find_element_by_css_selector(
        '#notes > div > ul > li:nth-child(2) > a').click()
    process(posters.find_elements_by_class_name('note'))

    return conf_data


# Supports ACL, EMNLP, NAACL
def get_acl_anthology(conference, year):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(f"https://aclweb.org/anthology/events/{conference}-{year}/")

    conf_data = []
    prefix_id = {
        'acl': 'p',
        'emnlp': 'd',
        'naacl': 'n'
    }
    suffix_ids = {
        'acl': defaultdict(lambda :[1, 2]),
        'emnlp': defaultdict(lambda : [1, 2]),
        'naacl': defaultdict(lambda : [1, 2]),
    }
    suffix_ids['acl']['2019'] = [1]
    for suffix_id in suffix_ids[conference][year]:
        papers = driver.find_element_by_id(
            f"{prefix_id[conference]}{str(year)[-2:]}-{suffix_id}").find_elements_by_tag_name('p')
        print(f"Processsing {conference} {year} with {len(papers)} papers")
        for paper in papers[1:]:
            if len(conf_data) % LOG_PER == 0:
                print(len(conf_data))
            data = initData()
            data['conference'] = conference
            data['year'] = year
            title = paper.find_element_by_css_selector('strong > a')
            data['name'] = title.get_attribute('text')
            spans = paper.find_elements_by_tag_name('span')
            pdf_link = getSubLink(spans[0])
            data['pdf_link'] = pdf_link
            authors = spans[1].find_elements_by_tag_name('a')
            for author in authors:
                data['authors'].append(author.get_attribute('text'))
            conf_data.append(data)
    return conf_data


# Supports COLT, ICML, AISTATS for >=2017
def get_mlr(conference, year):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("http://proceedings.mlr.press/")

    conf_data = []
    conf_link = driver.find_element_by_xpath(
        f"//li[text()[contains(., '{conference.upper()} {year}')]]")
    driver.get(getSubLink(conf_link))

    papers = driver.find_elements_by_class_name('paper')
    print(f"Processsing {conference} {year} with {len(papers)} papers")
    for paper in papers:
        if len(conf_data) % LOG_PER == 0:
            print(len(conf_data))
        data = initData()

        # We're given .../<identifier>.html, but the pdf lives at .../<identifier>/<identifier>.pdf
        pdf_link = list(urlsplit(getSubLink(paper)))
        link_base = basename(pdf_link[2])
        link_dir = dirname(pdf_link[2])
        link_base = link_base.split('.')
        link_base = f"{link_base[0]}/{link_base[0]}.pdf"
        pdf_link[2] = join(link_dir, link_base)

        data['pdf_link'] = urlunsplit(pdf_link)
        data['name'] = paper.find_element_by_class_name(
            'title').get_attribute('textContent')
        data['conference'] = conference
        links = paper.find_element_by_class_name('links')
        try:
            driver.implicitly_wait(1)
            code_link = links.find_element_by_xpath(
                f"a[text()[contains(., 'Code')]]")
            data['metadata']['code'] = code_link.get_attribute('href')
            driver.implicitly_wait(10)
            print(data['metadata'])
        except:
            pass
        data['year'] = year
        authors = paper.find_element_by_class_name(
            'authors').get_attribute('innerHTML')
        authors = [i.strip() for i in authors.split(',')]
        data['authors'] = authors
        conf_data.append(data)
    return conf_data


def get_neurips_special():
    conference = "nips"
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(

        f"https://openreview.net/group?id=NeurIPS.cc/2019/Reproducibility_Challenge")
    conf_data = []

    def process(papers):
        print(f"Processsing {conference} {year} with {len(papers)} papers")
        for paper in papers:
            if len(conf_data) % LOG_PER == 0:
                print(len(conf_data))
            data = initData()
            data['conference'] = conference
            data['year'] = year
            pdf_link = paper.find_element_by_tag_name('a')
            data['name'] = pdf_link.get_attribute('text').strip()
            data['pdf_link'] = pdf_link.get_attribute(
                'href').replace('forum', 'pdf')
            authors = paper.find_element_by_class_name(
                'note-authors').find_elements_by_tag_name('a')
            for author in authors:
                data['authors'].append(author.get_attribute('text'))
            conf_data.append(data)

    for page in range(28):
        orals = driver.find_element_by_id('unclaimed')
        process(orals.find_elements_by_class_name('note'))
        if page == 27:
            break
        next_page_button = driver.find_element_by_css_selector('#unclaimed > nav > ul > li:nth-child(13) > a')
        next_page_button.click()
        from time import sleep
        sleep(3)

    # posters = driver.find_element_by_id('')
    # driver.find_element_by_css_selector(
    #     '#notes > div > ul > li:nth-child(2) > a').click()
    # process(posters.find_elements_by_class_name('note'))

    return conf_data

if conference == 'nips' and year == 2019:
    res = get_neurips_special()
elif conference == 'nips':
    res = get_nips(year)
elif conference in ['cvpr', 'iccv', 'eccv']:
    res = get_openaccesscvf(conference, year)
elif conference == 'iclr':
    res = get_iclr(year)
elif conference in ['acl', 'emnlp', 'naacl']:
    res = get_acl_anthology(conference, year)
elif conference in ['colt', 'aistats', 'icml']:
    res = get_mlr(conference, year)

for paper in res:
    paper['pdf_link'] = quote(paper['pdf_link'])

json.dump(res, open(f'data/{conference}_{year}.json', 'w'),
          sort_keys=True, indent=2)
print(f"Downloaded {len(res)} papers")
