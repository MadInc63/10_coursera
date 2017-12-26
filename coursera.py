from lxml import etree
from bs4 import BeautifulSoup
from openpyxl import Workbook
import argparse
import requests
import random


def arg_parse():
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


def fetch_page(fetched_url):
    response = requests.get(fetched_url).text
    return response


def parse_courses_page(page):
    parsed_list = []
    root = etree.fromstring(page.content)
    for element in root.iter():
        if 'loc' in element.tag:
            parsed_list.append(element.text)
    return parsed_list


def get_random_elements(elements_list, amount_of_elements):
    return random.sample(elements_list, amount_of_elements)


def get_course_info(page):
    page.encoding = 'utf-8'
    course_information = {}
    soup = BeautifulSoup(page, 'html.parser')
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


def save_courses_info_to_file(save_filepath, courses_info):
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
    args = arg_parse()
    page_from_url = fetch_page(xml_url)
    list_of_courses_urls = parse_courses_page(page_from_url)
    list_of_random_courses_urls = get_random_elements(
        list_of_courses_urls,
        args.number_of_course
    )
    for url in list_of_random_courses_urls:
        course_page = fetch_page(url)
        course_info = get_course_info(course_page)
        course_info['url'] = url
        courses_info_list.append(course_info)
    save_courses_info_to_file(args.filepath, courses_info_list)
    print('Courses information saved to {}'.format(args.filepath))
