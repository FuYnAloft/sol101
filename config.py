from dataclasses import dataclass

@dataclass(frozen=True)
class Answer:
    name: str
    url: str
    fullname: str
    title: str
    details: str
    icon: str
    action_theme: str
    welcome: str


ANSWERS = [
    Answer(
        name="oj-dsa",
        url="https://raw.githubusercontent.com/GMyhf/2024spring-cs201/refs/heads/main/2024spring_dsa_problems.md",
        fullname="OpenJudge - 数算",
        title="OpenJudge 数算题解",
        details="cs101.openjudge.cn 数算部分的题解",
        icon="/icon-oj.jpg",
        action_theme="brand",
        welcome="欢迎来到 OpenJudge 数算部分的题解",
    ),
    Answer(
        name="oj",
        url="https://raw.githubusercontent.com/GMyhf/2020fall-cs101/refs/heads/main/2020fall_cs101.openjudge.cn_problems.md",
        fullname="OpenJudge - 计概",
        title="OpenJudge 计概题解",
        details="cs101.openjudge.cn 计概部分的题解",
        icon="/icon-oj.jpg",
        action_theme="alt",
        welcome="欢迎来到 OpenJudge 计概部分的题解",
    ),
    Answer(
        name="cf",
        url="https://raw.githubusercontent.com/GMyhf/2020fall-cs101/refs/heads/main/2020fall_Codeforces_problems.md",
        fullname="Codeforces",
        title="Codeforces 题解",
        details="codeforces.com的题解",
        icon="/icon-cf.png",
        action_theme="alt",
        welcome="欢迎来到 Codeforces 题解",
    ),
]