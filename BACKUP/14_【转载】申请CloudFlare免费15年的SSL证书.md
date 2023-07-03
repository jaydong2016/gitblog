# [【转载】申请CloudFlare免费15年的SSL证书](https://github.com/jaydong2016/gitblog/issues/14)

> 原文地址 vpsyx.com

> 前言 现在大家用的最多的免费证书，可能就是 Let,s encrytp 了吧，但是它有一个缺点，就是有效期太短了，最多只有 90 天，每次都要想着证书是不是快要到期了，是不 不是该查看一下了，这样就有个牵挂了，......

## **前言**

现在大家用的最多的免费证书，可能就是 Let,s encrytp 了吧，但是它有一个缺点，就是有效期太短了，最多只有 90 天，每次都要想着证书是不是快要到期了，是不

不是该查看一下了，这样就有个牵挂了，要做到一个短期没牵挂的方法，那就是来个长期有效的证书

那么就有了这个选择——15 年有效期的免费证书

![https://s2.loli.net/2023/06/30/pGN6VlH5jPsDXWc.png](https://s2.loli.net/2023/06/30/pGN6VlH5jPsDXWc.png)

这个[[域名](https://vpsyx.com/domain/)](https://vpsyx.com/domain/)我已经申请到了，到期日期——2037 年 7 月 23 日

注意

### **缺点一**

这个证书也有一个致命缺点，就是只能配合它家的 CDN，小云朵使用，即要打开代理状态

![https://s2.loli.net/2023/06/30/lzNSRO4jKanLgwf.png](https://s2.loli.net/2023/06/30/lzNSRO4jKanLgwf.png)

不然就是还是否会提示 “Win 没有足够信息，不能验证该证书”

![https://s2.loli.net/2023/06/30/l8nmM2PLDhHOI6A.png](https://s2.loli.net/2023/06/30/l8nmM2PLDhHOI6A.png)

这就是关了小云朵后的提示

### **缺点二**

即使申请的证书是 15 年，也是内部有效时间，对外，即客户层面看到的证书，还是 cloudflare 帮我们自动申请的，Let,s encrypt 的 E1 证书

![https://s2.loli.net/2023/06/30/mrhFRg3ekHNIa14.png](https://s2.loli.net/2023/06/30/mrhFRg3ekHNIa14.png)

不过这个不用我们自己再申请了，还是会一劳永逸的方法

如果能接受上面的两缺点，那我们才开始操作吧，如果接受不了，就放弃吧

## **申请过程**

第一步：登录 cloudflare——SSL/TLS—— 概述——完全（严格）

![https://s2.loli.net/2023/06/30/7J19Z8jgpnqbVUS.png](https://s2.loli.net/2023/06/30/7J19Z8jgpnqbVUS.png)

第二步：SSL/TLS——源服务器——创建证书

![https://s2.loli.net/2023/06/30/k2XwxmPhEIWU9Bz.png](https://s2.loli.net/2023/06/30/k2XwxmPhEIWU9Bz.png)

第三步：选择使用 cloudflare 生成私钥和 CSR，类型默认 RAS（2048）就可以了，创建

![https://s2.loli.net/2023/06/30/dsqeDxtA5FOU2y7.png](https://s2.loli.net/2023/06/30/dsqeDxtA5FOU2y7.png)

第四步：复制 pem 和 key，自行保存，这里的 key 只出现一次，**切记复制保存，切记复制保存，切记复制保存（重要）**

![https://s2.loli.net/2023/06/30/oiP1uSJzLC8a4Xs.png](https://s2.loli.net/2023/06/30/oiP1uSJzLC8a4Xs.png)

第五步：解析域名并开启代理小云朵，大功告成

## **总结**

优点是 15 年，不需要自己为证书牵挂，缺点就是要依赖小云朵的 CDN，要保持一一对应关系

我们个人申请的 Let's encrypt 是 R3 级别的，cloudflare 帮我们申请的是 E1 级别的，有什么区别也不是很清楚，只知道是不一样的

区别如官方图示

![https://s2.loli.net/2023/06/30/mT7CdHbS5pElxar.png](https://s2.loli.net/2023/06/30/mT7CdHbS5pElxar.png)