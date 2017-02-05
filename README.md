### 简介
这是一个用tornado框架搭建博客程的示例项目，前端页面和后端都是自己实现的，项目主体采用了三层架构。

### 目录结构
1. dao层是数据访问层，主要用来对数据库进行操作
2. service层是业务逻辑层，主要是调用dao层取得数据，返回给表示层，承上启下
3. web层是表示层，接受请求，返回数据
4. app.py启动文件
5. config.py配置文件

### 部分知识点
1. 整体框架：3层架构+MVC+SQLAlchemy
2. 前端html+css+jquery+ajax
3. 前端用jquery自己实现form表单验证
4. 后端自己实现分页插件、form表单验证
5. 后端自己实现session插件，只需修改配置文件就可实现将session放置在内存、memcached、redis中
6. 博客首页简单利用redis进行缓存
7. 文章多级评论

### 备注
这个项目是我早期完成，现在看来有许多不够满意的地方，代码有很多不够规范的地方，commit信息也不够清楚，
后期有时间的话，会对整体进行一个重构

### 博客效果

#### 1.首页视图
![index](https://github.com/Wxtrkbc/Tornado-boke/raw/master/web/static/screenshots/3.jpg)
#### 2.目录视图
![table of contents](https://github.com/Wxtrkbc/Tornado-boke/raw/master/web/static/screenshots/2.jpg)
#### 3.文章视图
![article](https://github.com/Wxtrkbc/Tornado-boke/raw/master/web/static/screenshots/4.jpg)
#### 4.评论树视图
![comment-tree](https://github.com/Wxtrkbc/Tornado-boke/raw/master/web/static/screenshots/5.jpg)
#### 5.注册视图
![register](https://github.com/Wxtrkbc/Tornado-boke/raw/master/web/static/screenshots/6.jpg)
