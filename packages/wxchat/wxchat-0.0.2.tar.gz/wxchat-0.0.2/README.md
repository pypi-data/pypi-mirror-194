# 快速开始
前置条件：
* 安装微信[3.6.0.18版本](https://115.com/s/sw6vkz733g3?password=d460)。

## 安装
因为需要编译c++文件，可能会比较慢，可以加上-v查看进度，这里使用清华镜像源下载依赖
```
> pip install . -v -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 使用
打开cmd命令行，启动微信服务端程序
```
> weixin_server.exe --port1 10086 --port2 10010
```

编写python代码，与微信服务端通信

```
from wechat import WechatHelper
helper = WechatHelper(127.0.0.1, 10086, 10010)

helper.wait_until_login()

helper.send_text("filehelper", "你好!")

@helper.message("chat")
def receive_message(topic, message):
    print(message)

helper.run_forever()

```

## 示例
TODO 
1. 接收消息
2. 发送消息
3. 查询好友
4. 添加好友
5. 获取群成员
6. 获取通讯录
7. 发送卡片
8. 发送文章
9. 自动收款
10. 自动入群
11. 自动同意好友请求
12. 发送小程序

# 声明
本项目仅为学习交流之用，如有问题请添加微信haiyiqiang
