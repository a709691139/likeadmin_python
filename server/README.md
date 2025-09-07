# 服务端项目
fastapi 文档：https://fastapi.tiangolo.com/zh/tutorial/first-steps/#_2

## 启动
服务端项目分为 后台 、 前台 两个服务

后台
打开终端，使用cd命令进入server目录，运行python asgi.py命令启动项目。

两个都要跑

cd likeadmin_python/server
### 方式一
python3 asgi.py
### 方式二
python3 -m uvicorn asgi:app --reload --port 8000
打开浏览器，访问http://127.0.0.1:8000/api/common/index/config，即可看到接口返回信息，说明启动成功。

前台
打开终端，使用cd命令进入server目录，运行python asgi_front.py命令启动项目。

cd likeadmin_python/server
### 方式一
python3 asgi_front.py
### 方式二
python3 -m uvicorn asgi_front:app --reload --port 8002
打开浏览器，访问http://127.0.0.1:8002/api/index，即可看到接口返回信息，说明启动成功。


## 接口文档
http://127.0.0.1:8000/docs 后台接口文档
http://127.0.0.1:8002/docs 前台接口文档


databases==0.6.1
SQLAlchemy==1.4.41
aiomysql==0.1.1