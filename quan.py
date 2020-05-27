import pandas as pd
from itertools import chain
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from typing import Tuple, List

from itertools import combinations
import pandas as pd
from itertools import chain
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from pprint import pprint
from time import time

import matplotlib
import matplotlib.gridspec as gridspec
matplotlib.font_manager._rebuild()
plt.rcParams['font.family']='sans-serif'
plt.rcParams['font.sans-serif'] = 'NSimSun,Times New Roman'# 中文设置成宋体，除此之外的字体设置成New Roman
plt.rcParams['axes.unicode_minus']=False
from matplotlib.lines import Line2D

from concurrent.futures import ProcessPoolExecutor, as_completed

# m1 = pd.read_csv('/Users/lifx/Downloads/all_stock_2013_14.gzip', compression='gzip', index_col=0)
# m2 = pd.read_csv('/Users/lifx/Downloads/all_stock_2015_17.gzip', compression='gzip', index_col=0)
# m3 = pd.read_csv('/Users/lifx/Downloads/all_stock_2018_19_20.gzip', compression='gzip', index_col=0)
# m = pd.concat([m1, m2, m3]).sort_values(['code', 'time']).reset_index(drop=True)
# m.to_parquet('/Users/lifx/Downloads/all_stock.parquet')
m = pd.read_parquet('/Users/lifx/Downloads/all_stock.parquet')
all_codes = m.code.drop_duplicates()

def get_score(slopes: pd.DataFrame, **kwargs):
    """
        根据斜率之间的度量，计算得分
        ------------------------------------------
        slopes: 各极值点到当日收盘价的连线的斜率, 系数等
        slope_distance_mx: 连线到各极值点的垂直距离绝对值 

        return: [
            score: float, 得分 
            index: list, 斜率所在直线的slopes终点索引链表
        ]
    """

    """
        计算各极值点A与极值点B到当前天直线的直线距离
        np.abs(A*x0+B*y0+C)/np.sqrt(x0**2+y0**2)
    """
    """使用For 循环计算."""
    # slope_distance_mx = np.zeros([slopes.shape[0], slopes.shape[0]]) 
    # for index, row in slopes.iterrows():
    #     slope_distance_mx[:, index] = slope_distance1(row.A, row.B, row.C, slopes.x, slopes.y)
    """使用numpy矩阵乘法."""
    slopes['z'] = 1
    part1 = slopes[['x', 'y', 'z']].values.dot(slopes[['A', 'B', 'C']].values.T)
    part2 = np.sqrt((slopes[['x', 'y']].values**2).sum(axis=1)).reshape([-1, 1])
    slope_distance_mx=np.abs(part1)/part2

    # pprint(np.where(part1>0, 1, 0))

    """
        阻力(支撑)线两侧极值点的分布情况
    """
    x_axis_mx = np.repeat(slopes[['x']].values, slopes.shape[0], axis=1) # 将x坐标扩展n次成方阵
    x_between_mx = np.where(x_axis_mx>x_axis_mx[:, 0], 1, 0) * part1  # 筛选极值点到当日点之间的极值点
    side1 = np.where(x_between_mx<0, 1, 0).sum(axis=0) # 直线一侧
    side2 = np.where(x_between_mx>0, 1, 0).sum(axis=0) # 直线另一侧
    side_ratio = side1/(side1+side2)
    """
        两条先之间的距离，使用对应点到线的距离，因此距离不是对偶的，使用三角矩阵计算，取两点的最短距离.
    """
    tril = np.tril(slope_distance_mx) #下三角
    triu = np.triu(slope_distance_mx).T #上三角转置
    slope_distance_mx = np.where(tril>triu, triu, tril) #取对角矩阵的较小值
    """设置两条斜率线之间差值的阈值，根据阈值返回线index"""
    colinearity_index = np.unique(
        np.r_[
            np.where((slope_distance_mx<=0.004)&(slope_distance_mx>0.000001))
    ])

    """计算筛选出来的点之间的距离之和."""
    aa = tuple(zip(*combinations(sorted(colinearity_index, key=lambda x: -x), 2)))
    ret = slope_distance_mx[aa].sum()
    # if True:
    if ret < 15000.01:
        # colinearity_index = side_ratio[colinearity_index].argsort()[:1]
        colinearity_index = [59, 14]
        return (ret, colinearity_index, slopes.loc[colinearity_index, 'slope'])
    return None

def slope_distance2(A, B, C, x0, y0, x_y):
    return np.abs(A*x0+B*y0+C)/x_y

def colinearity(mx: pd.Series, source_point: Tuple[float]):
    """
        共线性处理函数
        ----------------------------------------------------------------
        输入为目标点source_point和坐标点集合mx，计算目标点与坐标点集合所有点的斜率
    """
    return 

def win_offset_extremum(df, action, win_size=68, ptype=None):
    """窗口极值函数."""
    assert action in ('max', 'min', 'mean')
    assert ptype in ('oc_min', 'oc_max', 'high', 'low')
    ret = df[ptype].rolling(win_size, center=True, min_periods=1) # 设置min_periods=1防止最左最右的价格窗口函数返回nan
    if action == 'max':
        return ret.max()#.shift(-win_size)
    elif action == 'mean':
        return ret.mean()
    else:
        return ret.min()#.shift(-win_size)
    
def GeneralEquation(first_x,first_y,second_x,second_y):
    """
    一般式 Ax+By+C=0, y=(Ax+C)/-B = kx + c
    from http://www.cnblogs.com/DHUtoBUAA/
    返回: A, B, C, 斜率
    """
    A = second_y - first_y
    B = first_x - second_x
    C = second_x * first_y - first_x * second_y
    return [A,B,C,-A/B,-C/B]

code_index_map = m.reset_index().groupby('code').index.agg(['min', 'max']).to_dict('index')

def support_ma(
    stock_code=None, show_plot=False, method='max', 
    win_size=68, n_extremum_keep=30, n_last_point=3, volume_win_size=120,
    start_offset=0, end_offset = 0, 
):
    """
        stock_code: 股票代码
        win_size: 滑动窗口长度(单位:交易日)
        n_extremum_keep: 极值持续长度(单位:交易日)
        volume_win_size: 交易量滑动窗口长度
    """
    extremum_method = method
    dim = f'{extremum_method}{win_size}'
    bar_max_s = f'max{win_size}'
    bar_min_s = f'min{win_size}'
        
    code = stock_code
    start = code_index_map[code]['min'] + start_offset
    end = code_index_map[code]['max'] - end_offset
        
    mx = m.iloc[start:end, [3, 0, 6, 2, 4, 5]] # close, time, volume, open, high, low

    '''
        先选出olch的极大、小值，在有极大(小)值的bar上，画出olch到统计日收盘价的直线。因此在每条极值bar上会有4条线
    '''
    open_close_map_dict = dict([
        (f'oc_max', lambda x: x[['open', 'close']].max(axis=1)),
        (f'oc_min', lambda x: x[['open', 'close']].min(axis=1)),
    ])
    moving_func_dict = dict([
        (bar_max_s, lambda x: win_offset_extremum(x, 'max', win_size=win_size, ptype='high')),
        (bar_min_s, lambda x: win_offset_extremum(x, 'min', win_size=win_size, ptype='low')),
        ('v_peak', lambda x: x.volume.divide(x.volume.rolling(volume_win_size, center=True).mean()).round(2))
    ])
                                           
    # res = mx.reset_index(drop=True).dropna().rename(
    #     columns={'close': 'price'}
    # ).assign(**moving_func_dict).assign(**moving_equal_dict)

    res = mx.reset_index(drop=True).dropna().assign(**open_close_map_dict).assign(**moving_func_dict)
    
    # 标记: 峰值(谷值)的持续天数超过 n_extremum_keep 的日期
    # FIXME: 同样的问题，如果只针对max60分组的话，会导致不是连续日期max60也会分到一组，因此需要先对max60做日期连续性处理

    """将win_max or win_min分段"""
    def gg(x):
        if x == support_ma.r:
            return support_ma.iid
        else:
            support_ma.iid += 1
            support_ma.r = x
            return support_ma.iid

    support_ma.r = res.loc[:, bar_max_s].dropna().values[0]
    support_ma.iid = 0
    res[f'{bar_max_s}_group'] = res.loc[:, bar_max_s].dropna().apply(gg)

    support_ma.r = res.loc[:, bar_min_s].dropna().values[0]
    support_ma.iid = 0
    res[f'{bar_min_s}_group'] = res.loc[:, bar_min_s].dropna().apply(gg)
    
    # bar_array = res.loc[:, bar_max_s].dropna().values
    # bar_elem_map = dict(zip(*[set(bar_array), range(bar_array.size)]))
    # res[f'{bar_max_s}_group'] = np.vectorize(bar_elem_map.get)(bar_array)

    # bar_array = res.loc[:, bar_min_s].dropna().values
    # bar_elem_map = dict(zip(*[set(bar_array), range(bar_array.size)]))
    # res[f'{bar_min_s}_group'] = np.vectorize(bar_elem_map.get)(bar_array)

    # 筛选段长大于 n_extremum_keep 的
    top_points_index = res.reset_index().groupby(
        [f'{bar_max_s}_group', bar_max_s]
    ).index.agg(
        ['max', 'count']
    ).query('count>@n_extremum_keep').pipe(
        lambda x:x['max']-win_size//2
    ).values

    # tmp_mx = res.reset_index()[['index', f'{bar_max_s}_group', bar_max_s]].values
    # # concated_mx = tmp_mx[:, 1]*1000000 + tmp_mx[:, 2]
    # _, value_counts = np.unique(tmp_mx[:, 1:], axis=0, return_counts=True)
    # ss = map(
    #     lambda x: x.max()-win_size//2, 
    #     filter(
    #         lambda x: x.size>n_extremum_keep,
    #         np.split(tmp_mx[:, 0], np.cumsum(value_counts))[:-1]
    #     )
    # )
    # pprint(list(ss))
    
    bottom_points_index = res.reset_index().groupby(
        [f'{bar_min_s}_group', bar_min_s]
    ).index.agg(
        ['max', 'count']
    ).query('count>@n_extremum_keep').pipe(
        lambda x: x['max']-win_size//2
    ).values
    
    """
        1. res.index.isin(a) 持续N日的峰值
        2. res.max60==res.price 当日价等于峰值
    """
    # extremum_con = res.index.isin(a)&(res[dim]==res.price)
    top_extremum_con = res.index.isin(top_points_index)&(res[bar_max_s]==res.high)
    bottom_extremum_con = res.index.isin(bottom_points_index)&(res[bar_min_s]==res.low)
    extremum_con = (top_extremum_con)|(bottom_extremum_con)
    
    if res.loc[extremum_con, :].shape[0] < n_last_point:
        n_last_point = res.loc[extremum_con, :].shape[0]

    # x0 = res.loc[extremum_con, ['price']].iloc[-n_last_point:, 0].index
    # y0 = res.loc[extremum_con, ['price']].iloc[-n_last_point:, 0].values
    # print(res.loc[extremum_con, ['price']].iloc[-n_last_point:, 0])
    # x1 = res.iloc[-1:, 0].index[0]
    # y1 = res.iloc[-1:, 0].values[0]
    # print((x1, y1))

    x1 = res.iloc[-1:, 0].index[0]
    y1 = res.iloc[-1:, 0].values[0]

    # high_extremum_points: pd.Series = res.loc[top_extremum_con, ['high']].iloc[-n_last_point:, :]
    top_extremum_points: pd.DataFrame = res.loc[top_extremum_con, [bar_max_s, 'high']].iloc[-n_last_point:, :]
    bottom_extremum_points: pd.DataFrame = res.loc[bottom_extremum_con, [bar_min_s, 'low']].iloc[-n_last_point:, :]
    # low_extremum_points: pd.Series = res.loc[bottom_extremum_con, ['low']].iloc[-n_last_point:, :]

    extremum_points = pd.concat([
        bottom_extremum_points.iloc[:, 0], 
        bottom_extremum_points.iloc[:, 1], 
        top_extremum_points.iloc[:, 0], 
        top_extremum_points.iloc[:, 1]
    ]).sort_index()

    # slope_mean = []
    # for i in range(n_last_point):
    #     slope_mean.append((x0[i], GeneralEquation(x0[i], y0[i], x1, y1)[3]))

    """计算当日收盘价到各极值点的斜率."""
    # n_last_extremum_points = extremum_points[-n_last_point:].reset_index().assign(
    #     slope=GeneralEquation(extremum_points[-n_last_point:].index, extremum_points[-n_last_point:].values, x1, y1)[3]
    # ) 
    # slopes: pd.DataFrame = extremum_points.reset_index().assign(
    #     slope=GeneralEquation(extremum_points.index, extremum_points.values, x1, y1)[3],
    #     c=GeneralEquation(extremum_points.index, extremum_points.values, x1, y1)[4],
    #     A=GeneralEquation(extremum_points.index, extremum_points.values, x1, y1)[0],
    #     B=GeneralEquation(extremum_points.index, extremum_points.values, x1, y1)[1],
    #     C=GeneralEquation(extremum_points.index, extremum_points.values, x1, y1)[2],
    # ) 
    # slopes.to_csv('/Users/lifx/workroom/slopes.csv', sep=',')

    slopes: pd.DataFrame = pd.concat([
        extremum_points.reset_index(),
        pd.DataFrame(GeneralEquation(extremum_points.index, extremum_points.values, x1, y1)).T
    ], axis=1)
    slopes.columns = ['x', 'y', 'A', 'B', 'C', 'slope', 'c']


    """计算斜率之间的差值度量(最简单的就是绝对差值)."""
    # slope_distinct_list: List[Tuple[int, int, float]] = [
    #     (i, j, abs(slopes.iloc[i,-1] - slopes.iloc[j, -1])) 
    #     for i in range(0, slopes.shape[0]) for j in range(i+1, slopes.shape[0])
    # ]
    # slope_distance_mx = np.abs(np.subtract.outer(slopes.loc[:, 'slope'].values, slopes.loc[:, 'slope'].values))

    """根据斜率以及斜率差值计算得分."""
    r = get_score(slopes)
    
    # if r is not None and len(r[1]) >= 3 and r[2].min() > 0:
    if True:
        # print(f'hit: {code}, {sum(map(lambda x: x[2], slope_distinct_list))} {colinearity_index}')
        print(f'hit: {code}, {r}')
        if show_plot:
#             fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(17, 18))
            fig = plt.figure(1, figsize=(17, 12))
            gridspec.GridSpec(4,1)
            ax = plt.subplot2grid((4,1), (0,0), rowspan=3)
            
            xticks_index = np.linspace(res.index.min(), res.index.max(), 10).astype(int)
            res[['open', 'close', 'high', 'low', bar_max_s, bar_min_s]].plot(
                kind='line', style=['-', '-', '-', '-','--', '--'], linewidth=0.8, ax=ax,
                # color=['b', '#4287f5', '#4287f5', '#4287f5'],
                xlim=(res.index.min(), res.index.max())
            )
            ax.set_xticklabels(res.loc[xticks_index, 'time'])
            
            v_ax = plt.subplot2grid((4,1), (3,0), rowspan=1)
            res[['v_peak']].plot(
                kind='line', style='-', linewidth=0.5, ax=v_ax,
                xlim=(res.index.min(), res.index.max())
            )
            v_ax.set_xticklabels(res.loc[xticks_index, 'time'])
            
            """Plot上下极值."""
            if res.loc[bottom_extremum_con, :].shape[0]>0:
                res.loc[bottom_extremum_con, bar_min_s].plot(kind='line', style=['r*'], ax=ax)        

            if res.loc[top_extremum_con, :].shape[0]>0:
                res.loc[top_extremum_con, bar_max_s].plot(kind='line', style=['*'], color=['#04cc11'], ax=ax)        
        
        n_last_point_array = []
        # for i in range(n_last_point):
        #     if show_plot:
        #         ax.add_line(Line2D((x0[i],x1), (y0[i],y1), linewidth=1))
        #     n_last_point_array.append((x0[i], y0[i]))

        """Plot斜率线."""
        for _, row in slopes.iloc[r[1], :].iterrows():
            if show_plot:
                ax.add_line(Line2D((row.x,x1), (row.y,y1), linewidth=1))
            n_last_point_array.append((row.x, row.y))
        
        if False:
            # for index, value in res.loc[colinearity_index, 'price'].items():
            for index, row in n_last_extremum_points.iterrows():
                # ax.add_line(Line2D((index, x1), (value, y1), linewidth=1))
                ax.add_line(Line2D((row.x, x1), (row.y, y1), linewidth=1))
            # res.loc[colinearity_index, ['price']].plot(kind='line', style=['yo'], ax=ax)
            
        n_last_point_array.append((x1, y1))
        return len(n_last_point_array)
    
    return None


# import cProfile
# import pstats
# pr = cProfile.Profile()
# pr.enable()

support_ma(stock_code='000799.XSHE', method='min', win_size=10, n_extremum_keep=5, n_last_point=30, show_plot=True, start_offset=900)

'''
b = time()
futures = []
with ProcessPoolExecutor(max_workers=8) as executor:
    for index, code in enumerate(all_codes):
        futures.append(executor.submit(support_ma, code, win_size=30, n_extremum_keep=15, n_last_point=30, show_plot=False, offset=0))
print(time()-b)
'''

# pr.disable()
# import io
# s = io.StringIO()
# ps = pstats.Stats(pr, stream=s).sort_stats('cumtime').print_stats(10)
# ps.print_stats()
# print(s.getvalue())