"""
实现 plotly_express.py 中的几个常用绘图api，适用接口需完全相同，不同的仅仅是底层实现框架。



"""
from typing import List

import matplotlib.pyplot as plt
from pandas import DataFrame

try:
    import seaborn as sns

    sns.set_theme(style="whitegrid")
except:
    raise Exception("please install seaborn with commond pip install seaborn")


def plot_scatter(data: DataFrame, x: str, y: str, color: str = None, title: str = None):
    """
    绘制散点图

    data = pd.DataFrame({'xx': [1,2,3,4,5,6,7,8,9,10],
                         'yy': [1,2,1,3,5,6,0,7,9,6],
                         'color': ['a']*5 + ['b']*5
                         })
    color = 'color'
    x = 'xx'
    y = 'yy'
    title = '代码'
    """
    if color:
        for cat in data[color].unique():
            dfi = data.loc[data[color] == cat]
            xi, yi = dfi[x], dfi[y]
            sns.scatterplot(x=xi, y=yi, label=cat)
    else:
        xi, yi = data[x], data[y]
        sns.lineplot(x=xi, y=yi, marker='o')
    plt.legend(loc='best')
    plt.title(title)


def plot_line(data: DataFrame, x: str, y: str, color: str = None, title: str = None):
    """
    绘制单曲线图

    data = pd.DataFrame({'xx': [1,2,3,4,5,6,7,8,9,10],
                         'yy': [1,2,1,3,5,6,0,7,9,6],
                         'color': ['a']*5 + ['b']*5
                         })
    color = 'color'
    x = 'xx'
    y = 'yy'
    """
    if color:
        for cat in data[color].unique():
            dfi = data.loc[data[color] == cat]
            xi, yi = dfi[x], dfi[y]
            sns.lineplot(x=xi, y=yi, label=cat, marker='o')
    else:
        xi, yi = data[x], data[y]
        sns.lineplot(x=xi, y=yi, marker='o')
    plt.legend(loc='best')
    plt.title(title)


def plot_lines(data: DataFrame, x: str, y: List, y2: List = None, title: str = '标题名称'):
    """
    绘制多条曲线

    data = pd.DataFrame({'xx': [1,2,3,4,5,6,7,8,9,10],
                         'yy': [1,2,1,3,5,6,0,7,9,6],
                         'color': ['a']*5 + ['b']*5
                         })
    data['y2'] = data['yy'] * 2 - 1
    color = 'color'
    x = 'xx'
    y = ['yy']
    y2 = ['y2']

    y = ['yy', 'y2']
    """
    for yi in y:
        sns.lineplot(data[x], data[yi], label=yi, marker='o')
    plt.legend(loc='best')
    plt.title(title)
