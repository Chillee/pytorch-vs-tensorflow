from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import json
import time
import uuid


year = 2019


def getNewPaperId():
    return uuid.uuid4().hex[:8]


def initData():
    return {
        "name": None,  # string
        "authors": [],  # list of (name, affiliation) tuples
        "id": getNewPaperId(),  # uuid
        "pdf_link": None,  # URL
        "metadata": {
            'words': []
        },
        "conference": None,  # string
    }


paper_data = []


def get_link_iclr(paper_elem):
    pdf_link = paper_elem.find_elements_by_class_name(
        "href_PDF")
    if len(pdf_link) == 0:
        continue
    pdf_link = pdf_link[0].get_attribute("href")
    pdf_link = pdf_link.replace("forum", "pdf")
    return pdf_link

# ICLR, NIPS


def get_papers(conference, paper_type, start_idx=0):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    conf_link = None
    if conference == "iclr":
        conf_link = f"https://iclr.cc/Conferences/{year}/Schedule?type={paper_type}"
    else:
        raise RuntimeError(
            f"Don't know how to get papers for conference {conference}.")
    driver.get(conf_link)
    paper_number = len(driver.find_elements_by_class_name(paper_type))

    for paper_idx in range(start_idx, paper_number):
        data = initData()
        driver.get(conf_link)
        papers = driver.find_elements_by_class_name(paper_type)
        paper = papers[paper_idx]
        if conference == "iclr":
            data["pdf_link"] = get_link_iclr(paper)
        else:
            pass
        paper_name = paper.find_element_by_class_name(
            "maincardBody").get_attribute("innerHTML")
        data["name"] = paper_name
        paper.click()

        def get_authors():
            main = driver.find_element_by_id('main')
            authors = main.find_elements_by_class_name("glyphicon-user")
            return authors
        paper_link = driver.current_url
        author_number = len(get_authors())

        for author_idx in range(author_number):
            driver.get(paper_link)
            author = get_authors()[author_idx]
            author_link = author.find_element_by_xpath('..')
            author_link.click()
            card = driver.find_element_by_class_name('maincard')
            author_name = card.find_element_by_tag_name(
                'h3').get_attribute("innerHTML")
            author_affiliation = card.find_element_by_tag_name(
                'h4').get_attribute("innerHTML")
            data['authors'].append((author_name, author_affiliation))
        data['metadata']['type'] = paper_type
        data['conference'] = conference
        print(
            f"Processed {paper_type} {paper_idx} out of {paper_number} for {conference}")
        paper_data.append(data)
        json.dump(paper_data, open(
            f"data/{conference}_{year}.json", "w"), sort_keys=True, indent=2)
    driver.close()


get_papers("iclr", "Poster")
get_papers("iclr", "Oral")
