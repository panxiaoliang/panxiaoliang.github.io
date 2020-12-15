==========================================
中英文混合排版和 reStructuredText 中的空格
==========================================

:layout: post
:authors: 潘晓亮
:date: 2020-05-12
:modified: 2020-09-09
:slug: space-in-the-chinese-english-hybrid-typesetting-and-restructuredtext
:category: Computer Technology
:tags: 排版, reStructuredText
:summary:

.. contents::

在中英文混合排版时是否要在中文和英文之间加空格？这个问题困扰了我很长时间。最初
我是没有意识到这个问题的，一般情况下都不加空格。直到有一天，我发现网上很多页面
的内容都会在中文和英文之间加上一个空格。我像是发现了新大陆一样，觉得在中文和英
文之间加上一个空格的这种排版方法简直太优雅了。于是我开始尝试着在中英文混合排版
时也使用这种加空格的方法。但是新的问题又随之而来，不是所有的中英文混合排版加上
空格都好看，有的时候不加空格更好。于是我又开始研究在中英文混合排版的情况下，什
么时候要在中文和英文之间加上一个空格，什么时候不加空格。最终我发现 `知乎`_ 上的
一个类似的问题 `《中英文混排时中文与英文之间是否要有空格？》中梁海的回答`_ 接近
我想要的答案。在这个答案的基础上我整理了符合我个人口味的中英文混合排版加空格规
则：

一般情况下，中英文混合排版时英文及数字应该使用半角方式输入。

以下情况需要在英文左右各加一个半角空格：

- 中文语境中出现的内部有空格的英文短语，例如：iPad Pro。
- 中文语境中出现的独立的英文单词，例如：iPhone。
- 中文语境中出现的全大写字母的英文缩写，例如：HTML。

以下情况不需要加半角空格：

- 英文及数字的左边或者右边紧接着任何的中文全角标点符号。
- 中文语境中出现的单个的英文字母，例如：X。
- 中文语境中出现的纯数字，例如：7。
- 表示标识或概念名称的中英文混合词，例如：捭阖ERP。

接下来再说说 reStructuredText_ 中的空格。reStructuredText 是一种简洁、强壮、优
雅的轻量级标记语言。其实我最开始接触的轻量级标记语言是 Markdown_ 。用了一段时间
Markdown 以后，感觉 Markdown 简洁、易用，但是不够规范、强壮。后来在学习 Python
的过程中接触了 reStructuredText，瞬间就喜欢上了。于是我便将使用的轻量级标记语言
从 Markdown 改为 reStructuredText。在刚开始使用 reStructuredText 的时候，我又接
触了 CommonMark_ 和 `GitHub Flavored Markdown`_ 。当时我非常纠结在
reStructuredText 和 GitHub Flavored Markdown 之间到底选择哪个作为主力轻量级标记
语言。最终我选择了 reStructuredText。在我心目中，reStructuredText 是接近完美的
轻量级标记语言。为什么说是接近完美呢？因为 reStructuredText 的标记指令是空格敏
感的，就是说一般情况下要在 reStructuredText 的标记指令开始前和结束后有一个空格
，否则标记指令无效。这在英文这种以空格区分单词的语境中很自然，不会有什么问题，
甚至很优雅，但是在中文这种不以空格区分单词的语境中就会有些问题了，有些标记指令
会使解析后文本产生多余空格。为了解决这个问题，需要在 reStructuredText 中的适当
位置加上「\\」（反斜杠）。但是这样会降低 reStructuredText 源文件的可读性。经过
再三的权衡，我还是为了 reSturcturedText 源文件的可读性放弃了加「\\」去除解析后
文本产生多余空格的做法。我认为通过扩展 reStructuredText 的方法来解决这个问题是
个不错的思路。将来我可能会写个 rST-CJK 程序来解决这个问题，把 reStructuredText
变成我心目中完美的轻量级标记语言。

.. _知乎: https://www.zhihu.com
.. _《中英文混排时中文与英文之间是否要有空格？》中梁海的回答:
   https://www.zhihu.com/question/19587406/answer/12298128
.. _reStructuredText: https://docutils.sourceforge.io/rst.html
.. _Markdown: https://daringfireball.net/projects/markdown/
.. _CommonMark: https://commonmark.org
.. _GitHub Flavored Markdown: https://github.github.com/gfm/
