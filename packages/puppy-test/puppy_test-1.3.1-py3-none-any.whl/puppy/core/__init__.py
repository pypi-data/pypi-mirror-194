# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    describe:This is a test frame about api, before using it, please copy the file dir as your project dir.
"""
from .function.thread.pool import ResourcePool
from .useful.cfg import config

config = config
ResourcePool = ResourcePool
