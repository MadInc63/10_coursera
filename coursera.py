from lxml import etree
import requests
from bs4 import BeautifulSoup
import openpyxl
import random


def getXML(xml_url):
    xml_page = requests.get(xml_url)
    return xml_page


def get_courses_list(xml_page, number_of_urls):
    all_course_on_cursera=[]
    root = etree.fromstring(xml_page.content)
    for element in root.iter():
        if 'loc' in element.tag:
            all_course_on_cursera.append(element.text)
    return random.sample(all_course_on_cursera, number_of_urls)


def get_course_info(random_courses_list):
    for course_url in random_courses_list:
        course_page = requests.get(course_url)
        html_page = course_page.text
        soup = BeautifulSoup(html_page, 'lxml')
        print(soup.find('h2', attrs={'class':'headline-4-text course-title'}).get_text())
        print(soup.find('div', attrs={'class':'rc-Language'}).get_text())
        print(soup.find('div', attrs={'class':'startdate rc-StartDateString caption-text'}).get_text())
        print(soup.find_all('div', attrs={'class':'week-heading body-2-text'}).get_text())


def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    xml_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    number_of_urls = 20
    xml_page = getXML(xml_url)
    random_courses_list = get_courses_list(xml_page, number_of_urls)
    print(get_course_info(random_courses_list))
1