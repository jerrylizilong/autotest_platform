# autotest_platform
基于python+selenium的自动化测试管理、执行平台。

## 版本要求：
python 3.4 以上

## 1. 管理平台：
基于flask进行开发，进行用例、用例集、步骤等的增删改查等功能。

## 2. 启动core服务：
```python
python app/core/coreservice.py
```


- 基于selenium进行封装，从数据库中读取需要执行的测试用例，并转化、执行、记录测试结果及截图。
- 需结合selenium grid 或 selenium docker 作为节点进行具体执行载体。


## 安装步骤：
- 1. clone 或下载代码包到本地解压:   
```
git clone https://github.com/jerrylizilong/autotest_platform.git
```


- 2. 按requirements.txt 安装依赖:
```
cd autotest_platform
pip3 install -r requirements.txt
```
- 3. 数据库配置： 创建数据库，并执行 init.sql 建表并初始化配置数据。
- 4. 配置： 修改 app/config.py 中关于数据库部分的配置： host、port、database、user、password。

## 启动：
### 1.启动 flask：
```
python run.py 
```
       
此时可通过访问  localhost:5000  访问登录界面。
初始用户及密码：  admin/0
### 2. 启动 core service（selenium 的执行服务）：
```python
python app/core/coreservice.py
```


### 3. selenium 接入
可以按以下两种方式进行接入：
#### 3.1 selenium server接入：
- 服务端启动： python app/core/service.py， 将通过9998 端口监听节点启动、关闭状态
- selenium grid 节点启动： 将app/client 目录复制到已安装selenium driver 的服务器/PC 中，修改client.py文件中host 为服务端对应地址，并启动： 
```python
python client.py
```

服务启动后，会启动 selenium server，并注册到服务器中。

#### 3.2 其他方式（原有selenium server、selenium docker等）
- 将已启动的selenium服务地址（如 http://172.10.XXX.XXX:4444）手动添加到自动化测试-节点管理中即可。


## 使用说明：

### 1. 新建用例：

用例步骤说明：
- 每个用例步骤中通过逗号进行分隔。
- 单个步骤的格式： 步骤名称+分隔符（|）+参数列表（参数间按@@进行分隔）。如：填写|id@@kw@@selenium， 表示步骤为“填写”，参数列表为“id、kw、selenium”。
- 默认的参数含义：1：通过什么属性定位目标元素（可使用id、name、class、text、xpath、css等多种定位方式进行定位） 2：目标元素对应的属性值（如id = kw） 3：其他。
- 例如：填写|id@@kw@@selenium： 代表通过 id = kw 查找到输入框，并输入  selenium 。

#### 具体步骤说明请查看菜单：自动化测试-步骤说明。

#### 用例说明：
例子：在百度中输入selenium，并验证查询结果是否正确。

Chrome,前往|http://www.baidu.com,填写|id@@kw@@selenium,点击|id@@su,验证|Web Browser Automation,截图

步骤解析：

- Chrome： 调用 Chrome driver 进行测试。    
- 前往|http://www.baidu.com ：  前往目标页。
- 填写|id@@kw@@selenium ：  在 id 为 kw 的元素中输入 selenium。    
- 点击|id@@su ： 点击 id 为 su 的元素。
- 验证|Web Browser Automation ：  验证页面中是否出现 ‘Web Browser Automation’ 的文字。
- 截图： 对当前页面进行截图并保存。


### 2.公共用例

某些公共的步骤，可以封装为公共方法进行调用：
- 公共方法添加：新建用例，选择用例类型为 公共用例， 所属模块为public。
- 公共方法调用：步骤： 公共方法|公共方法名， 如  公共方法|登录；公共方法|查询订单。


### 3.用例管理：

还可对用例进行如下管理：
- 用例查询
- 用例复制：新建用例时可考虑复制一条步骤类似的用例，再修改对应步骤。
- 用例删除：逻辑删除，可在数据库对应表中恢复。
- 用例执行：执行单条用例。可查看对应执行记录、截图、或重跑用例。


### 4.用例集管理：

- 用例集（test suite）对应一个测试范围，可关联多个不同的用例。
- 执行用例集时会根据设置的并发数进行并发执行，提高测试效率。
- 用例集中的用例是从测试用例中复制而来，因此每个用例可以在多个不同的测试用例集中关联。
- 用例集可重跑全部用例、重跑失败用例、重跑单条用例。 注意：重跑用例时，会自动从对应测试用例中加载最新的步骤。


### 5.节点管理：
- 节点：可加载多个selenium grid节点，系统根据当前可用节点的数量，分配用例进行执行。

### 6.步骤管理：
- 步骤：现已对大部分常见步骤进行了封装。
- 扩展封装：可根据需要进行扩展封装。
- - 可直接封装selenium的方法，请参考 刷新、前往、悬浮点击 等方法。
- - 可对selenium提供的方法进行二次封装，请参考 点击、填写、选择等方法。对应扩展代码可在  app/core/extend.py 文件中进行管理。





