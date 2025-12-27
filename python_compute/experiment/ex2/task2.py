"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""

try:
    # see if Swampy is installed as a package
    from swampy.TurtleWorld import *
except ImportError:
    # otherwise see if the modules are on the PYTHONPATH
    from swampy.TurtleWorld import *


def koch(t, n):
    """Draws a koch curve with length n."""
    if n<20:  # 修改基本情况的条件
        fd(t, n)
        return
    # 将线段分成5部分而不是3部分
    m = n/5.0
    
    # 绘制第一部分
    koch(t, m)
    
    # 旋转60度
    lt(t, 60)
    koch(t, m)
    
    # 第二次旋转-120度
    rt(t, 120)
    koch(t, m * 3) # 中间部分是3个m
    
    # 第三次旋转60度
    lt(t, 60)
    koch(t, m)
    
    # 最后一部分
    koch(t, m)


def snowflake(t, n):
    """Draws a snowflake (a triangle with a Koch curve for each side)."""
    for i in range(3):
        koch(t, n)
        rt(t, 120)


world = TurtleWorld()
bob = Turtle()
bob.delay = 0.01 # 减缓速度以便观察

# 调整初始位置
bob.x = 300
bob.y = -100
bob.redraw()

# 绘制泛化koch曲线（单边）
snowflake(bob, 500)

world.mainloop()
