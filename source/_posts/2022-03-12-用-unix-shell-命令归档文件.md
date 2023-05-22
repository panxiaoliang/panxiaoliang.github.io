---
title: 用 Unix Shell 命令归档文件
date: 2022-03-12
categories: 计算机技术
tags:
    - Unix
    - Unix Shell
    - 归档
---

我最近有了把[百度网盘]当做备份盘的想法，但百度网盘对于非会员用户限制上传单个文件不能超过 4G。这样的话就只能将文件以 4G 为一个单位分卷压缩归档后再上传到百度网盘了。我选择的方案是用 Unix Shell 命令将文件分卷压缩归档，涉及到的 Unix Shell 命令有：`tar`、`split` 和 `cat`。

在开始介绍这些 Unix Shell 命令的用法之前我先说下我的运行环境。我的操作系统是 macOS Monterey 12.1，使用的 Unix Shell 是 [Zsh] 5.8。因为 `tar`、`split` 和 `cat` 是标准的 Unix Shell 命令，所以这些命令在 FreeBSD 和 Linux 这些类 Unix 系统下是同样有效的。

接下来我就简单地聊聊如何在不同的场景下应用这些 Unix Shell 命令。

[百度网盘]: https://pan.baidu.com
[Zsh]: https://www.zsh.org

<!-- more -->

## 压缩归档文件

如果只是将一个或多个文件压缩归档，那么只使用 `tar` 这个 Unix Shell 命令就可以了。

[维基百科的 tar 词条]是这样介绍的：

> tar 是 Unix 和类 Unix 系统上的归档打包工具，可以将多个文件合并为一个文件，打包后的文件名亦为“tar”。目前，tar 文件格式已经成为 POSIX 标准，最初是 POSIX.1-1988，目前是 POSIX.1-2001。本程序最初的设计目的是将文件备份到磁带上（tape archive），因而得名 tar。
>
> 常用的 tar 是自由软件基金会开发的 GNU 版，目前的稳定版本是1.33，发布于2021年1月7日。
>
> tar 代表未压缩的 tar 文件。已压缩的 tar 文件则附加数据压缩格式的扩展名，如经过 gzip 压缩后的 tar 文件，扩展名为“.tar.gz”。

`tar` 的命令格式：

```bash
tar <参数 [选项]> <文件>
```

`tar` 的常用参数：

- `-c`，创建新的 `tar` 文件。
- `-f`，指定要处理的文件名，可以用 `-` 代表标准输入或标准输出。
- `-v`，列出每一步处理涉及的文件的信息，只用一个 `v` 时，仅列出文件名，使用两个 `v` 时，列出权限、所有者、大小、时间、文件名等信息。
- `-x`，解开 `tar` 文件。
- `-z`，调用 `gzip` 执行压缩或解压缩。

比如想要将当前目录下的 `personal-files` 目录创建成一个以 zip 格式压缩的 tar 文件并命名为 `pfiles.tar.gz`：

```bash
tar -czvf pfiles.tar.gz personal-files
```

将 `pfiles.tar.gz` 解压缩：

```bash
tar -xzvf pfiles.tar.gz
```

[维基百科的 tar 词条]: https://zh.wikipedia.org/wiki/Tar

## 分卷压缩归档文件

如果想要实现将一个或多个文件分卷压缩归档，那么我们需要结合使用 `tar` 和 `split` 这两个 Unix SHell 命令。

[维基百科的 split 词条]是这样介绍的：

> split 是一个 Unix 实用程序，最常用于将文件分割成两个或更多个较小的文件。
>
> split 默认生成固定大小的输出文件，默认为1000行。这些文件的命名方式是在输出文件名后添加 aa、ab、ac 等后缀。 如果没有给出输出文件名，则使用默认的文件名x，例如 xaa、xab 等。输入文件名为连字符（-）时，将从标准输入中读取数据。

`split` 的命令格式：

```bash
split [参数 [选项]] [输入 [前缀]]
```

`split` 的常用参数：

- `-a`，指定生成文件后缀的长度。
- `-b`，指定每多少字节就要切割成一个小文件，支持单位：`k`、`m`。
- `-d`，以数字生成文件后缀，此参数为非 Unix 标准参数，通常在 Linux 环境下有效，在 macOS 下无效。
- `-l`，指定每多少行就要切割成一个小文件。

比如我们要将前面生成的 `pfiles.tar.gz` 文件以 4G 为一个单位进行分卷，生成的文件后缀的长度为4并指定生成的文件名前缀为 `pfiles-part.tar.gz`：

```bash
split -b 4096m -a 4 pfiles.tar.gz pfiles-part.tar.gz.
```

如果想要直接将当前目录下的 `personal-files` 目录以 4G 为一个单位分卷压缩为 `.tar.gz` 文件，生成的文件后缀的长度为4并指定生成的文件名前缀为 `pfiles-part.tar.gz`：

```bash
tar -czvf - personal-files | split -b 4096m -a 4 - pfiles-part.tar.gz.
```

如果想要解压缩多个分卷压缩后的 `.tar.gz` 文件，那么我们需要结合使用 `cat` 和 `tar` 这两个 Unix Shell 命令。

[维基百科的 cat 词条]是这样介绍的：

> cat 是 Unix 系统下用来检视档案连续内容用的指令，字面上的含意是“concatenate”(连续)的缩写。除了用来作为显示档案内容外，cat 指令也可用于标准串流上的处理，如将显示的讯息转入或附加另一档案上。

`cat` 的命令格式：

```bash
cat [参数 [选项]] [文件]
```

比如我们想要将前面生成的多个文件 `pfiles-part.tar.gz.*` 解压缩：

```bash
cat pfiles-part.tar.gz.* | tar -xzv
```

[维基百科的 split 词条]: https://zh.wikipedia.org/wiki/Split_(Unix)
[维基百科的 cat 词条]: https://zh.wikipedia.org/wiki/Cat_(Unix)

（全文完）

## 参考链接

- <https://zh.wikipedia.org/wiki/Tar>
- <https://zh.wikipedia.org/wiki/Split_(Unix)>
- <https://zh.wikipedia.org/wiki/Cat_(Unix)>
- <https://wangying.sinaapp.com/archives/2574>
