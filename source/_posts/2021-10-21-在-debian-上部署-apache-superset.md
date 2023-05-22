---
title: 在 Debian 上部署 Apache Superset
date: 2021-10-21
categories: 计算机技术
tags:
    - Linux
    - Debian
    - Superset
---

我最近在研究 [Apache Superset]，今天就来说说如何在 [Debian] 上部署 Apache Superset。在开始前先交代下我的 Apache Superset 运行环境，我现在用的电脑是[苹果]的 [MacBook Air] \(13-inch, 2017\)，操作系统为 [macOS Big Sur] 11.5.2，在 [VirtualBox] 6.1.26 创建的虚拟机上安装的 [Debian Buster] 10.10.0，然后在 Debian Buster 10.10.0 上部署的 Apache Superset 1.3.1。具体的 Apache Superset 运行环境如下：

- [Debian Buster] 10.10.0
- [Git] 2.20.1
- [pyenv] 1.2.24
- [Python] 3.7.10
- [Virtualenv] 20.7.2
- [MariaDB] 10.3.29
- [Apache HTTP Server] 2.4.38
- [PHP] 7.3.29-1~deb10u1
- [phpMyAdmin] 5.1.1

好，我的 Apache Superset 运行环境交代完了，接下来进入正题。

[Apache Superset]: https://superset.apache.org
[Debian]: https://www.debian.org
[苹果]: https://www.apple.com.cn
[MacBook Air]: https://www.apple.com.cn/macbook-air/
[macOS Big Sur]: https://www.apple.com.cn/macos/big-sur/
[VirtualBox]: https://www.virtualbox.org
[Debian Buster]: https://www.debian.org/releases/buster/
[Git]: https://git-scm.com
[pyenv]: https://github.com/pyenv/pyenv
[Python]: https://www.python.org
[Virtualenv]: https://virtualenv.pypa.io/en/latest/
[MariaDB]: https://mariadb.org
[Apache HTTP Server]: http://httpd.apache.org
[PHP]: https://www.php.net
[phpMyAdmin]: https://www.phpmyadmin.net

<!-- more -->

## Debian 的相关设置

我是用 [netinst] 镜像文件安装的 Debian，在安装时我选了 `Debian 桌面环境`、`GNOME` 和 `标准系统工具` 这三个组件。其中安装 `Debian 桌面环境` 和 `GNOME` 是为了我在虚拟机中方便调试。如果是在生产环境中部署 Apache Superset 的话，最小化安装 Debian，只选中 `标准系统工具` 就可以了。

在安装 Debian 时创建的用户为：superset，没有 `sudo` 权限，需要手动授权：

1. 打开终端，登录 [bash]。
2. 运行 `su` 命令然后输入 root 密码。
3. 使用 Vim 编辑 `sudoers` 文件：

   ```bash
   sudo vi /etc/sudoers
   ```

4. 找到 `# User privilege specification`，在这部分追加 `superset	ALL=(ALL:ALL) ALL`：

   ```
   # User privilege specification
   root	ALL=(ALL:ALL) ALL
   superset	ALL=(ALL:ALL) ALL
   ```

5. 运行 `:wq!` 命令强制保存并退出。

[bash]: https://www.gnu.org/software/bash/
[netinst]: https://www.debian.org/distrib/netinst

## 部署 Python 运行环境

Apache Superset 是用 Python 开发的，所以要先部署 Python 运行环境。我选择用 pyenv 和 Virtualenv 部署 Python 运行环境。

### 安装 pyenv

1. 打开终端，登录 bash。
2. 部署 pyenv 在 Debian 上的构建环境：

   ```bash
   sudo apt update; sudo apt install make build-essential libssl-dev zlib1g-dev \
   libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
   libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
   ```

3. pyenv 在 Debian 上需要通过 Git 来安装，所以需要先安装 Git：

   ```bash
   sudo apt install git
   ```

4. 用 Git 将 pyenv 克隆到本地：

   ```bash
   git clone https://github.com/pyenv/pyenv.git ~/.pyenv
   ```

   如果网络连接超时，运行：

   ```bash
   git clone https://gitclone.com/github.com/pyenv/pyenv ~/.pyenv
   ```

5. 构建 pyenv：

   ```bash
   cd ~/.pyenv && src/configure && make -C src
   ```

6. 配置 pyenv 的 Shell 环境：

   ```bash
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
   echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
   echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
   echo 'eval "$(pyenv init -)"' >> ~/.bashrc
   ```

7. 重启终端，登录 bash。

### 安装 Python

接下来我们在 bash 上用 pyenv 安装 Python：

1. 打开终端，登录 bash。
2. 在安装 Python 前查看一下当前可安装的 Python 版本：

   ```bash
   pyenv install --list
   ```

3. 查看后我们选择安装 Python 3.7.10：

   ```bash
   pyenv install 3.7.10
   ```

4. 安装完成后查看下当前可用 Python 版本：

   ```bash
   pyenv versions
   ```

   会看到类似下面的信息：

   ```bash
   * system (set by /home/superset/.pyenv/version)
     3.7.10
   ```

   我们看到可用的 Python 版本有 `system` 和 `3.7.10`，当前使用的是 `system`（系统默认版本）。
   
5. 看下当前具体使用的是 Python 的哪个版本：

   ```bash
   python --version
   ```

   显示如下信息：

   ```bash
   Python 2.7.16
   ```

6. 将本地运行的 Python 版本切换到 `3.7.10`：

   ```bash
   pyenv local 3.7.10
   ```

   再用 `pyenv versions` 命令看下：

   ```bash
     system
   * 3.7.10 (set by /home/superset/.python-version)
   ```

   Python 的版本已经切换到 `3.7.10` 了，再用 `python --version` 命令验证下，显示：

   ```bash
   Python 3.7.10
   ```

### 安装 Virtualenv

1. 打开终端，登录 bash。
2. 升级 pip：

   ```bash
   pip install --upgrade pip
   ```

3. 安装 Virtualenv：

   ```bash
   pip install virtualenv==20.7.2
   ```

## 部署 MariaDB

Apache Superset 默认使用 [SQLite] 部署，但支持多种数据库管理系统部署。我们使用 MariaDB 部署。

[SQLite]: https://www.sqlite.org

### 安装 MariaDB

1. 打开终端，登录 bash。
2. 安装 MariaDB：

   ```bash
   sudo apt install mariadb-server mariadb-client
   ```

3. 按照提示操作完成后查看 MariaDB 服务运行状态：

   ```bash
   systemctl status mariadb
   ```

   如果显示类似下面信息：

   ```bash
   ● mariadb.service - MariaDB 10.3.29 database server
      Loaded: loaded (/lib/systemd/system/mariadb.service; enabled; vendor preset: enabled)
      Active: active (running) since Tue 2021-08-24 20:42:11 CST; 10min ago
        Docs: man:mysqld(8)
              https://mariadb.com/kb/en/library/systemd/
    Main PID: 2454 (mysqld)
      Status: "Taking your SQL requests now..."
       Tasks: 30 (limit: 4689)
      Memory: 72.3M
      CGroup: /system.slice/mariadb.service
              └─2454 /usr/sbin/mysqld
   ```

   说明 MariaDB 服务已经启动运行（查看后用 `:q` 命令返回 Shell）。

4. 一些其他的操作 MariaDB 服务的命令如下：

   - 启动 MariaDB 服务：`systemctl start mariadb`
   - 重启 MariaDB 服务：`systemctl restart mariadb`
   - 停止 MariaDB 服务：`systemctl stop mariadb`
   - 重新加载 MariaDB 服务配置：`systemctl reload mariadb`

### 增强 MariaDB 的安全性设置

MariaDB 的默认安装是不安全的。我们可以用 MariaDB 附带的 `mysql_secure_installation` 脚本来添加一些额外的安全性：

1. 打开终端，登录 bash。
2. 运行：`sudo mysql_secure_installation`，这里一定要输入 `sudo` 命令，否则在脚本运行过程中输入 root 密码的那个步骤无法通过。
3. 按照提示输入相关信息，在输入 root 密码的那个步骤直接按回车，然后设置新的 root 密码，其他出现带 `[Y/n]` 提示的步骤一律输入 `y`。
4. 修改 root 用户使用 `mysql_native_password` 插件登录：

   ```bash
   sudo mysql -u root
   ```

   进入 MariaDB Shell 后，切换当前数据库到 mysql：

   ```sql
   USE mysql;
   ```

   查看 root 用户使用哪个插件登录：

   ``sql
   SELECT User, Host, plugin FROM user;
   ```

   显示：

   ```
   +------+-----------+-------------+
   | User | Host      | plugin      |
   +------+-----------+-------------+
   | root | localhost | unix_socket |
   +------+-----------+-------------+
   ```

   这表示 root 用户正在使用 `unix_stocket` 插件登录。我们将 root 用户切换到使用 `mysql_native_password` 插件登录：

   ```sql
   UPDATE user SET plugin='mysql_native_password' WHERE User='root';
   ```

   然后：

   ```sql
   FLUSH PRIVILEGES;
   ```

   退出 MariaDB Shell：

   ```sql
   EXIT;
   ```

5. 重启 MariaDB 服务：`sudo systemctl restart mariadb`。

经过以上步骤操作，增强 MariaDB 的安全性设置就完成了。最终的 MariaDB 环境增强了以下安全性：

- 设置 root 用户的密码。
- 禁用 root 用户远程登录。
- 删除匿名用户帐户。
- 删除测试数据库默认情况下可以由匿名用户访问并重新加载权限。
- 设置 root 用户使用 `mysql_native_password` 插件登录，必须以 `mysql -u root -p` 方式登录。

## 部署 phpMyAdmin（可选项）

phpMyAdmin 是一个以 PHP 为基础，以 Web-Base 方式架构在网站主机上的 MySQL 的数据库管理工具，让管理者可用 Web 接口管理 MySQL 数据库。因为 MariaDB 和 MySQL 同源，所以 phpMyAdmin 也可以管理 MariaDB。部署 phpMyAdmin 主要是为了方便管理 MariaDB，与部署 Apache Superset 没有直接关系，所以本章节为可选项，可以直接跳过，继续阅读部署 Apache Superset 章节。

### 安装 Apache HTTP Server

1. 打开终端，登录 bash。
2. 安装 Apache HTTP Server：

   ```bash
   sudo apt install apache2
   ```

   按照提示操作完成后查看 Apache HTTP Server 服务运行状态：

   ```bash
   systemctl status apache2
   ```

   如果显示类似下面信息：

   ```bash
   ● apache2.service - The Apache HTTP Server
      Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset: enabled)
      Active: active (running) since Sun 2021-08-29 16:20:38 CST; 2min 59s ago
        Docs: https://httpd.apache.org/docs/2.4/
    Main PID: 2463 (apache2)
       Tasks: 55 (limit: 4689)
      Memory: 10.9M
      CGroup: /system.slice/apache2.service
              ├─2463 /usr/sbin/apache2 -k start
              ├─2465 /usr/sbin/apache2 -k start
              └─2466 /usr/sbin/apache2 -k start
   ```

   说明 Apache HTTP Server 服务已经启动运行（查看后用 `:q` 命令返回 Shell）。一些其他的操作 Apache HTTP Server 服务的命令如下：

   - 启动 Apache HTTP Server 服务：`systemctl start apache2`
   - 重启 Apache HTTP Server 服务：`systemctl restart apache2`
   - 停止 Apache HTTP Server 服务：`systemctl stop apache2`
   - 重新加载 Apache HTTP Server 服务配置：`systemctl reload apache2`

   接下来我们看下 Apache HTTP Server 工作是否正常。打开浏览器，如果访问 `http://localhost` 这个地址能够显示 Apache2 Debian Default Page，那么说明 Apache HTTP Server 工作正常。

### 安装 PHP

1. 打开终端，登录 bash。
2. 安装 PHP：

   ```bash
   sudo apt install php libapache2-mod-php php-mysql
   ```

   按照提示操作完成后重启 Apache HTTP Server 服务：

   ```bash
   systemctl restart apache2
   ```

3. 接下来测试 PHP 在 Apache HTTP Server 上工作是否正常。使用 Vim 创建 `phpinfo.php` 文件：

   ```bash
   sudo vi /var/www/html/phpinfo.php
   ```

   在文件中插入如下代码：

   ```php
   <?php phpinfo(); ?>
   ```

   保存退出后，打开浏览器，如果访问 `http://localhost/phpinfo.php` 这个地址能够显示 PHP 版本信息页面，那么说明 PHP 在 Apache HTTP Server 上工作正常。由于刚才创建的 `phpinfo.php` 文件会暴露 PHP 的敏感信息，这样会降低安全性，所以在测试后要删除这个文件：

   ```bash
   sudo rm /var/www/html/phpinfo.php
   ```

4. 安装 phpMyAdmin 相关依赖。phpMyAdmin 需要如下 PHP 扩展模块支持：

   - `php-mbstring`：用于管理非 ASCII 字符串，将字符串转换为不同编码的 PHP 扩展模块。
   - `php-gettext`：实现了NLS(Native Language Support) API 国际化支持的 PHP 扩展模块。
   - `php-zip`：支持将 `.zip` 文件上传到 phpMyAdmin 的 PHP 扩展模块。
   - `php-gd`：支持 GD 图形库的 PHP 扩展模块。

   接下来我们开始安装这些依赖：

   ```bash
   sudo apt install php-mbstring php-gettext php-zip php-gd
   ```

   按照提示操作完成后需要显示启用 `php-mbstring`：

   ```bash
   sudo phpenmod mbstring
   ```

   然后重启 Apache HTTP Server 服务：

   ```bash
   systemctl restart apache2
   ```

### 从源代码安装 phpMyAdmin

由于目前 Debaian Buster 10.10.0 的默认 APT 源不提供 phpMyAdmin，所以需要从源代码安装 phpMyAdmin。

1. 打开浏览器，访问 phpMyAdmin 下载页面，找到最新稳定版本下载链接的列表，然后复制以 tar.gz 结尾的下载链接。 目前 phpMyAdmin 的最新稳定版本为 5.1.1，复制 `phpMyAdmin-5.1.1-all-languages.tar.gz` 的下载链接。
2. 打开终端，登录 bash。
3. 用 `wget` 命令下载：

   ```bash
   wget -P ~/downloads/ https://files.phpmyadmin.net/phpMyAdmin/5.1.1/phpMyAdmin-5.1.1-all-languages.tar.gz
   ```

4. 下载完成后解压缩 `phpMyAdmin-5.1.1-all-languages.tar.gz`：

   ```bash
   tar -zxvf ~/downloads/phpMyAdmin-5.1.1-all-languages.tar.gz -C ~/downloads/
   ```

   这将会创建 `~/downloads/phpMyAdmin-5.1.1-all-languages/` 目录并将 `phpMyAdmin-5.1.1-all-languages.tar.gz` 中的文件全部解压缩到这里。

5. 将解压缩后得到的目录及文件移动到 `/usr/share/` 目录并且重命名为 `phpmyadmin`，这是 phpMyAdmin 默认希望查找其配置文件的位置：

   ```bash
   sudo mv ~/downloads//phpMyAdmin-5.1.1-all-languages/ /usr/share/phpmyadmin/
   ```

6. 创建一个 phpMyAdmin 存储临时文件的目录：

   ```bash
   sudo mkdir -p /var/lib/phpmyadmin/tmp/
   ```

   然后修改 `/var/lib/phpmyadmin/` 目录的所有者及用户组为 `www-data`（这是 Debian 上 Apache HTTP Server 默认配置的用户和组）：

   ```bash
   sudo chown -R www-data:www-data /var/lib/phpmyadmin
   ```

7. 用 phpMyAdmin 附带的示例配置文件 `config.sample.inc.php` 复制一个副本，命名为 `config.inc.php`，将其作为正式的配置文件：

   ```bash
   cp /usr/share/phpmyadmin/config.sample.inc.php /usr/share/phpmyadmin/config.inc.php
   ```

8. 安装 `pwgen`：

   ```bash
   sudo apt install pwgen
   ```

   然后用 `pwgen` 生成一个32位密钥：

   ```bash
   pwgen -s 32 1
   ```

   这将会生成一个类似下面这样的32位密钥：

   ```bash
   wHPV5cCVkfRE7kQygmaPx5mr0gVAKftW
   ```

9. 用 Vim 编辑 `config.inc.php`：

   ```bash
   vi /usr/share/phpmyadmin/config.inc.php
   ```

   找到 `$cfg['blowfish_secret']` 开头的行，在等号后面的单引号中插入刚才生成的32位密钥，改成像下面这样：

   ```php
   ...
   $cfg['blowfish_secret'] = 'wHPV5cCVkfRE7kQygmaPx5mr0gVAKftW'; /* YOU MUST FILL IN THIS FOR COOKIE AUTH! */
   ...
   ```

   然后找到另一个以注释 `/* User used to manipulate with storage */` 开头的部分，这里包含一些定义名为 pma 的 MariaDB 数据库用户的指令，该用户在 phpMyAdmin 中执行某些管理任务。 根据官方文档，在只有一个用户访问 phpMyAdmin 的情况下，不需要此特殊用户账户，但建议在多用户方案中使用。

   通过删除前面的斜杠取消注释 `controluser` 和 `controlpass` 指令。 然后更新 `controlpass` 指令以指向您选择的安全密码。 如果不这样做，默认密码将保留在原位，未知用户可以通过 phpMyAdmin 界面轻松访问您的数据库。

   进行这些更改后，文件的此部分像下面这样：

   ```php
   ...
   /* User used to manipulate with storage */
   // $cfg['Servers'][$i]['controlhost'] = '';
   // $cfg['Servers'][$i]['controlport'] = '';
   $cfg['Servers'][$i]['controluser'] = 'pma';
   $cfg['Servers'][$i]['controlpass'] = 'pmapass';
   ...
   ```

   （注：需要将 `pmapass` 设置成自己的密码。）

   然后找到另一个以注释 `/* Storage database and tables */` 开头的部分，这里包含许多定义 phpMyAdmin 配置存储的指令，去掉这个部分所有行前面的注释，改成像下面这样：

   ```php
   ...
   /* Storage database and tables */
   $cfg['Servers'][$i]['pmadb'] = 'phpmyadmin';
   $cfg['Servers'][$i]['bookmarktable'] = 'pma__bookmark';
   $cfg['Servers'][$i]['relation'] = 'pma__relation';
   $cfg['Servers'][$i]['table_info'] = 'pma__table_info';
   $cfg['Servers'][$i]['table_coords'] = 'pma__table_coords';
   $cfg['Servers'][$i]['pdf_pages'] = 'pma__pdf_pages';
   $cfg['Servers'][$i]['column_info'] = 'pma__column_info';
   $cfg['Servers'][$i]['history'] = 'pma__history';
   $cfg['Servers'][$i]['table_uiprefs'] = 'pma__table_uiprefs';
   $cfg['Servers'][$i]['tracking'] = 'pma__tracking';
   $cfg['Servers'][$i]['userconfig'] = 'pma__userconfig';
   $cfg['Servers'][$i]['recent'] = 'pma__recent';
   $cfg['Servers'][$i]['favorite'] = 'pma__favorite';
   $cfg['Servers'][$i]['users'] = 'pma__users';
   $cfg['Servers'][$i]['usergroups'] = 'pma__usergroups';
   $cfg['Servers'][$i]['navigationhiding'] = 'pma__navigationhiding';
   $cfg['Servers'][$i]['savedsearches'] = 'pma__savedsearches';
   $cfg['Servers'][$i]['central_columns'] = 'pma__central_columns';
   $cfg['Servers'][$i]['designer_settings'] = 'pma__designer_settings';
   $cfg['Servers'][$i]['export_templates'] = 'pma__export_templates';
   ...
   ```

   然后在文件的底部插入：

   ```php
   ...
   $cfg['TempDir'] = '/var/lib/phpmyadmin/tmp';
   ```

   然后运行 `:wq` 命令保存退出。

10. 用 phpMyAdmin 附带的 `create_tables.sql` 文件创建存储数据库和表：

    ```bash
    sudo mysql -u root -p < /usr/share/phpmyadmin/sql/create_tables.sql
    ```

11. 创建 pma 用户。首先登录 MariaDB Shell：

    ```bash
    sudo mysql -u -root -p
    ```

    然后执行：

    ```sql
    GRANT SELECT, INSERT, UPDATE, DELETE ON phpmyadmin.* TO 'pma'@'localhost' IDENTIFIED BY 'pmapass';
    ```

    （注：需要将 `pmapass` 改成 `config.inc.php` 文件中定义的密码。）

    然后运行 `EXIT;` 命令退出 MariaDB Shell。

12. 配置 Apache HTTP Server 服务。在 `/etc/apache2/conf-available/` 目录中创建一个名为 `phpmyadmin.conf` 的文件：

    ```bash
    sudo vi /etc/apache2/conf-available/phpmyadmin.conf
    ```

    然后将以下内容添加到该文件中：

    ```
    # phpMyAdmin default Apache configuration
    
    Alias /phpmyadmin /usr/share/phpmyadmin
    
    <Directory /usr/share/phpmyadmin>
        Options SymLinksIfOwnerMatch
        DirectoryIndex index.php
    
        <IfModule mod_php5.c>
            <IfModule mod_mime.c>
                AddType application/x-httpd-php .php
            </IfModule>
            <FilesMatch ".+\.php$">
                SetHandler application/x-httpd-php
            </FilesMatch>
    
            php_value include_path .
            php_admin_value upload_tmp_dir /var/lib/phpmyadmin/tmp
            php_admin_value open_basedir /usr/share/phpmyadmin/:/etc/phpmyadmin/:/var/lib/phpmyadmin/:/usr/share/php/php-gettext/:/usr/share/php/php-php-gettext/:/usr/share/javascript/:/usr/share/php/tcpdf/:/usr/share/doc/phpmyadmin/:/usr/share/php/phpseclib/
            php_admin_value mbstring.func_overload 0
        </IfModule>
        <IfModule mod_php.c>
            <IfModule mod_mime.c>
                AddType application/x-httpd-php .php
            </IfModule>
            <FilesMatch ".+\.php$">
                SetHandler application/x-httpd-php
            </FilesMatch>
    
            php_value include_path .
            php_admin_value upload_tmp_dir /var/lib/phpmyadmin/tmp
            php_admin_value open_basedir /usr/share/phpmyadmin/:/etc/phpmyadmin/:/var/lib/phpmyadmin/:/usr/share/php/php-gettext/:/usr/share/php/php-php-gettext/:/usr/share/javascript/:/usr/share/php/tcpdf/:/usr/share/doc/phpmyadmin/:/usr/share/php/phpseclib/
            php_admin_value mbstring.func_overload 0
        </IfModule>
    
    </Directory>
    
    # Authorize for setup
    <Directory /usr/share/phpmyadmin/setup>
        <IfModule mod_authz_core.c>
            <IfModule mod_authn_file.c>
                AuthType Basic
                AuthName "phpMyAdmin Setup"
                AuthUserFile /etc/phpmyadmin/htpasswd.setup
            </IfModule>
            Require valid-user
        </IfModule>
    </Directory>
    
    # Disallow web access to directories that don't need it
    <Directory /usr/share/phpmyadmin/templates>
        Require all denied
    </Directory>
    <Directory /usr/share/phpmyadmin/libraries>
        Require all denied
    </Directory>
    <Directory /usr/share/phpmyadmin/setup/lib>
        Require all denied
    </Directory>
    ```

    运行 `:wq` 命令保存退出。然后运行：

    ```bash
    sudo a2enconf phpmyadmin.conf
    ```

    然后重新加载 Apache HTTP Server 服务：

    ```bash
    sudo systemctl reload apache2
    ```

13. 打开浏览器，访问 `http://localhost/phpmyadmin` 这个地址，如果能够在显示的 phpMyAdmin 登录页面以 root 用户身份登录，那么说明 phpMyAdmin 工作正常。

## 部署 Apache Superset

经过一番折腾，我们终于可以进入主题了。下面我们开始部署 Apache Superset。

### 创建 Python 虚拟环境

为了防止 Python 的全局配置混乱，我们用 Virtualenv 为 Apache Superset 创建一个虚拟环境。

1. 打开终端，登录 bash。
2. 创建 `superset` 目录：

   ```bash
   mkdir ~/superset/
   ```

3. 进入 `superset` 目录：

   ```bash
   cd ~/superset/
   ```

   然后创建 Python 虚拟环境：

   ```bash
   virtualenv venv
   ```

4. 激活 Python 虚拟环境运行：

   ```bash
   source ./venv/bin/activate
   ```

   退出 Python 虚拟环境运行：

   ```bash
   deactivate
   ```

### 安装 Apache Superset

1. 打开终端，登录 bash。
2. 安装 Apache Superset 依赖包：

   ```bash
   sudo apt install build-essential libssl-dev libffi-dev \
   python-dev python3-dev python-pip python3-pip libsasl2-dev libldap2-dev
   ```

3. 进入 `~/superset/` 目录，激活 Python 虚拟环境。
4. 升级 pip：

   ```bash
   pip install --upgrade pip
   ```

5. 安装 Apache Superset：

   ```bash
   pip install apache-superset==1.3.1
   ```

6. 创建 MariaDB 数据库和用户。登录 MariaDB Shell：

   ```bash
   mysql -u root -p
   ```

   登录后创建 `superset` 数据库：

   ```sql
   CREATE DATABASE superset;
   ```

   然后创建 `superset` 用户：

   ```sql
   CREATE USER superset@'%' IDENTIFIED BY 'password';
   ```

   （注：`password` 需要改成自己设置的密码。）

   然后给 `superset` 用户赋予相应权限：

   ```sql
   GRANT ALL ON superset.* TO superset@'%' IDENTIFIED BY 'passowrd' WITH GRANT OPTION;
   FLUSH PRIVILEGES;
   ```

   （注：`password` 需要改成自己设置的密码。）

   然后退出 MariaDB Shell：

   ```sql
   EXIT;
   ```

7. 安装 `pwgen`：

   ```bash
   sudo apt install pwgen
   ```

   然后用 `pwgen` 生成一个32位密钥：

   ```bash
   pwgen -s 32 1
   ```

   这将会生成一个类似下面这样的32位密钥：

   ```bash
   e367ZPcOBwo0U2xRcFY36GqmFgsIomqw
   ```

8. 创建 Apache Superset 配置文件：

   ```bash
   vi ~/superset/superset_config.py
   ```

   然后插入如下内容：

   ```python
   # Superset specific config
   ROW_LIMIT = 5000

   SUPERSET_WEBSERVER_PORT = 8088

   # Flask App Builder configuration
   # Your App secret key
   SECRET_KEY = 'e367ZPcOBwo0U2xRcFY36GqmFgsIomqw'

   # The SQLAlchemy connection string to your database backend
   # This connection defines the path to the database that stores your
   # superset metadata (slices, connections, tables, dashboards, ...).
   # Note that the connection information to connect to the datasources
   # you want to explore are managed directly in the web UI
   SQLALCHEMY_DATABASE_URI = 'mysql://superset:password@localhost:3306/superset'

   # Flask-WTF flag for CSRF
   WTF_CSRF_ENABLED = True
   # Add endpoints that need to be exempt from CSRF protection
   WTF_CSRF_EXEMPT_LIST = []
   # A CSRF token that expires in 1 year
   WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365

   # Set this API key to enable Mapbox visualizations
   MAPBOX_API_KEY = ''

   # ---------------------------------------------------
   # Babel config for translations
   # ---------------------------------------------------
   # Setup default language
   BABEL_DEFAULT_LOCALE = "zh"

   CACHE_NO_NULL_WARNING = True
   ```

   （注：上面内容中 `SECRET_KEY` 的值是刚才生成的32位密钥，`SQLALCHEMY_DATABASE_URI` 的 `password` 需要改成自己设置的密码。）

   然后运行 `:wq` 命令保存并退出。

9. 设置环境变量，在 PYTHONPATH 中添加 `superset_config.py` 所在目录：

    ```bash
    echo 'export PYTHONPATH="$PYTHONPATH:/home/superset/superset"' >> ~/.bashrc
    ```

10. 重启终端，登录 bash，进入 `~/superset/` 目录，激活 Python 虚拟环境。

11. 安装 Python 的 MariaDB 数据库连接驱动 mysqlclient。首先需要安装 mysqlclient 的依赖包：

    ```bash
    sudo apt install libmariadb-dev libssl-dev libcrypto++-dev
    ```

    然后安装 mysqlclient：

    ```bash
    pip install mysqlclient==2.0.3
    ```

12. 初始化 Apache Superset 数据库：

    ```bash
    superset db upgrade
    ```

13. 创建 Apache Superset 管理员账号：

    ```bash
    superset fab create-admin
    ```

    命令运行后会提示输入以下信息：

    ```bash
    Username [admin]:
    User first name [admin]:
    User last name [user]:
    Email [admin@fab.org]:
    Password:
    Repeat for confirmation:
    ```

    对应输入的内容解释如下：

    ```bash
    Username [admin]: 用户名，如果不输入直接按回车，默认用户名为：admin。
    User first name [admin]: 名字，如果不输入直接按回车，默认名称为：admin。
    User last name [user]: 姓氏，如果不输入直接按回车，默认姓氏为：user。
    Email [admin@fab.org]: 邮箱，如果不输入直接按回车，默认邮箱为：admin@fab.org
    Password: 密码，不能为空，必须输入。
    Repeat for confirmation: 确认密码，要和前面输入的密码一致，不能为空。
    ```

14. 初始化 Apache Superset，创建默认角色和权限：

    ```bash
    superset init
    ```

15. 配置 Apache Superset 的 systemd 服务。创建 `superset.service`：

    ```bash
    sudo vi /etc/systemd/system/superset.service
    ```

    然后插入如下内容：

    ```
    [Unit]
    Description=Apache Superset
    After=network.target

    [Service]
    # 设置环境变量，在 PYTHONPATH 中添加 superset_config.py 所在目录。
    Environment=PYTHONPATH=$PYTHONPATH:/home/superset/superset

    # 设置 Apache Superset 的工作目录。
    WorkingDirectory=/home/superset/superset

    # gunicorn 命令的路径在激活 superset 的 Python 虚拟环境后通过 which gunicorn 命令获取。
    # gunicorn 命令的 -w 参数值按 2 * CPU 核心数量 + 1 设置。
    ExecStart=/home/superset/superset/venv/bin/gunicorn -w 5 -k gevent -b 0.0.0.0:8000 --access-logfile=success.log --error-logfile=error.log "superset.app:create_app()"

    Restart=on-failure
    RestartSec=30s

    [Install]
    WantedBy=multi-user.target
    ```

    运行 `:wq` 命令保存退出。然后加载 systemd 服务配置：

    ```bash
    sudo systemctl daemon-reload
    ```

    然后启动 `superset.service`：

    ```bash
    sudo systemctl start superset.service
    ```

    然后将 `superset.service` 设置为开机启动：

    ```bash
    sudo systemctl enable superset.service
    ```

16. 打开浏览器，访问 `http://localhost:8000` 这个地址，如果能够在显示的 Apache Superset 登录页面以 admin 用户身份登录，那么说明 Apache Superset 工作正常。

## Apache Superset 多实例部署

如果需要在同一主机上部署多个 Apache Superset 实例，那么需要重复完成前面的部署步骤。部署新的 Apache Superset 实例时需要注意以下事项：

1. 需要创建不同的 MariaDB 数据库及用户名、Apache Superset 工作目录、Python 虚拟环境进行部署。
2. 需要创建新的 `superset_config.py` 文件，并在其中设置新的数据库连接参数。
3. 在部署 Apache Superset 新实例的过程中，可以在 `.bashrc` 中将 `PYTHONPATH` 指向新实例的工作目录，然后再创建一个新的 systemd 服务配置文件，比如 `superset-0002.service`，在其中更改如下设置：

   - 将 `Environment` 参数中的 `PYTHONPATH` 指向新实例的工作目录。
   - 将 `WorkingDirectory` 参数指向新实例的工作目录。
   - 将 `ExecStart` 参数中的 `gunicorn` 命令的 `-b` 参数指向新的网络端口。

4. 当所有的 Apache Superset 实例都部署完成后，可以删除 `.bashrc` 中的 `PYTHONPATH` 设置，只保留各个实例的 systemd 服务配置中的 `PYTHONPATH` 设置就行。

## 总结

通过完成以上步骤的部署，我们完成了一个 Apache Superset 在 Debian 上的准生产环境部署，并且根据需要可以实现在同一主机上部署多个 Apache Superset 实例。部署过程主要是通过运行 Shell 命令的方式实现，大多数 Shell 命令都可以通过 `--help` 参数查看帮助信息。在部署过程中遇到问题，还可以根据报错信息在网上搜索解决办法。另外，熟悉 Shell 命令的相关知识肯定会事半功倍。

（全文完）

## 参考链接

- <https://blog.csdn.net/lincyang/article/details/21020295>
- <https://github.com/pyenv/pyenv>
- <https://github.com/pyenv/pyenv/wiki#suggested-build-environment>
- <https://git-scm.com/download/linux>
- <https://git-scm.com/docs>
- <https://virtualenv.pypa.io/en/latest/>
- <https://www.howtoing.com/install-mariadb-database-in-debian-10>
- <https://www.iizyx.com/62/>
- <https://www.huaweicloud.com/articles/12654923.html>
- <https://www.cnblogs.com/acmexyz/p/12350151.html>
- <https://zh.wikipedia.org/wiki/PhpMyAdmin>
- <https://www.howtoing.com/how-to-install-and-secure-phpmyadmin-on-debian-9>
- <https://www.howtoing.com/how-to-install-phpmyadmin-from-source-debian-10>
- <https://www.php.net/manual/zh/intro.gettext.php>
- <https://ipcmen.com/wget>
- <https://einverne.github.io/post/2016/09/tar-archive-and-extract.html>
- <https://superset.apache.org/docs/installation/installing-superset-from-scratch>
- <https://superset.apache.org/docs/installation/configuring-superset>
- <https://blog.csdn.net/wenqiang1208/article/details/105520549>
- <https://juejin.cn/post/6844903850713825287>
- <http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html>
- <http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-part-two.html>
- <https://gist.github.com/romankierzkowski/c54c83496b3267362cc805477c4e409f>
