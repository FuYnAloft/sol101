# sol101

**网站地址**: https://fuynaloft.github.io/sol101/

这是一个算法题目题解网站，题解来源于 [GMyhf/2020fall-cs101](https://github.com/GMyhf/2020fall-cs101)。本项目将原版的长 Markdown 文件拆分成独立的题解文件（一道题一个），并使用 VitePress 构建成网站方便阅读，同时使用 GitHub Actions 实现自动更新和构建。

## 本地构建

### 环境要求

- Node.js 20 或更高版本
- Python 3.x
- npm

### 构建步骤

1. 克隆仓库：
```bash
git clone https://github.com/FuYnAloft/sol101.git
cd sol101
```

2. 安装 Python 依赖：
```bash
pip install -r requirements.txt
```

3. 安装 Node.js 依赖：
```bash
npm ci
```

4. （可选）运行更新和拆分脚本：
```bash
python update.py
python split.py
```

5. 构建 VitePress 网站：
```bash
npm run docs:build
```

生成的网站文件位于 `docs/.vitepress/dist` 目录。

### 本地预览

如果你想在本地预览网站，可以运行：
```bash
npm run docs:dev
```

然后在浏览器中访问 `http://localhost:5173`（或终端显示的地址）。

## 更新流程

本项目通过 GitHub Actions 自动更新题解内容：

1. **自动更新**：每天 UTC 00:00 自动运行更新流程
2. **update.py**：从上游仓库检查并下载最新的题解文件
   - 使用 ETag 检测文件变化
   - 下载的文件保存到 `original/` 目录
   - 如果有更新则输出 `true`，否则输出 `false`
3. **split.py**：将长 Markdown 文件拆分成独立的题解文件
   - 根据标题（# 和 ##）拆分文件
   - 生成 VitePress 侧边栏配置
   - 输出到 `docs/cf/` 和 `docs/oj/` 目录
4. **自动提交**：如有更新，自动提交并推送到仓库
5. **自动部署**：当 `docs/` 目录有变化时，自动构建并部署到 GitHub Pages

### 手动触发更新

如需手动触发更新，可以在 GitHub Actions 页面手动运行 "Auto Update, Split and Commit" 工作流。

## 贡献

欢迎贡献！如果你发现问题或有改进建议，请：

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的修改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个 Pull Request

**注意**：题解内容来源于上游仓库，如需修改题解内容，请前往 [GMyhf/2020fall-cs101](https://github.com/GMyhf/2020fall-cs101) 提交修改。

## 题解来源

题解主要来源于：
- yhf 老师的"计算概论"和"数据结构与算法"课程学生
- 其他老师的学生贡献

题目来源：
- [cs101.openjudge.cn](http://cs101.openjudge.cn)
- [Codeforces](https://codeforces.com)

## 许可证

本项目仅用于学习交流，题解版权归原作者所有。
