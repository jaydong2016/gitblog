# [Nginx 可视化管理界面](https://github.com/jaydong2016/gitblog/issues/16)

> 今天给大家介绍一款 Nginx 可视化管理界面，非常好用，小白也能立马上手。

![](http://pic9.adone.eu.org/modb_20230329_01597a5a-cdd7-11ed-a521-38f9d3cd240d.png)



今天给大家介绍一款 Nginx 可视化管理界面，非常好用，小白也能立马上手。

nginx-proxy-manager 是一个反向代理管理系统，它基于 NGINX，具有漂亮干净的 Web UI。还可以获得受信任的 SSL 证书，并通过单独的配置、自定义和入侵保护来管理多个代理。它是开源的，斩获 11.8K 的 Star 数。

特征
--

*   基于 Tabler(https://tabler.github.io/) 的美观安全的管理界面

*   无需了解 Nginx 即可轻松创建转发域、重定向、流和 404 主机

*   使用 Let's Encrypt 的免费 SSL 或提供您自己的自定义 SSL 证书

*   主机的访问列表和基本 HTTP 身份验证

*   高级 Nginx 配置可供超级用户使用

*   用户管理、权限和审核日志

安装
--

### 1、安装 Docker 和 Docker-Compose

### 2、创建一个 docker-compose.yml 文件

```
version: '3'
services:
  app:
    image: 'jc21/nginx-proxy-manager:latest'
    restart: unless-stopped
    ports:
      - '80:80'
      - '81:81'
      - '443:443'
    volumes:
      - ./data:/data
      - ./letsencrypt:/etc/letsencrypt


```

### 3、运行

```
docker-compose up -d

#如果使用的是 docker-compose-plugin
docker compose up -d

```

### 4、访问网页

运行成功后，访问 http://127.0.0.1:81/ 就能看到界面啦

![](http://pic9.adone.eu.org/modb_20230329_01674f18-cdd7-11ed-a521-38f9d3cd240d.png)

### 5、登录

网站默认账号和密码为

```
账号：admin@example.com
密码：changeme


```

登录成功后第一次要求修改密码，按照步骤修改即可！

### 6、登录成功主界面

![](http://pic9.adone.eu.org/modb_20230329_01835f46-cdd7-11ed-a521-38f9d3cd240d.png)

实战：设置后台管理界面的反向代理
----------------

这里，我们就用 http://a.test.com/ 来绑定我们的端口号为 81 的后台管理界面，实现浏览器输入 http://a.test.com/ 即可访问后台管理界面，并且设置 HTTPS。

### 1、前提

*   安装好 Nginx Proxy Manager

*   拥有一个域名

*   将 http://a.test.com/ 解析到安装 Nginx Proxy Manager 的服务器 ip 地址上

### 2、反向代理操作

先用`ip:81`  
 访问后台管理界面，然后输入账号密码进入后台。

点击绿色图标的选项

![](http://pic9.adone.eu.org/modb_20230329_0176ed88-cdd7-11ed-a521-38f9d3cd240d.png)

点击右边`Add Proxy Host`  
 ，在弹出的界面`Details`  
选项中填写相应的字段。

![](http://pic9.adone.eu.org/modb_20230329_01918620-cdd7-11ed-a521-38f9d3cd240d.png)

*   **Domain Names**: 填写要反向代理的域名，这里就是 http://a.test.com/

*   **Forward Hostname / IP**: 填写的 ip 值见下文解释

*   **Forward Port**: 反向代理的端口，这里就是 81

*   **Block Common Exploits**: 开启后阻止一些常见漏洞

*   其余两个暂不知作用

**Forward Hostname / IP 填写说明**

如果搭建的服务和 nginx proxy manager 服务所在不是一个服务器，则填写能访问对应服务的 IP。如果都在同一台服务器上，则填写在服务器中输入`ip addr show docker0`  
 命令获取得到的 ip。

![](http://pic9.adone.eu.org/modb_20230329_01a1ce36-cdd7-11ed-a521-38f9d3cd240d.png)

这里不填`127.0.0.1`  
的原因是使用的是 docker 容器搭建 web 应用，docker 容器和宿主机即服务器不在同一个网络下，所以`127.0.0.1`  
并不能访问到宿主机，而`ip addr show docker0`  
获得的 ip 地址就是宿主机地址。

![](http://pic9.adone.eu.org/modb_20230329_01b10bf8-cdd7-11ed-a521-38f9d3cd240d.png)

接下来即可用`a.test.com`  
 访问后台管理界面，此时还只是 http 协议，没有 https。不过此时就可以把之前的 81 端口关闭了，输入`a.test.com`  
 访问的是服务器`80`  
端口，然后在转发给内部的 81 端口。

### 3、申请 ssl 证书

申请一个`a.test.com`  
 证书，这样就可以提供 https 访问了。

在 Nginx Proxy Manager 管理后台，选择`Access Lists`  
->`Add SSL Certificate`  
->`Let's Encrypt`  
选项。

![](http://pic9.adone.eu.org/modb_20230329_01bfc6fc-cdd7-11ed-a521-38f9d3cd240d.png)

按照下图方式填写，点击 Save 就可以了

![](http://pic9.adone.eu.org/modb_20230329_01ccf318-cdd7-11ed-a521-38f9d3cd240d.png)

### 4、设置 HTTPS

进入反向代理设置界面，编辑上文创建的反代服务，选择 SSL 选项，下拉菜单中选择我们申请的证书，然后可以勾选`Force SSL`  
即强制 HTTPS。

![](http://pic9.adone.eu.org/modb_20230329_01dc94a8-cdd7-11ed-a521-38f9d3cd240d.png)

总结
--

以上就是本教程的全部内容，更多的使用教程，大家可以访问官方文档。

> 官方文档：https://nginxproxymanager.com/guide/