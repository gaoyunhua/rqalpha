#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tkinter as tk
from tkinter import Menu    # 导入菜单类

win = tk.Tk()
win.title("Python GUI")    # 添加标题

# 创建菜单栏功能
menuBar = Menu(win)
win.config(menu=menuBar)

# 创建一个名为File的菜单项
fileMenu = Menu(menuBar)
menuBar.add_cascade(label="File", menu=fileMenu)

# 在菜单项File下面添加一个名为New的选项
fileMenu.add_command(label="New")

# 在菜单项下面添加一个名为Exit的选项
fileMenu.add_command(label="Exit")


win.mainloop()      # 当调用mainloop()时,窗口才会显示出来





