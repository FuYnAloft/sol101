# Solutions101

**网站地址**: https://fuynaloft.github.io/sol101/

这是一个算法题目题解网站，题目来源于 [openjudge](http://cs101.openjudge.cn) 和 [codeforces](https://codeforces.com/)，
题解来源于 [GMyhf/2020fall-cs101](https://github.com/GMyhf/2020fall-cs101)。
本项目将原版的长 Markdown 文件拆分成独立的题解文件，并使用 VitePress 构建成方便阅读的网站，同时使用 GitHub Actions 实现自动更新和构建。

## 本地构建

### 环境要求

- Node.js 20 或更高版本
- npm (通常随 Node.js 一起安装)
- Python 3.x (可选，用于运行更新和拆分脚本)
- pip, venv (通常随 Python 一起安装)

### 构建步骤

1. 克隆仓库：
   ```bash
   git clone https://github.com/FuYnAloft/sol101.git
   cd sol101
   ```

2. （可选）创建虚拟环境并安装 Python 依赖 ：
   ```bash
   python -m venv # 创建虚拟环境
   # 激活虚拟环境
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt # 安装依赖
   ```

3. （可选）运行更新和拆分脚本：
   ```bash
   # 确保激活虚拟环境后运行
   python update.py
   python split.py
   ```

4. 安装 Node.js 依赖：
   ```bash
   npm ci
   ```

5. 构建 VitePress 网站：
   ```bash
   npm run docs:build
   ```

生成的网站文件位于 `docs/.vitepress/dist` 目录。你可以运行 `npm run docs:preview` 来预览构建结果。

## 贡献

欢迎贡献！如果你发现问题或有改进建议，请：

1. 最好先开个 issue 进行讨论
2. Fork 本仓库
3. 创建你的特性分支，提交修改并推送到你的 Fork
4. 开启一个 Pull Request

**注意**：题解内容来源于上游仓库，如需修改题解内容，请前往 [GMyhf/2020fall-cs101](https://github.com/GMyhf/2020fall-cs101) 提交修改。

## 题解来源

题解主要来源于[GMyhf/2020fall-cs101](https://github.com/GMyhf/2020fall-cs101)，感谢所有为该项目贡献题解的同学们。

题目来源：
- [cs101.openjudge.cn](http://cs101.openjudge.cn)
- [Codeforces](https://codeforces.com)

## 许可证

本项目仅用于学习交流，题解版权归原作者所有。
