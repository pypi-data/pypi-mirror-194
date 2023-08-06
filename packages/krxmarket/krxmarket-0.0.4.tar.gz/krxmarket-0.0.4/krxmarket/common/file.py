import tempfile
import zipfile
import re
import os
import xmltodict
import pathlib


def read_file_from_zip(download_uri: str, filename: str):
    with tempfile.TemporaryDirectory() as path:
        with zipfile.ZipFile(download_uri, 'r') as zip_ref:
            zip_ref.extractall(path=path)

        for root, _, files in os.walk(path):
            for file in files:
                if re.search(filename, file):
                    with open(os.path.join(root, file), encoding='utf8') as f:
                        content = xmltodict.parse(f.read())
                        return content
    return {}


def unzip_xbrl(dest_directory: str, download_uri: str):
    with zipfile.ZipFile(download_uri, 'r') as zip_ref:
        zip_ref.extractall(path=dest_directory)
    for root, _, files in os.walk(dest_directory):
        for file in files:
            if pathlib.Path(os.path.join(root, file)).suffix == '.xbrl':
                return os.path.join(root, file)
    return ''
