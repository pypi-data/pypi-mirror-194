import os
import sys
import requests
from urllib.parse import urlparse
from pathlib import Path
from tqdm import tqdm
import argparse


def download(url, filename='', path='', overwrite=False):
    if not url.startswith('http'):
        url = f'https://{url}'
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print('Invalid URL or connection error.')
        sys.exit()

    if not filename:
        filename = os.path.basename(urlparse(url).path)
    filepath = os.path.join(path, filename) if path else filename

    if os.path.exists(filepath):
        if not overwrite:
            response.close()
            print('File already exists. Aborting download.')
            sys.exit()
        else:
            choice = input('File already exists. Overwrite? [y/n]: ')
            if choice.lower() != 'y':
                response.close()
                print('Aborting download.')
                sys.exit()

    print(f'Downloading {filename}...')
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(filepath, 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()
    return filepath

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

    print(f"File '{filename}' downloaded successfully.")
