===============================
用 GitHub Pages 和 Pelican 建站
===============================

:layout: post
:authors: 潘晓亮
:date: 2019-07-09
:modified: 2020-09-24
:slug: creating-a-website-with-github-pages-and-pelican
:category: Computer Technology
:tags: GitHub, GitHub Pages, Pelican, 建站
:summary:

.. contents::

作为一个喜欢偶尔写写文章的计算机技术爱好者，用 `GitHub Pages`_ 和 Pelican_ 建站
发表文章是我最喜欢的一种方式。今天我就把这种方式介绍给你，下面我来简单的讲解下
如何用 GitHub Pages 和 Pelican 建站。

用 GitHub Pages 和 Pelican 建站需要具备使用 GitHub_ 和搭建 `Python 虚拟环境`_
的相关知识。如果你还不熟悉这些知识，那么需要你先学习一下 `Pro Git`_ 和
`Django Girls 教程`_ 。

下面是用 GitHub Pages 和 Pelican 建站的操作步骤：

1. 注册一个 GitHub 账号，然后在 GitHub 上创建一个名称为 ``<user>.github.io`` 的
   公开代码仓库。在创建代码仓库时需要选择用于 Python_ 的 ``.gitignore`` ，并且
   选择一个 `自由软件许可证`_ 。

2. 安装最新版本的 Git_, Python_ 和 Virtualenv_

3. 将 ``<user>.github.io`` 克隆到本地

4. 创建 Pelican 的 Python 虚拟环境

5. 安装最新版本的 Pelican

6. 在本地 ``<user>.github.io`` 的根目录下创建 Pelican 实例，然后修改
   ``pelicanconf.py`` 中的 ``OUTPUT_PATH`` 值为 ``docs`` 。

7. 安装 Pelican `主题`_ 和 `插件`_

8. 在本地 ``<user>.github.io`` 的 ``content`` 目录下创建后缀名为 ``.rst`` 的纯
   文本文件，然后用 reStructuredText_ 语法撰写文章。

9. 在本地 ``<user>.github.io`` 的根目录下使用 ``pelican`` 命令将文章输出为网页
   文件存储到 ``docs`` 目录

10. 使用 Git 命令将本地 ``<user>.github.io`` push 到 GitHub

11. 在 GitHub 的 ``<user>.github.io`` 的 ``Settings`` 找到 ``GitHub Pages`` 选
    项，将 ``Branch`` 选择为 ``master`` ，将 ``Floder`` 选择为 ``/docs`` ，再点
    击 ``Save`` 按钮。然后再勾选 ``Enforce HTTPS`` 。

12. 如果以后想要发表新文章，重复步骤8-10即可。

以上的操作步骤是我用 GitHub Pages 和 Pelican 建站的一个简单的笔记。如果你看不太
明白，建议你阅读这篇 `Creating a blog with Pelican and GitHub Pages`_ ，译文叫
做 `使用 Pelican 和 GitHub Pages 来搭建博客`_ 。

最后推荐一个 Pelican 主题和一些相关的 Pelican 插件，这个主题叫做 Elegant_ ，与
其相关的 Pelican 插件有：

.. code-block:: shell

   sitemap
   extract_toc
   tipue_search
   neighbors
   assets

可以在 `Pelican 插件的 GitHub 代码仓库`_ 中获取以上插件。

.. _Git: https://git-scm.com
.. _Pro Git: https://git-scm.com/book/zh
.. _GitHub: https://github.com
.. _GitHub Pages: https://pages.github.com
.. _自由软件许可证: https://www.gnu.org/licenses/license-list.html
.. _Python: https://www.python.org
.. _Python 虚拟环境: https://virtualenv.pypa.io
.. _Virtualenv: https://virtualenv.pypa.io
.. _Django Girls 教程: https://tutorial.djangogirls.org/zh/
.. _reStructuredText: http://docutils.sourceforge.io/rst.html
.. _Pelican: http://getpelican.com
.. _主题: https://github.com/getpelican/pelican-themes
.. _插件: https://github.com/getpelican/pelican-plugins
.. _Elegant: https://github.com/Pelican-Elegant/elegant
.. _Creating a blog with Pelican and GitHub Pages:
   https://rsip22.github.io/blog/create-a-blog-with-pelican-and-github-pages.html
.. _使用 Pelican 和 GitHub Pages 来搭建博客:
   https://linux.cn/article-9445-1.html
.. _Pelican 插件的 GitHub 代码仓库:
   https://github.com/getpelican/pelican-plugins
