from setuptools import find_packages
from distutils.core import setup

with open("README.md", "r",encoding="utf-8") as f:
  long_description = f.read()

setup(
    name="nonebot_plugin_jrrp2",   # python包的名字
    version="1.6",                # 版本号
    description='nonebot2带数据库可查询历史平均人品的jrrp插件',           # 描述
    long_description=long_description,                  # 详细描述，这里将readme的内容放置于此
    author='Rene8028',                                      # 作者
    author_email='Rene8028@outlook.com',              # 作者邮箱
    license='MIT License',                                    # 遵守协议
    packages=find_packages(),
    install_requires=["nonebot-adapter-onebot","nonebot2"],
    platforms=["all"],
    url='https://github.com/Rene8028/nonebot_plugin_jrrp2',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)