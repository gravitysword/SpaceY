import importlib
import subprocess
import sys

def install_package(package_name):
    try:
        # 尝试导入包
        importlib.import_module(package_name)
        print(f"{package_name} 已经安装")
    except ImportError:
        # 如果包未安装，则使用 pip 安装
        print(f"正在安装 {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"{package_name} 安装成功")

def main():
    with open("requirements.txt") as f:
        for i in f:
            install_package(i)
