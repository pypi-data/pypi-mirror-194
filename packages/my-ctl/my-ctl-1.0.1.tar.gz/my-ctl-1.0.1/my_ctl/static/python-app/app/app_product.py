#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import json

class AppProduct:
    """
    运行环境
    """

    def __init__(self):
        """
        环境变量
        """
        # 日志
        self.IS_DEBUG = True
        # 声明环境变量: product.json 保持一致

    def create():
        # 环境
        env_code = "debug"
        if "ENV" in os.environ:
            env_code = os.environ["ENV"]
        envs = {}
        with open("product.json", "r") as file:
            envs = json.loads(file.read())["envs"]
        runtime = envs[env_code]
        # 环境变量
        if "IS_DEBUG" in os.environ:
            runtime["IS_DEBUG"] = os.environ["IS_DEBUG"]
        # 初始化配置
        prod = AppProduct()
        prod.__dict__ = runtime
        return prod


# exports product
product = AppProduct.create()
