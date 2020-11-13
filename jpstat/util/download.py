import os
import cgi
import requests
import shutil


def download_file(url, path, file_name=None):
    """Download file from url to directory

    URL is expected to have a Content-Disposition header telling us what
    filename to use.

    Returns filename of downloaded file.

    """
    res = requests.get(url, stream=True)
    if res.status_code != 200:
        raise ValueError('Failed to download')

    if file_name is None:
        params = cgi.parse_header(
            res.headers.get('Content-Disposition', ''))[-1]
        if 'filename*' not in params:
            raise ValueError('Could not find a filename')
        file_name = params['filename*'].replace("UTF-8''", "")

    abs_path = os.path.join(path, os.path.basename(file_name))
    with open(abs_path, 'wb') as target:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, target)

    print(f"Download {file_name}")
