#coding=utf-8
from distutils.core import setup
setup(
    name='supermath1', # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，里面只有数学方法，用于测试哦', #描述
    author='fangchangfan', # 作者
    author_email='2803284510@qq.com', py_modules=['supermath1.demo1','supermath1.demo2'] # 要发布的模块
)
