# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/2/28

import setuptools

long_description = """
# yyxx-game-pkg

`yyxx-game-pkg` 是一个专门为 yyxx 公司开发的 Python 内部接口集合。

## 模块

### xtrace

`xtrace` 模块封装了链路追踪的帮助类，可以帮助开发人员快速地实现链路追踪功能。该模块提供了以下功能：

- 封装了调用链路追踪的相关逻辑，可以自动记录服务间的调用关系。
- 提供了统一的接口，方便开发人员在不同的应用场景中调用。

## 安装
要安装yyxx_pkg,请使用：
`pip install yyxx-game-pkg`

"""

setuptools.setup(
    name="yyxx-game-pkg",
    version="0.0.1b",
    author="yyxxgame",
    description="yyxx game custom module",
    long_description=long_description,
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "opentelemetry-api>=1.16.0",
        "opentelemetry-exporter-jaeger>=1.16.0",
        "opentelemetry-sdk>=1.16.0",
        "opentelemetry-instrumentation-requests>=0.37b0"
    ]
)