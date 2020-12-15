==============================
将博客从 Pelican 迁移到 Jekyll
==============================

:layout: post
:authors: 潘晓亮
:date: 2020-04-12
:modified: 2020-09-10
:slug: move-blog-from-pelican-to-jekyll
:category: Computer Technology
:tags: 博客, Pelican, Jekyll, GitHub Pages
:summary:

.. contents::

经过一番折腾后，我还是决定将博客从 Pelican_ 迁移到 Jekyll_ 。主要是因为：

1. 在研究了 `GitHub Flavored Markdown`_ 以后，我决定将轻量级标记语言从原来使用
   的 reStructuredText_ 改成 GitHub Flavored Markdown。Pelican 支持 Markdown 的
   依赖包是 Python-Markdown_ ，语法上与 GitHub Flavored Markdown 有些差别，有个
   pelican-commonmark_ 插件，不过这个插件已经停止更新了，最新的版本0.1.0是
   2015-05-03发布的，要想正常使用这个插件还得修改一些代码，但是即使修改完代码让
   这个插件正常使用了以后的效果也不太理想。而 Jekyll 支持 Markdown 用的依赖包是
   kramdown_ ，对 GitHub Flavored Markdown 支持良好。

2. 使用 Pelican 时，要想将博客实例的源代码和生成的网页都托管到 GitHub_ 上，需要
   创建2个代码仓库。一个用于托管 Pelican 实例的源代码，一个用于托管 Pelican 生
   成的网页。而 Jekyll 是 `GitHub Pages`_ 的原生环境，只需要创建一个代码仓库，
   然后将 Jekyll 实例的源代码 ``push`` 到这个代码仓库即可。

接下来说说将博客从 Pelican 迁移到 Jekyll 过程中的一些感受。

总的来说，迁移过程非常顺利，按照 Jekyll 和 GitHub Pages 的官方文档配置部署后，
再将页面和文章的相关文件复制到 Jekyll 相对应的目录下，然后再简单的修改了页面和
文章内容的一些格式，就可以了。博客迁移到了 Jekyll 以后，我对页面和文章的链接网
址做了一些调整，以前的链接就失效了，要想查看以前的内容可以到 `我的博客首页`_ 通
过搜索功能查找。

`Jekyll 的官方文档`_ 写得很详尽，所有的常见问题都可以通过官方文档解决。
`Jekyll 的主题和插件`_ 在官网上都有相关资源的链接。我的博客使用的主题是 NexT_
，是从另一个静态网页生成器 Hexo_ 的 `NexT 主题`_\ 移植过来的。由于 Jekyll 是用
Ruby_ 写的，所以我在研究 Jekyll 的过程中也顺便研究了一下 Ruby 的部署和依赖包管
理工具：rbenv_, RubyGems_, Bundler_ 。感觉 Ruby 的部署和依赖包管理工具做得真好
，比 Python_ 的好。

.. _Pelican: http://getpelican.com
.. _Jekyll: https://jekyllrb.com
.. _GitHub Flavored Markdown: https://github.github.com/gfm/
.. _reStructuredText: https://docutils.sourceforge.io/rst.html
.. _Python-Markdown: https://python-markdown.github.io
.. _pelican-commonmark: https://github.com/theskumar/pelican-commonmark
.. _kramdown: https://github.com/gettalong/kramdown
.. _GitHub: https://github.com
.. _GitHub Pages: https://pages.github.com
.. _我的博客首页: https://panxiaoliang.github.io
.. _Jekyll 的官方文档: https://jekyllrb.com/docs/
.. _Jekyll 的主题和插件: https://jekyllrb.com/resources/
.. _NexT: https://github.com/Simpleyyt/jekyll-theme-next
.. _Hexo: https://hexo.io
.. _NexT 主题: https://github.com/iissnan/hexo-theme-next
.. _Ruby: https://www.ruby-lang.org
.. _rbenv: https://github.com/rbenv/rbenv
.. _RubyGems: https://rubygems.org
.. _Bundler: https://bundler.io
.. _Python: https://www.python.org
