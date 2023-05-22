---
title: 在 macOS 上安装 Oh My Zsh
date: 2022-01-29
categories: 计算机技术
tags:
    - 计算机技术
    - macOS
    - Zsh
    - Oh My Zsh
---

## 运行环境

- macOS Monterey 12.1
- macOS 终端 2.12
- [iTerm2](https://iterm2.com) 3.4.15
- [Zsh](https://www.zsh.org) 5.8
- [Git](https://git-scm.com) 2.23.0

<!-- more -->

## 安装步骤

1. 打开 macOS 终端，登录 Zsh，运行命令：

   ```bash
   sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
   ```

2. 安装 Powerline 字体，运行命令：

   ```bash
   git clone https://github.com/powerline/fonts.git --depth=1
   ```

   然后：

   ```bash
   ./fonts/install.sh
   ```

   然后：

   ```bash
   rm -rf fonts
   ```

3. 设置 macOS 终端，在 macOS 终端的「偏好设置」中找到「描述文件」选项，然后创建一个名为「Oh My Zsh」的描述文件。然后在文本选项下面将字体设置为「DejaVu Sans Mono for Powerline」，字体大小设置为12号字，然后选择适当的配色。具体情况可以参考下图设置：

   ![install-oh-my-zsh-on-macos_0001.png](/images/install-oh-my-zsh-on-macos_0001.png)

   然后将「Oh My Zsh」描述文件设置为默认，在 macOS 终端的「偏好设置」中找到「通用」选项，将「启动时，打开：」选项设置为「使用描述文件新建窗口：」，描述文件设置为「Oh My Zsh」：

   ![install-oh-my-zsh-on-macos_0002.png](/images/install-oh-my-zsh-on-macos_0002.png)

4. 设置 iTerm2，在 iTerm2 的「Preferences」中找到「Profiles」选项，然后基于「Default」创建一个名为「Oh My Zsh」的描述文件。选中「Default」后在创建描述文件的「+-」按钮右侧的菜单中选择「Duplicate Profile」：

   ![install-oh-my-zsh-on-macos_0003.png](/images/install-oh-my-zsh-on-macos_0003.png)

   然后在「General」选项中找到「Name」，将描述文件的名称改为「Oh My Zsh」：

   ![install-oh-my-zsh-on-macos_0004.png](/images/install-oh-my-zsh-on-macos_0004.png)

   然后在「Colors」选项中选择配色方案为「Solarized Dark」：

   ![install-oh-my-zsh-on-macos_0005.png](/images/install-oh-my-zsh-on-macos_0005.png)

   然后在「Text」选项中找到「Font」，将字体设置为「DejaVu Sans Mono for Powerline」，字体大小设置为12号字：

   ![install-oh-my-zsh-on-macos_0006.png](/images/install-oh-my-zsh-on-macos_0006.png)

   然后将「Oh My Zsh」描述文件设置为默认项，选中「Oh My Zsh」后在创建描述文件的「+-」按钮右侧的菜单里选择「Set as Default」：

   ![install-oh-my-zsh-on-macos_0007.png](/images/install-oh-my-zsh-on-macos_0007.png)

   然后「Oh My Zsh」描述文件的名称前面会多出一个五角星图标：

   ![install-oh-my-zsh-on-macos_0008.png](/images/install-oh-my-zsh-on-macos_0008.png)

5. 设置 Oh My Zsh 主题为 agnoster，打开 macOS 终端，登录 Zsh，运行命令：

   ```bash
   vi ~/.zshrc
   ```

   找到：

   ```
   ZSH_THEME="robbyrussell"
   ```

   修改成：

   ```
   ZSH_THEME="agnoster"
   ```

   然后运行 `:wq` 保存文件并退出 Vim。

6. 设置 Oh My Zsh 插件，和设置 Oh My Zsh 主题一样，需要在 macOS 终端下用 Vim 编辑 `.zshrc` 文件，找到 `plugins=` 开头的行，修改其内容类似下面这样：

   ```
   plugins=(
     emoji
     git
     jenv
     pyenv
     rbenv
   )
   ```

   这里启用了 `emoji`、`git`、`jenv`、`pyenv`、`rbenv` 这五个插件。pyenv 和 rbenv 原本需要在 `.zshrc` 文件中配置一些参数的，因为安装了 Oh My Zsh，所以这些配置参数需要放在 `.zprofile` 中。安装配置 pyenv 和 rbenv 不在本文讨论范围之内，这里就不赘述了。

7. 经过以上步骤的操作就完成了 Oh My Zsh 的安装工作，关闭并重新打开 macOS 终端后就会变成下面这样了：

   ![install-oh-my-zsh-on-macos_0009.png](/images/install-oh-my-zsh-on-macos_0009.png)

   在 iTerm2 下是这个样子的：

   ![install-oh-my-zsh-on-macos_0010.png](/images/install-oh-my-zsh-on-macos_0010.png)

（全文完）

## 参考链接

- <https://ohmyz.sh>
- <https://github.com/ohmyzsh/ohmyzsh>
- <https://github.com/agnoster/agnoster-zsh-theme>
- <https://github.com/powerline/fonts>
- <https://zh.wikipedia.org/wiki/DejaVu%E5%AD%97%E4%BD%93>
- <https://github.com/gnachman/iTerm2>
- <https://zhuanlan.zhihu.com/p/62419420>