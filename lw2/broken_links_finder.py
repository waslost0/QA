from collections import deque
from urllib.parse import urljoin
import datetime
import requests
from lxml import html
from requests.exceptions import HTTPError

HTTP = 'http://'
DOMAIN = f'{HTTP}91.210.252.240'
TARGET_URL = f'{DOMAIN}/broken-links/'

COUNTER = {
    'good': 0,
    'bad': 0,
    }


def get_current_time():
    return ''.join(datetime.datetime.now().strftime("%d/%m/%Y  %H:%M:%S"))


def is_successful_response(reponse):
    try:
        reponse.raise_for_status()
    except HTTPError:
        return False
    return True


def filter_urls(content):
    try:
        urls = []
        for href in html.fromstring(content).xpath("//a/@href"):
            urls.append(urljoin(TARGET_URL, href))
        return set(urls)
    except Exception:
        return []


def get_urls(URL):
    response = requests.get(URL)
    links = filter_urls(response.content)
    return response.status_code, links, is_successful_response(response)


def make_report(reported_urls):
    with open("good.txt", "w+") as good, open("bad.txt", "w+") as bad:
        for url, status in reported_urls.items():
            status_code, is_good_response = status
            file = good if is_good_response else bad
            file.write(f"{url} {status_code}\n")

        good.write(f"\nCount links: {COUNTER['good']}\nCheck date: {get_current_time()}\n")
        bad.write(f"\nCount links: {COUNTER['bad']}\nCheck date: {get_current_time()}\n")


if __name__ == '__main__':
    status_code, urls, is_good_response = get_urls(TARGET_URL)

    queue = deque([href for href in urls if DOMAIN in href])

    processed_urls = [TARGET_URL]
    reported_urls = {TARGET_URL: (status_code, is_good_response)}

    while queue:
        url = queue.pop()
        if 'tel://' in url or 'mailto:' in url:
            continue
        if url in processed_urls:
            continue
        processed_urls.append(url)
        status_code, urls, is_good_response = get_urls(url)
        reported_urls[url] = status_code, is_good_response
        print(url, status_code)

        if DOMAIN in url:
            queue.extend(list(urls))

    make_report(reported_urls)
