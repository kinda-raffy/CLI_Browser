from bs4 import BeautifulSoup
from collections import deque
from colorama import Fore, Style
import requests
import argparse
import os

commands = ['back']


def parse_html(r) -> list:
    tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']
    soup = BeautifulSoup(r.content, 'html.parser')
    return [Style.RESET_ALL + element.text if element.name != 'a' else Fore.BLUE + element.text
            for element in soup.find_all(tags)]


def get_url():
    url = input("Enter an URL: ")
    return ('https://' + url) if 'https://' not in url and url != 'exit' else url


def is_valid_url(url: str) -> bool:
    if url in commands:
        return False

    if '.' in url:
        return True
    else:
        print('Incorrect URL')
        return False


def dir_manager(dir_name: str):
    save_dir = os.path.join(os.getcwd(), dir_name)
    if not os.access(save_dir, os.F_OK):
        os.makedirs(save_dir, exist_ok=True)
    return save_dir


def cli_dir_grabber():
    parser = argparse.ArgumentParser(description="Text based web browser")
    parser.add_argument("dir_name")
    return parser.parse_args().dir_name


def main():
    dir_name = cli_dir_grabber()
    save_dir = dir_manager(dir_name=dir_name)
    history = deque()
    url_var = None
    while not (url := get_url()) == 'exit':
        if is_valid_url(url):
            history.append(url_var) if url_var is not None else None
            url_var = url.rstrip('.com').lstrip('https://')
            r = requests.get(url)
            content = parse_html(r)
            for line in content:
                print(line)
            if not os.access(path := os.path.join(save_dir, url_var), os.F_OK):
                with open(path, 'w', encoding='utf-8') as file:
                    for line in content:
                        file.write(line)
        else:
            if url == 'back':
                print(history.pop()) if len(history) > 0 else None
    else:
        exit()


if __name__ == '__main__':
    main()
