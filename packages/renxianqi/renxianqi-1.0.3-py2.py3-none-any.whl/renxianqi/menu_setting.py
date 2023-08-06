#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/10/9 9:24 上午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : menu_setting.py.py
# @Project : absentee


import tkinter.messagebox as mb


def show_copyright():
    message = """
工具采用Apache License，请放心免费使用！
开发者：雷学委
作者网站：https://blog.csdn.net/geeklevin
社区信息：https://py4ever.gitee.io/
欢迎关注公众号【雷学委】，加入Python开发者阵营！
    """
    mb.showinfo("[人贤齐-万能清点工具]", message)

def show_about():
    message = """
操作说明：
界面分为左右两边：左边是全部人员输入框，按照一行一个人
界面分为左右两边：右边是实际出席人员输入框，一行一个人
点击按钮'开始校验' 
下面'缺席人员'可以显示哪些是缺少/没有到场的 
其他问题可以找qq：【Python全栈技术学习交流】：https://jq.qq.com/?_wv=1027&k=ISjeG32x 
    """
    mb.showinfo("[人贤齐-万能清点工具]", message)