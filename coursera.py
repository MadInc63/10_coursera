from lxml import etree
from bs4 import BeautifulSoup
from openpyxl import Workbook
import argparse
import requests
import random


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filepath',
        help='path to file for load course from www.coursera.org'
    )
    parser.add_argument(
        'number_of_course',
        type=int,
        help='number of random course from www.coursera.org'
    )
    return parser.parse_args()


def fetch_courses_list(course_xml_url):
    xml_page = requests.get(course_xml_url)
    all_courses_on_coursera = []
    root = etree.fromstring(xml_page.content)
    for element in root.iter():
        if 'loc' in element.tag:
            all_courses_on_coursera.append(element.text)
    return all_courses_on_coursera


def get_random_curses(courses_list, number_of_course_urls):
    return random.sample(courses_list, number_of_course_urls)


def fetch_course_page(course_url):
    course_page = requests.get(course_url)
    course_page.encoding = 'utf-8'
    return course_page.text


def get_course_info(course_page):
    course_information = {}
    soup = BeautifulSoup(course_page, 'html.parser')
    course_information['title'] = soup.find(
        'h1',
        attrs={'class': 'title display-3-text'}
    ).get_text()
    course_information['language'] = soup.find(
        'div',
        attrs={'class': 'rc-Language'}
    ).get_text()
    course_information['date'] = soup.find(
        'div',
        attrs={'class': 'startdate rc-StartDateString caption-text'}
    ).get_text()
    course_information['weeks'] = len(soup.find_all(
        'div',
        attrs={'class': 'week-heading body-2-text'}
    ))
    try:
        course_information['rating'] = soup.find(
            'div',
            attrs={'class': 'ratings-text bt3-visible-xs'}
        ).get_text()
    except AttributeError:
        course_information['rating'] = 'no rating'
    return course_information


def output_courses_info_to_xlsx(save_filepath, courses_info):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Coursera'
    head_table = [
        'URL',
        'Course Title',
        'Language',
        'Start Date',
        'Duration (weeks)',
        'Rating'
    ]
    ws.append(head_table)
    for course in courses_info:
        ws.append([
            course['url'],
            course['title'],
            course['language'],
            course['date'],
            course['weeks'],
            course['rating']
        ])
    wb.save(save_filepath)


if __name__ == '__main__':
    xml_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    courses_info_list = []
    args_parse = arg_parser()
    courses_list_from_xml = fetch_courses_list(xml_url)
    random_courses_list = get_random_curses(
        courses_list_from_xml,
        args_parse.number_of_course
    )
    for url in random_courses_list:
        courses_info_page = fetch_course_page(url)
        course_info = get_course_info(courses_info_page)
        course_info['url'] = url
        courses_info_list.append(course_info)
    output_courses_info_to_xlsx(args_parse.filepath, courses_info_list)
    print('Courses information saved to {}'.format(args_parse.filepath))
