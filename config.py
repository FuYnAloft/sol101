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
        name="oj",
        url="https://raw.githubusercontent.com/GMyhf/2020fall-cs101/refs/heads/main/2020fall_cs101.openjudge.cn_problems.md",
        fullname="OpenJudge",
        title="OpenJudge的题解",
        details="cs101.openjudge.cn的题解",
        icon="/icon-oj.jpg",
        action_theme="brand",
        welcome="欢迎来到OpenJudge题库",
    ),
    Answer(
        name="cf",
        url="https://raw.githubusercontent.com/GMyhf/2020fall-cs101/refs/heads/main/2020fall_Codeforces_problems.md",
        fullname="Codeforces",
        title="Codeforces的题解",
        details="codeforces.com的题解",
        icon="/icon-cf.png",
        action_theme="alt",
        welcome="欢迎来到Codeforces题库",
    ),
]