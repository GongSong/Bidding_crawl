# 基于镜像基础
FROM python:3.7

# 设置代码文件夹工作目录 /app
WORKDIR /app

# 复制当前代码文件到容器中 /app .表示当前目录
ADD . /app

# 安装所需的包
RUN pip install -r requirements.txt

#系统是linux 要赋予adb可执行的权限
RUN chmod +x /usr/local/lib/python3.7/site-packages/airtest/core/android/static/adb/linux/adb

#当容器运行时,运行的命令
CMD ["python", "Pydaemon.py"]