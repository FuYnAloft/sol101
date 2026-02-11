from dataclasses import dataclass

@dataclass(frozen=True)
class Answer:
    name: str
    url: str


ANSWERS = [
    Answer(
        name="oj",
        url="https://raw.githubusercontent.com/GMyhf/2020fall-cs101/refs/heads/main/2020fall_cs101.openjudge.cn_problems.md"
    ),
    Answer(
        name="cf",
        url="https://raw.githubusercontent.com/GMyhf/2020fall-cs101/refs/heads/main/2020fall_Codeforces_problems.md"
    ),
]