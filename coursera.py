from lxml import etree
from bs4 import BeautifulSoup
from openpyxl import Workbook
import argparse
import requests
import random


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath",
                        help="path to file for load course "
                             "from www.coursera.org")
    parser.add_argument("number_of_course", type=int,
                        help="number of random course from www.coursera.org")
    return parser.parse_args()


def get_courses_list(xml_url, number_of_urls):
    xml_page = requests.get(xml_url)
    all_courses_on_coursera = []
    root = etree.fromstring(xml_page.content)
    for element in root.iter():
        if 'loc' in element.tag:
            all_courses_on_coursera.append(element.text)
    return random.sample(all_courses_on_coursera, number_of_urls)


def get_course_info(random_courses_list):
    courses_info_list = []
    for course_url in random_courses_list:
        course_info = {}
        course_page = requests.get(course_url)
        course_page.encoding = 'utf-8'
        html_page = course_page.text
        soup = BeautifulSoup(html_page, 'html.parser')
        course_info['url'] = course_url
        course_info['title'] = soup.find(
            'h1', attrs={'class': 'title display-3-text'}).get_text()
        course_info['language'] = soup.find(
            'div', attrs={'class': 'rc-Language'}).get_text()
        course_info['date'] = soup.find(
            'div',
            attrs={'class': 'startdate rc-StartDateString caption-text'}
        ).get_text()
        course_info['weeks'] = len(
            soup.find_all('div', attrs={'class': 'week-heading body-2-text'}))
        try:
            course_info['rating'] = soup.find(
                'div',
                attrs={'class': 'ratings-text bt3-visible-xs'}).get_text()
        except AttributeError:
            course_info['rating'] = 'no rating'
        courses_info_list.append(course_info)
    return courses_info_list


def output_courses_info_to_xlsx(filepath, course_info_list):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Coursera'
    head_table = ['URL', 'Course Title', 'Language', 'Start Date',
                  'Duration (weeks)', 'Rating']
    ws.append(head_table)
    for course in course_info_list:
        ws.append([course['url'], course['title'], course['language'],
                   course['date'], course['weeks'], course['rating']])
    wb.save(filepath)
    print('Courses information saved to {}'.format(filepath))


if __name__ == '__main__':
    xml_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    start_arg = arg_parser()
    number_of_urls = start_arg.number_of_course
    filepath = start_arg.filepath
    random_courses_list = get_courses_list(xml_url, number_of_urls)
    courses_info_list = get_course_info(random_courses_list)
    output_courses_info_to_xlsx(filepath, courses_info_list)
