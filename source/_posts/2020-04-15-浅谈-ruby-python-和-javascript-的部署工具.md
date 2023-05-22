---
title: 浅谈 Ruby、Python 和 JavaScript 的部署工具
date: 2020-04-15
categories: 计算机技术
tags:
    - Ruby
    - Python
    - JavaScript
    - 部署工具
---

最近在研究 [Ruby on Rails] 和 [Django]，发现 Ruby on Rail 6 默认集成了基于 [Node.js] 的前端组件。Ruby on Rails、Django 和基于 Node.js 的前端组件分别是用 [Ruby]、[Python] 和 [JavaScript] 写的，这三种编程语言都有自己的部署工具，而且每个编程语言都有不只一个部署工具，并且部署工具之间的关系错综复杂。为此我在研究如何使用这些部署工具上花了不少工夫。其实我是先学习的 Python，所以是先研究的 Django。但是为什么把 Ruby 和 Ruby on Rails 放在前面讲呢？因为我觉得 Ruby 的部署工具是这三种编程语言中做得最好的。下面我就来分享下我对这三种编程语言部署工具的认识。为了更清晰的阐述这三种编程语言的各个部署工具的作用和它们之间的关系，我们先来看一些概念：

- **操作系统的软件包管理器**：操作系统上的软件包管理工具，用于管理操作系统上的应用软件包。像 Ruby 和 Python 这样的动态编程语言的解释器其实也是一种应用软件，所以操作系统的软件包管理器也可以用于安装、删除 Ruby 和 Python 的某个或多个版本的解释器。
- **编程语言的版本管理器**：用于管理编程语言解释器各版本运行环境的增强工具。虽然操作系统的软件包管理器可以用于安装、删除编程语言的某个或多个版本的解释器，但是想在各版本运行环境中进行切换需要执行复杂繁琐的 shell 命令。借助编程语言的版本管理器可以很轻松地安装、删除、切换多个版本的运行环境。
- **编程语言的包管理器**：编程语言的运行环境中附带的包管理工具，用于管理编程语言相关的软件包。
- **编程语言的包依赖关系管理器**：编程语言的包管理器的增强工具。在编程语言的包管理器的基础上，针对包依赖关系管理方面的功能进行了加强与扩展。

这些概念都是我自己定义的，看完了是不是有一知半解的感觉？而且还是不知道在什么时候该用哪个部署工具？的确，上面概念中的各种管理器之间的功能和应用场景的边界很模糊。其实你只需要记住：

「操作系统的软件包管理器」是用来安装「编程语言的版本管理器」用的，「编程语言的版本管理器」是用来安装各版本编程语言的运行环境用的；用「编程语言的包管理器」安装「编程语言的包依赖关系管理器」，用「编程语言的包依赖关系管理器」借助「编程语言的包管理器」管理编程语言的相关软件包。

这个规则就可以了。是不是觉得很绕口？在 macOS 下以 Ruby 为例就是：

[Homebrew] 是用来安装 [rbenv] 用的，rbenv 是用来安装各版本 Ruby 的运行环境用的；用 [RubyGems] 安装 [Bundler]，用 Bundler 借助 RubyGems 管理 Ruby 的相关软件包。

其实 Ruby、Python 和 JavaScript 这三种编程语言都有着自己的设计哲学，所以相关的部署工具在实现细节上都有些差异。接下来我再具体说说这三种编程语言的部署工具。

先说下我的运行环境， **我的操作系统是 macOS Catalina 10.15.4，操作系统的软件包管理器是 Homebrew。**

[Ruby on Rails]: https://rubyonrails.org
[Django]: https://www.djangoproject.com
[Node.js]: https://nodejs.org
[Ruby]: https://www.ruby-lang.org
[Python]: https://www.python.org
[JavaScript]: https://zh.wikipedia.org/wiki/JavaScript
[Homebrew]: https://brew.sh
[rbenv]: https://github.com/rbenv/rbenv
[RubyGems]: https://rubygems.org
[Bundler]: https://bundler.io

<!-- more -->

## Ruby 篇

Ruby 有两个比较著名的版本管理器，分别是 [RVM] 和 rbenv。其中 RVM 是大而全的设计，而 rbenv 是小而美的设计。

RVM 是一个机制完善并且功能强大的 Ruby 版本管理器。RVM 除了 Ruby 版本管理器功能外，还通过 gemsets 对 Ruby 的包管理功能进行了增强。就是说 RVM 可以用于安装、删除、切换多个独立的 Ruby 运行环境，并且可以对各个环境下的 Ruby 包进行管理。

按理来说 RVM 的功能已经非常强大了，我们应该别无他求了。为什么还会有人开发出来了其他的 Ruby 版本管理器呢？RVM 功能强大带来的副作用就是设置起来相对复杂，而且 RVM 会改动 shell 命令。于是就有人为了解决 RVM 的这些问题而开发出来了 rbenv。

rbenv 是一个小而美，够用就好的 Ruby 版本管理器。rbenv 遵循只做一件事并且做好的 Unix 设计哲学，它的功能只专注于 Ruby 版本管理。rbenv 安装 Ruby 的功能是通过一个叫 [ruby-build] 的插件实现的，本身没有管理 Ruby 包依赖关系的功能的，而是推荐使用 Bundler 来作为 Ruby 的包依赖关系管理器。rbenv 的官方文档里有一篇文章《[Why choose rbenv over RVM?]》解释了它和 RVM 的区别。

就我个人来说，我更喜欢 rbenv。可以说 rbenv 简单够用，在 Ruby 版本管理方面的功能比 RVM 好，在使用 Bundler 作为 Ruby 的包依赖关系管理器后完全就不需要 RVM 的 gemsets 功能了。

说完 Ruby 的版本管理器我们再来看看 Ruby 的包管理器——RubyGems。

> RubyGems 是 Ruby 的一个包管理器，提供了分发 Ruby 程序和库的标准格式“gem”，旨在方便地管理 gem 安装的工具，以及用于分发 gem 的服务器。RubyGems 大约创建于2003年11月，从 Ruby 1.9 版起成为 Ruby 标准库的一部分。

上面这段话摘自[维基百科的 RubyGems 介绍]。

Ruby 的包依赖关系管理器叫做 Bundler，这个前文已经有所提及。Bundler 主要用来管理 RubyGems 的依赖关系。一般情况下，一个 Ruby 项目会使用多个 gem，而各个 gem 都有自己的依赖包，这些 gem 的依赖包又会交叉重叠，并且会有多个 gem 依赖同一个包的不同版本的情况。Ruby 的做法是同一个版本的运行环境下可以同时安装一个 gem 的多个版本，然后通过 Bundler 来管理这些 gem 的依赖关系。Bundler 先用 Gemfile 记录项目中都使用了哪些 gem，然后计算出不同 gem 的依赖关系并生成 Gemfile.lock 记录确切的 gem 名称和版本号以及它们所依赖的 gem 的名称和版本号。当第一次运行 `bundle install` 时，Bundler 会根据 Gemfile 自动生成 Gemfile.lock。以后每次运行 `bundle install` 时，如果 Gemfile 中的条目不变 Bundler 就不会再次计算 gem 依赖版本号，直接根据 Gemfile.lock 检查和安装 gem。如果出现依赖冲突时可以通过 `bundle update` 更新 Gemfile.lock。

接下来我以创建一个 Ruby on Rails 项目为例来说明如何使用 rbenv、RubyGems 和 Bundler。

1. 使用 Homebrew 安装 rbenv：

   ```bash
   $ brew install rbenv
   ```

   执行上面的命令后会同时安装 rbenv 的 ruby-build 插件。然后：

   ```bash
   $ rbenv init
   ```

   根据提示设置 rbenv 的 shell 集成，设置完成后关闭并重新打开终端。

2. 使用 rbenv 安装 Ruby：

   ```bash
   $ rbenv install --list
   ```

   查看有哪些可安装的 Ruby 版本，比如要安装 Ruby 2.6.6：

   ```bash
   $ rbenv install 2.6.6
   ```

   安装完成后将 Ruby 的本地版本切换到2.6.6：

   ```bash
   $ rbenv local 2.6.6
   ```

3. 使用 RubyGems 安装 Bundler：

   ```bash
   $ gem install bundler
   ```

4. 使用 RubyGems 安装 Ruby on Rails：

   ```bash
   $ gem install rails
   ```

5. 创建一个 Ruby on Rails 项目：

   ```bash
   $ rails new railsporject
   ```

   上面命令中的 `railsproject` 是项目名，可以改成你想起的名字。另外目前最新版的 Ruby on Rails 6.0.2.2 的安装脚本集成了 Node.js，所以创建项目前需要安装 Node.js。如何安装 Node.js 请看本文的 JavaScript 篇。

6. 启动刚刚创建的 Ruby on Rails 项目服务器：

   ```bash
   $ cd railsproject
   $ bundle exec rails server
   ```

   打开浏览器在地址栏中输入 `http://localhost:3000`，出现「Yay! You’re on Rails!」页面，说明项目创建并启动成功。

[RVM]: https://rvm.io
[ruby-build]: https://github.com/rbenv/ruby-build
[Why choose rbenv over RVM?]: https://github.com/rbenv/rbenv/wiki/Why-rbenv%3F
[维基百科的 RubyGems 介绍]: https://zh.wikipedia.org/wiki/RubyGems

## Python 篇

Python 的主流部署工具是 [Virtualenv]，包管理器是 [pip]。和 Ruby 的部署工具设计理念不同，Virtualenv 以项目为单位创建完全独立的 Python 运行环境。Virtualenv 本身是一个 Python 的软件包，所以需要先安装 Python 后再通过 pip 安装 Virtualenv。Virtualenv 不能用于安装 Python 解释器，只能在操作系统已经安装的各个 Python 解释器版本下创建运行环境。Python 的包管理器 pip 除了用来安装包之外还可以管理包依赖关系，pip 通过 requirements.txt 来记录项目的依赖包列表，然后再结合 Virtualenv 实现完整的项目运行环境管理功能。

有很长一段时间我都是用 Homebrew 安装 Python，然后再用 pip 结合 Virtualenv 的方式来管理 Pyhton 的运行环境。后来接触到 Ruby，我觉得 Ruby 的部署工具的管理方式更好些。我便开始寻找 Python 有没有接近 Ruby 的管理方式的部署工具，于是我找到了 [pyenv] 和 [Pipenv]。pyenv 是 Python 的版本管理器，功能和设计理念完全照搬了 rbenv。Pipenv 的功能类似 Bundler，但是结合 Virtualenv 做出了 Python 自有的特色。有了 pyenv 和 Pipenv 以后就意味着我可以按照 Ruby 的方式部署 Python 的运行环境了。

接下来我以创建一个 Django 项目为例来说明如何使用 pyenv、pip、Virtualenv 和 Pipenv。

1. 使用 Homebrew 安装 pyenv：

   ```bash
   $ brew install pyenv
   ```

   然后：

   ```bash
   $ pyenv init
   ```

   根据提示设置 pyenv 的 shell 集成，设置完成后关闭并重新打开终端。

2. 使用 pyenv 安装 Python：

   ```bash
   $ pyenv install --list
   ```

   查看有哪些可安装的 Python 版本，比如要安装 Python 3.8.2：

   ```bash
   $ pyenv install 3.8.2
   ```

   安装完成后将 Python 的本地版本切换到3.8.2：

   ```bash
   $ pyenv local 3.8.2
   ```

3. 使用 pip 安装 Virtualenv：

   ```bash
   $ pip install virtualenv
   ```

4. 使用 pip 安装 Pipenv：

   ```bash
   $ pip install pipenv
   ```

5. 使用 pip 安装 Django：

   ```bash
   $ pip install Django
   ```

6. 创建一个 Django 项目：

   ```bash
   $ django-admin startproject djangoproject
   ```

   上面命令中的 `djangoproject` 是项目名，可以改成你想起的名字。

7. 在刚刚创建的 Django 项目中初始化 Pipenv：

   ```bash
   $ cd djangoproject
   $ pipenv install Django
   ```

   上面的命令会创建一个与 `djangoproject` 相关联的 Virtualenv 实例并且在其中安装 Django，然后再生成 Pipfile 和 Pipfile.lock 文件记录项目的依赖包。命令执行完成后关闭并重新打开终端。

8. 启动刚刚创建的 Django 项目服务器：

   ```bash
   $ cd djangoproject
   $ pipenv run python manage.py runserver
   ```

   打开浏览器在地址栏中输入 `http://localhost:8000`，出现「The install worked successfully! Congratulations!」页面，说明项目创建并启动成功。

[Virtualenv]: https://virtualenv.pypa.io
[pip]: https://pip.pypa.io
[pyenv]: https://github.com/pyenv/pyenv
[Pipenv]: https://pipenv.pypa.io

## JavaScript 篇

JavaScript 是因为 Node.js 的兴起才开始逐渐出现了完善的部署工具。JavaScript 的部署工具受 Ruby 的影响较大，有对标 RVM 的 [nvm]、对标 rbenv 的 [nodenv]、对标 RubyGems 的 [npm]、对标 Bundler 的 [Yarn]。因为在 Ruby 篇我已经讲过了更喜欢 rbenv，所以我在 JavaScript 中就选择了 nodenv 作为版本管理器。

接下来我以创建一个 [Express.js] 项目为例来说明如何使用 nodenv、npm 和 Yarn。

1. 使用 Homebrew 安装 nodenv：

   ```bash
   $ brew install nodenv
   ```

   执行上面的命令后会同时安装 nodenv 的 [node-build] 插件。然后：

   ```bash
   $ nodenv init
   ```

   根据提示设置 nodenv 的 shell 集成，设置完成后关闭并重新打开终端。

2. 使用 nodenv 安装 Node.js：

   ```bash
   $ nodenv install --list
   ```

   查看有哪些可安装的 Node.js 版本，比如要安装 Node.js 12.16.2：

   ```bash
   $ nodenv install 12.16.2
   ```

   安装完成后将 Node.js 的本地版本切换到12.16.2：

   ```bash
   $ nodenv local 12.16.2
   ```

3. 使用 npm 安装 Yarn：

   ```bash
   $ npm install -g yarn
   ```

   关闭并重新打开终端。

   *（完成本步骤以后就具备了 Ruby on Rails 6.0.2.2 的安装脚本要求的 Node.js 基本运行环境。）*

4. 创建一个 Express.js 项目：

   ```bash
   $ mkdir expressjsproject
   $ cd expressjsproject
   $ yarn init
   ```

   上面命令中的 `expressjsproject` 是项目名，可以改成你想起的名字。执行完 `yarn init` 命令以后会提示输入一系列内容，比如程序名称、版本号、主文件名等，根据实际情况填写相关内容即可。因为我这里创建的只是一个演示项目，所以一路回车按照默认内容创建项目。

   然后在当前项目中安装 Express.js：

   ```bash
   $ yarn add express
   ```

5. 创建 Express.js 项目的 `hello, world`，在项目目录中创建一个名为 `index.js` 的文件，然后添加以下代码：

   ```bash
   var express = require('express');
   var app = express();

   app.get('/', function (req, res) {
       res.send('hello, world');
   });

   app.listen(3000, function () {
       console.log('Example app listening on port 3000!');
   });
   ```

6. 启动刚刚创建的 Express.js 项目服务器：

   ```bash
   $ node index.js
   ```

   打开浏览器在地址栏中输入 `http://localhost:3000`，出现「hello, world」页面，说明项目创建并启动成功。

[nvm]: https://github.com/nvm-sh/nvm
[nodenv]: https://github.com/nodenv/nodenv
[node-build]: https://github.com/nodenv/node-build
[npm]: https://www.npmjs.com
[Yarn]: https://yarnpkg.com
[Express.js]: https://expressjs.com

（全文完）
