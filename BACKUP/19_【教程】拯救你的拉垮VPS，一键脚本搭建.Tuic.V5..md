# [【教程】拯救你的拉垮VPS，一键脚本搭建 Tuic V5 ](https://github.com/jaydong2016/gitblog/issues/19)

> 我的 AWS 光帆使用其他协议，速度基本没法看，直到我安装了tuic v5
> 各位有垃圾VPS 的确实可以一试
> 
以下转载自 [最新Tuic V5性能提升及使用方法 - mack-a (v2ray-agent.com)](https://www.v2ray-agent.com/archives/1687167522196)

Tuic 最近发布了 **V5**，性能提升较大，经过了解和使用这篇文章应运而生。

QUIC 协议汲取了大量人们给 TCP 糊墙的经验教训，把连接结构优化到（目前来看）极致。但是现在市面上的代理工具还没有能完全利用 QUIC 特性的存在 - **官方介绍**。

如果本地使用 **hysteria** 经常发生 **QoS**，可以尝试一下此工具。相对于 hysteria 更加温和，在**不影响良好使用情况下尽量发挥最大的性能**。据群友测试，**可以提升数倍**，而且没有发现 QoS 问题，如果是**线路以及性能优良的 VPS 则提升不明显**，如果有 [**RackNerd**](https://www.v2ray-agent.com/archives/racknerdtao-can-zheng-li-nian-fu-10mei-yuan) 的可以尝试一下使用一下。

*   1-RTT TCP 中继
    
*   0-RTT UDP 中继，且 NAT 类型为 FullCone
    
*   在用户空间的拥塞控制，也就是说可以在任何系统平台实现双向的 BBR
    
*   两种 UDP 中继模式: native （原生 UDP 特性，数据仍被 TLS 加密）和 quic (100% 送达率，每个包单独单独作为一个 QUIC “流”，一个包的确认重传不会阻塞其它包)
    
*   完全多路复用，服务器和客户端之间始终只需要一条 QUIC 连接，所有任务作为这个连接中的 “流” 进行传输（一个流的暂时阻塞不会影响其它流），所以除连接第一个中继任务外的其它任务都不需要经过 QUIC 握手和 TUIC 的鉴权
    
*   网络切换时的会话平滑转移，例如在从 Wi-Fi 切换到移动数据时连接不会像 TCP 一样直接断开
    
*   0-RTT 、与中继任务并行的鉴权
    
*   支持 QUIC 的 0-RTT 握手（开启之后能达到 真・ 1 -RTT TCP 和 0-RTT UDP ，但是就算不开启，多路复用的特性也能保证在绝大多数情况下 1-RTT 和 0-RTT ）
    

1. 下载脚本
-------

```
wget -P /root -N --no-check-certificate "https://raw.githubusercontent.com/mack-a/v2ray-agent/master/install.sh" && chmod 700 /root/install.sh && /root/install.sh

```

2. 安装或者个性化安装
------------

*   只需要保证安装 VLESS_TLS_Vision 即可（需要依赖这个）
    

```
vasma->1/2

```

3. 安装 Tuic
----------

```
vasma->7

```

目前支持 Tuic V5 客户端较少，推荐以下两个

1.windows
---------

### 1.[v2rayN（需要 Pre-release 的最新版）](https://github.com/2dust/v2rayN/releases)

*   1. 下载最新的完成后其中默认带的 Tuic 内核**不支持 V5**，所以这里还需要手动下载 [Tuic-client 1.0.0](https://github.com/EAimTY/tuic/releases/tag/tuic-client-1.0.0) 进行替换（不要下载成 server 端了） , 下载文件名称一般为 **tuic-client-1.0.0-x86_64-pc-windows-msvc.exe。**
    
*   2. 下载完成后改名 **tuic-client.exe** 并替换原来的 **tuic-client.exe**，文件路径为 **v2rayN 程序目录 / bin/tuic/。**
    
*   3. 将脚本提供的 json 配置，复制并保存到本地，名字为 config.json。
    
*   4. 客户端配置：v2rayN-> 服务器 -> 自定义配置 -> 浏览 -> 导入刚才的 json 文件。Core 类型选择 tuic，Socks 端口输入 7798，点击确定进行保存。由于无法进行测速，只能设置为活跃节点后打开浏览器测试可用性。
    
    ![](https://www.v2ray-agent.com/upload/wk/v2rayN_tuic_01.png)
    
    ![](https://www.v2ray-agent.com/upload/wk/v2rayN_tuic_02.png)
    

### 2.[Clash for Windows](https://github.com/Fndroid/clash_for_windows_pkg/releases/tag/0.20.23)([Clash.Meta](https://github.com/MetaCubeX/Clash.Meta/releases/tag/Prerelease-Alpha))

*   1. 下载上方链接中的 Clash For Windows GUI。
    
*   2. 下载[**最新的 Alpha**](https://github.com/MetaCubeX/Clash.Meta/releases/tag/Prerelease-Alpha) 的 Clash.Meta，名称一般为 **clash.meta-windows-amd64-alpha-xxx.zip**。如果是 ARM 则是 **clash.meta-windows-arm64-alpha-xxx.zip** 下载完成后，解压并修改文件名字为【**clash-win64.exe**】
    
*   3. 将上面下载成功的内核替换到下面的路径。
    
    ```
    # windows 替换文件 clash-win64.exe
    # AMD
    cfw程序目录->resources/static/files/win/x64/
    # ARM
    cfw程序目录->resources/static/files/win/arm64/
    
    ```
    
*   4.**vasma->6. 账号管理 ->2. 查看订阅** 拉取即可
    

### 3.[Clash Verge](https://github.com/zzzgydi/clash-verge/releases)

*   1. 下载上方连接的 GUI，windows 一般为 **Clash.Verge_1.3.3_x64_zh-CN.msi**，Mac 则是 **Clash.Verge_1.3.3_x64.dmg**，Mac M1/M2 则是 **Clash.Verge_1.3.3_aarch64.dmg**
    

*   2.**vasma->6. 账号管理 ->2. 查看订阅** 拉取即可
    

![](https://www.v2ray-agent.com/upload/wk/clashVerge_%E8%AE%A2%E9%98%85.png)

*   3. 修改设置，第一步进入设置，打开局域网连接、Tun 模式、系统代理，第二步修改 Clash 内核为 Clash Meta，第三步重启应用
    

2.MacOS
-------

### 1.[Clash for Windows](https://github.com/Fndroid/clash_for_windows_pkg/releases/tag/0.20.23)([Clash.Meta](https://github.com/MetaCubeX/Clash.Meta/releases/tag/Prerelease-Alpha))

步骤参考上面的 windows 配置方法，与 windows 的区别是核心修改的名称不一样，Mac 的是 **clash-darwin**。一般下载的名称为 **clash.meta-darwin-amd64-alpha-xx.gz**，ARM 则是 **clash.meta-darwin-arm64-alpha-xx.gz，**替换路径如下

```
# macos intel
/Applications/Clash\ for\ Windows.app/Contents/Resources/static/files/darwin/x64/
# macosARM（M1、M2）
/Applications/Clash\ for\ Windows.app/Contents/Resources/static/files/darwin/arm64/

```

2.Clash Verge
-------------

*   参考上方设置