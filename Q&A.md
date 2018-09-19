常见问题：
### 1：没有可用的节点
- Q： 运行用例之后会提示这个-ERROR: no hubs is availabe!
- A： 说明没有可以使用的selenium节点执行测试。请检查是否已启动对应的 selenium server，并已配置到节点管理中，而且服务器可以正常访问该节点。
### 2：selenium 的浏览器被占用
- Q：使用docker启动的selenium 镜像服务，如果用例执行报错， selenium grid console中的Chrome浏览器好像被置灰不可用了
- A：这是因为如果执行报错时，没有正常退出 driver，导致对应的selenium线程持续被占用，需要等待一段时间才能释放。建议启动docker 的时候把最大进程设置为10， 这样可以并发执行，提高使用率：
sudo docker run -e NODE_MAX_INSTANCES=10 -e NODE_MAX_SESSION=10 -d --net grid -e HUB_HOST=selenium-hub -v /dev/shm:/dev/shm selenium/node-firefox-debug

### 3：selenium 相关报错
- Q：selenium相关报错
- A：可能对应的 selenium server版本不支持目前使用的一些功能，建议更新到较新版本的 selenium server
