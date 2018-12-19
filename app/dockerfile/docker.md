
## 1. 使用 s2i 从github 获取最新代码并构建镜像：
- 安装 s2i 服务。 参考： https://github.com/openshift/source-to-image
- 拉取所需的 python-35-centos7 镜像：  docker pull python-35-centos7
- 使用 s2i 构建镜像：
```
s2i build https://github.com/jerrylizilong/autotest_platform.git centos/python-35-centos7 jerry-sample-flask
```

## 2.基于新生成的镜像，创建可运行的 flask 镜像：
- 新建目录，复制 Dockerfile 和 runall.sh 到该目录中。
- 在该目录中构建镜像：  docker build -t jerry/jerrynewflask:v1 .

### 3. 启动容器：
```
docker run -d -t -p 5001:5000 --net grid --link mysql:mysql --link selenium-hub:selenium --name flask1 648f9459184e
```

### 4. 进入容器中，修改 config 文件：
```
docker exec -it flask1 bash
```
修改 /opt/app-root/src/app/config.py 文件中的配置。