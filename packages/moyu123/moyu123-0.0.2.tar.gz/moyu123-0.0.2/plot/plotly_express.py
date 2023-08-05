"""
使用 plotly express 简单绘图.

注意，只适用于 ipynb 这种网页绘图，无法调用 matplotlib 这种形式，即在 pycharm 中是无法使用的。

安装：pip install plotly_express

本模块包含数据分析中常用的是2种图形：
1、线图（含单线图，多线图，分组线图，第2坐标轴等）
2、散点图（含简单散点图，分组散点图）

以上不包含多子图等。

官方文档：
https://plotly.com/python/
https://plotly.com/python/line-charts/
https://plotly.com/python/figure-labels/

"""

from typing import List

from pandas import DataFrame, to_datetime

try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except:
    raise Exception("未找到 plotly.express 模块，请使用 pip install plotly_express 进行安装")


def plot_scatter(data: DataFrame, x_col: str, y_col: str, color_col: str = None, title: str = None):
    """
    绘制简单散点图。
    x_col：x轴的列名
    y_col：y轴的列名
    color_col: 颜色分组，不同的组用不同的颜色
    title: 标题

    df = px.data.iris()
    fig = px.scatter(df, x="sepal_length", y="sepal_width", color="species",
                    title="Automatic Labels Based on Data Frame Column Names")
    fig.show()
    """
    fig = px.scatter(data, x=x_col, y=y_col, color=color_col, title=title)
    fig.show()


def plot_line(data: DataFrame, x_col: str, y_col: str, color_col: str = None, title: str = None):
    """
    绘制曲线图.
    x_col：x轴的列名
    y_col：y轴的列名
    color_col: 颜色分组，不同的组用不同的颜色
    title: 标题

    其相当于pandas中的 data.groupby(color).plot() 的意思

    data = pd.DataFrame({'x': [1,2,3,4,5,6,7,8,9,10],
                         'y': [1,2,1,3,5,6,0,7,9,6],
                         'color': ['a']*5 + ['b']*5
                         })

    plot_line(data, 'x', 'y', 'color', 'title')
    """
    fig = px.line(data, x=x_col, y=y_col, color=color_col, markers=True, title=title)
    fig.update_layout(title={'text': title, 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
    # 如果x轴是日期，则处理日期格式
    try:
        _ = to_datetime(data[x_col])
        fig.update_xaxes(showgrid=True, tickformat="%Y-%m-%d")
    except:
        pass
    fig.show()


def plot_lines(data: DataFrame, x_col: str, y_cols: List[str], y2_cols: List[str] = None, title: str = ''):
    """
    绘制多条曲线。
    plot_line() 是根据某个分组来绘制多条曲线，而这里的 plot_lines() 则是 根据不同的 y 列来绘制多条图形，是不一样的想法。
    y2_cols: 第2坐标轴

    data = pd.DataFrame({'x': [1,2,3,4,5,6,7,8,9,10],
                         'y1': [1,2,1,3,5,6,0,7,9,6],
                         'y2': [1,2,3,4,5,6,4,3,6,1]
                         })
    plot_lines(data, 'x', ['y1'], ['y2'], 'title')

    """
    # 是否有第二坐标轴
    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])  # 绘制1*1的子图
    if len(y2_cols) > 0:

        x = data[x_col].values
        for y_col in y_cols:
            yi = data[y_col].values.copy()
            fig.add_trace(go.Scatter(x=x, y=yi, mode='lines+markers', name=y_col, connectgaps=False), row=1, col=1)  # connectgaps=False表示如果有null值也不会跳过

        for y_col in y2_cols:
            yi = data[y_col].values.copy()
            fig.add_trace(go.Scatter(x=x, y=yi, mode='lines+markers', name=y_col, connectgaps=False), row=1, col=1, secondary_y=True)  # 第2坐标轴
    # 没有第二坐标轴，直接叠加绘制即可
    else:
        x = data[x_col].values
        for y_col in y_cols:
            yi = data[y_col].values.copy()
            fig.add_trace(go.Scatter(x=x, y=yi, mode='lines+markers', name=y_col, connectgaps=False))  # connectgaps=False表示如果有null值也不会跳过
    # 如果x轴是日期，则处理日期格式
    try:
        _ = to_datetime(data[x_col])
        if ':' not in data[x_col].iloc[0]:
            fig.update_xaxes(showgrid=True, tickformat="%Y-%m-%d")
        else:
            fig.update_xaxes(showgrid=True, tickformat="%H:%M:%S \n %Y-%m-%d")
    except:
        pass
    # 添加xy轴标题
    x_title = x_col
    y1_title = y_cols[0] if len(y_cols) == 1 else 'y轴'
    y2_title = y2_cols[0] if len(y2_cols) == 1 else '第2y轴'
    fig.update_xaxes(title_text=x_title)
    fig.update_yaxes(title_text=y1_title, secondary_y=False)
    fig.update_yaxes(title_text=y2_title, secondary_y=True)
    # xy周标题也可以用下面的方法
    # fig.update_layout(title={'text': title, 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
    #                   xaxis_title='x_title',
    #                   yaxis_title='y_title',
    #                   )
    # 添加主标题
    fig.update_layout(title={'text': title, 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
    fig.show()
