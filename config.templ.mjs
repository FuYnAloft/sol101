import {defineConfig} from 'vitepress'
import mark from 'markdown-it-mark'

// https://vitepress.dev/reference/site-config
export default defineConfig({
    base: '/sol101/',
    lang: "zh-CN",
    title: "Solutions CS101",
    description: "OJ 和 CF 的题解",
    markdown: {
        math: true,
        vue: false,
        languages: ['python', 'cpp'],
        config: (md) => {
            md.use(mark)
        }
    },
    themeConfig: {
        // https://vitepress.dev/reference/default-theme-config
        nav: [
            {text: 'Home', link: '/'},
            {text: 'Openjudge', link: '/oj.md'},
            {text: 'Codeforces', link: '/cf.md'}
        ],

        socialLinks: [
            {icon: 'github', link: 'https://github.com/FuYnAloft/sol101'}
        ],

        sidebar: {
            // template: sidebar
        },

        outline: {
            level: [2, 6],
            label: '大纲'
        },

        footer: {
            message: '仓库地址：<a href=https://github.com/FuYnAloft/sol101>https://github.com/FuYnAloft/sol101</a>',
        },

        search: {
            provider: 'local',
            options: {
                locales: {
                    root: {
                        translations: {
                            button: {
                                buttonText: '搜索',
                                buttonAriaLabel: '搜索'
                            },
                            modal: {
                                displayDetails: '显示详细列表',
                                resetButtonTitle: '重置搜索',
                                backButtonTitle: '关闭搜索',
                                noResultsText: '没有结果',
                                footer: {
                                    selectText: '选择',
                                    selectKeyAriaLabel: '输入',
                                    navigateText: '导航',
                                    navigateUpKeyAriaLabel: '上箭头',
                                    navigateDownKeyAriaLabel: '下箭头',
                                    closeText: '关闭',
                                    closeKeyAriaLabel: 'esc'
                                }
                            }
                        }
                    }
                }
            }
        }
    }
})
