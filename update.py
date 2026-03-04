import os
import sys

import requests

from config import ANSWERS

# 如果命令行参数中包含 --force，则强制全量更新，否则使用 ETag 进行增量更新
FORCE_UPDATE = '--force' in sys.argv


def sync_github(url, etag_path):
    headers = {}
    if not FORCE_UPDATE and os.path.exists(etag_path): # 如果强制全量更新，则不使用 ETag 进行增量更新
        with open(etag_path, "r") as f:
            etag = f.read().strip()
            if etag:
                headers["If-None-Match"] = etag

    resp = requests.get(url, headers=headers, timeout=10)

    if resp.status_code == 304:
        # 文件未变化
        return -1, ""

    elif resp.status_code == 200:
        # 文件更新
        etag = resp.headers.get("ETag")
        if etag:
            os.makedirs(os.path.split(etag_path)[0], exist_ok=True)
            with open(etag_path, "w") as f:
                f.write(etag)

        content = resp.text
        return 0, content

    else:
        # 其他错误
        raise requests.HTTPError(resp.status_code)


def main():
    changed = 0
    for answer in ANSWERS:
        name = answer.name
        url = answer.url
        ret, content = sync_github(url, rf"etag/{name}")
        if ret == 0:
            changed += 1
            os.makedirs('original', exist_ok=True)
            with open(f'original/{name}.md', 'w', encoding='utf-8') as f:
                f.write(content)

    if changed:
        print('true')
    else:
        print('false')


if __name__ == '__main__':
    main()
