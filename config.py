from dataclasses import dataclass


@dataclass(frozen=True)
class IconVariants:
    light: str
    dark: str


@dataclass(frozen=True)
class Answer:
    name: str
    url: str
    fullname: str
    title: str
    details: str
    icon: str | IconVariants
    action_theme: str
    welcome: str


ANSWERS = [
    Answer(
        name="oj-dsa",
        url="https://raw.githubusercontent.com/GMyhf/2024spring-cs201/refs/heads/main/2024spring_dsa_problems.md",
        fullname="OpenJudge - 数算",
        title="OpenJudge 数算题解",
        details="cs101.openjudge.cn 数算部分题解",
        icon="/icons/oj.jpg",
        action_theme="brand",
        welcome="欢迎来到 OpenJudge 数算部分题解，点击左边目录选择题目。",
    ),
    Answer(
        name="oj",
        url="https://raw.githubusercontent.com/GMyhf/2020fall-cs101/refs/heads/main/2020fall_cs101.openjudge.cn_problems.md",
        fullname="OpenJudge - 计概",
        title="OpenJudge 计概题解",
        details="cs101.openjudge.cn 计概部分题解",
        icon="/icons/oj.jpg",
        action_theme="alt",
        welcome="欢迎来到 OpenJudge 计概部分题解，点击左边目录选择题目。",
    ),
    Answer(
        name="cf",
        url="https://raw.githubusercontent.com/GMyhf/2020fall-cs101/refs/heads/main/2020fall_Codeforces_problems.md",
        fullname="Codeforces",
        title="Codeforces 题解",
        details="codeforces.com 题解",
        icon="/icons/cf.png",
        action_theme="alt",
        welcome="欢迎来到 Codeforces 题解，点击左边目录选择题目。",
    ),
    Answer(
        name="leetcode-em",
        url="https://raw.githubusercontent.com/GMyhf/2024fall-cs101/refs/heads/main/2024fall_LeetCode_problems.md",
        fullname="LeetCode - 易+中",
        title="LeetCode 易+中 题解",
        details="LeetCode 简单+中等难度题解",
        icon=IconVariants(
            light="/icons/leetcode-light.svg",
            dark="/icons/leetcode-dark.svg",
        ),
        action_theme="alt",
        welcome="欢迎来到 LeetCode 简单+中等难度题题解，点击左边目录选择题目。困难题目在隔壁",
    ),
    Answer(
        name="leetcode-tough",
        url="https://raw.githubusercontent.com/GMyhf/2024fall-cs101/refs/heads/main/2024fall_LeetCode_tough_problems.md",
        fullname="LeetCode - 难",
        title="LeetCode 困难题题解",
        details="LeetCode 困难题题解",
        icon=IconVariants(
            light="/icons/leetcode-light.svg",
            dark="/icons/leetcode-dark.svg",
        ),
        action_theme="alt",
        welcome="欢迎来到 LeetCode 困难题题解，点击左边目录选择题目。简单和中等题目在隔壁",
    ),
    Answer(
        name="sunnywhy",
        url="https://raw.githubusercontent.com/GMyhf/2024spring-cs201/refs/heads/main/sunnywhy_problems.md",
        fullname="Sunnywhy",
        title="Sunnywhy 题解",
        details="sunnywhy.com 题解",
        icon="/icons/sunnywhy.jpg",
        action_theme="alt",
        welcome="欢迎来到 Sunnywhy 题解，点击左边目录选择题目。",
    ),
]
