import os.path
from dataclasses import dataclass
from typing import Iterable

import requests

from config import Answer, ANSWERS


@dataclass(frozen=True)
class UpdateResult:
    updated: bool
    content: str | None = None
    etag: str | None = None


def update_github(url: str, etag: str | None) -> UpdateResult:
    headers: dict[str, str] = {}
    if etag:
        headers["If-None-Match"] = etag

    response = requests.get(url, headers=headers, timeout=10)

    match response.status_code:
        case 304:
            return UpdateResult(False)

        case 200:
            etag = response.headers.get("ETag")
            content = response.text
            return UpdateResult(True, content, etag)

        case _:
            raise Exception(f"Unexpected status code: {response.status_code}")


def update_answer(answer: Answer) -> bool:
    etag_path = f"etag/{answer.name}.etag"
    if os.path.exists(etag_path):
        with open(etag_path, "r") as f:
            etag = f.read().strip()
    else:
        etag = None
    result = update_github(answer.url, etag)
    updated = result.updated

    # 如果没更新，把 etag 设成 None 强制下载，并覆盖 result
    if not updated:
        result = update_github(answer.url, None)

    os.makedirs('original', exist_ok=True)
    with open(f'original/{answer.name}.md', 'w', encoding='utf-8') as f:
        f.write(result.content or "")
    os.makedirs('etag', exist_ok=True)
    with open(etag_path, "w") as f:
        f.write(result.etag or "")

    return updated


def update(answers: Iterable[Answer]) -> bool:
    updated = False
    for answer in answers:
        if update_answer(answer):
            print(f"Updated {answer.name}")
            updated = True
        else:
            print(f"No update for {answer.name}")
    return updated


if __name__ == "__main__":
    update(ANSWERS)