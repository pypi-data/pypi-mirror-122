# from distutils.core import setup
from setuptools import setup,find_packages


def readme_file():
    with open("README.md", encoding="utf-8") as rf:
        return rf.read()


setup(
    name="frogpy",  # 需要打包的名字
    version="0.0.1",  # The initial release version
    description="frogpy: Implement algorithms and solve equations",
    packages=find_packages(),
    author="Tao Xiang",  # Full name of the author
    url="https://github.com/xiang-tao",
    author_email="xiangtao@smail.xtu.edu.cn",
    long_description=readme_file()
)
