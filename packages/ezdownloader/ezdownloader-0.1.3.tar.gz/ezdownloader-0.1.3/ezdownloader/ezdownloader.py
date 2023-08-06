import os
import sys
import requests
from urllib.parse import urlparse
from tqdm import tqdm
from termcolor import colored
import argparse

def download(url, filename='', path='', overwrite=False):
    if not url.startswith('http'):
        url = f'https://{url}'
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print(colored('Invalid URL or connection error.', 'red'))
        sys.exit()

    if not filename:
        filename = os.path.basename(urlparse(url).path)

    filepath = os.path.join(path, filename) if path else filename

    if os.path.exists(filepath):
        if not overwrite:
            response.close()
            print(colored('File already exists. Aborting download.', 'yellow'))
            sys.exit()
        else:
            choice = input(colored('File already exists. Overwrite? [y/n]: ', 'yellow'))
            if choice.lower() != 'y':
                response.close()
                print(colored('Aborting download.', 'yellow'))
                sys.exit()

    print(colored(f'Downloading {filename}...', 'blue'))
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(filepath, 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()

    print(colored(f'Download complete: {filename}', 'green'))
    return filename


def main():
    parser = argparse.ArgumentParser(description='Download a file from a URL.')
    parser.add_argument('url', help='The URL of the file to download')
    parser.add_argument(
        '--filename', '-f', help='The name to save the file as (defaults to the name from the URL)')
    parser.add_argument(
        '--path', '-p', help='The directory to save the file in (defaults to the current working directory)')
    parser.add_argument('--overwrite', '-o', action='store_true',
                        help='Whether to overwrite an existing file with the same name (defaults to False)')
    args = parser.parse_args()
    filename = download(args.url, args.filename, args.path, args.overwrite)
