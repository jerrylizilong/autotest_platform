# update : 2018-09-19
- 新增执行完成后发送邮件
- 需要在 app/config.py 中对应部分打开开关并配置对应账号信息

# update : 2018-09-14
- 优化步骤出错处理：  使用了 retrying 模块。  需要新安装该模块：  pip install retrying
- 部分步骤进行了调整，建议重新初始化  keywords 表的数据。
- 调整了打印内容


# update ： 2018-08-28
- 新增测试用例步骤生成器
- 修改页面：新增、编辑用例

# update ： 2018-08-24
- 新增android 设备使用 ATX 进行测试：
- 修改：
-- app/config.py 文件新增 ATXHost 配置，需要将 atx server 的地址配置到该项中

### 前提： 已安装 atx server进行设备管理
### 关于 ATX server：
请查看这篇文章的介绍：
https://testerhome.com/topics/11738