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
    course_info_list = []
    for course_url in random_courses_list:
        course_info = {}
        course_page = requests.get(course_url)
        html_page = course_page.text
        soup = BeautifulSoup(html_page, 'lxml')
        course_info['title'] = soup.find('h2', attrs={'class':'headline-4-text course-title'}).get_text()
        course_info['language'] = soup.find('div', attrs={'class':'rc-Language'}).get_text()
        course_info['date'] = soup.find('div', attrs={'class':'startdate rc-StartDateString caption-text'}).get_text()
        course_info['week'] = len(soup.find_all('div', attrs={'class':'week-heading body-2-text'}))
        try:
            course_info['stars'] = soup.find('div', attrs={'class':'ratings-text bt3-visible-xs'}).get_text()
        except AttributeError:
            course_info['stars'] = 'no stars'
        course_info_list.append(course_info)
    return course_info_list


def output_courses_info_to_xlsx(file_path, course_info_list):
    wb = openpyxl.load_workbook(filename=file_path)
    sheet = wb['Лист1']
    row_xlsx = 1
    for dict in course_info_list:
        column_xls = 1
        for key, value in dict.items():
            sheet.cell(row=row_xlsx, column=column_xls).value = value
            column_xls +=1
        row_xlsx += 1
    wb.save(file_path)


if __name__ == '__main__':
    xml_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    number_of_urls = 20
    file_path = 'coursera.xlsx'
    xml_page = getXML(xml_url)
    random_courses_list = get_courses_list(xml_page, number_of_urls)
    course_info_list = get_course_info(random_courses_list)
    output_courses_info_to_xlsx(file_path, course_info_list)
