import requests
from io import StringIO, BytesIO
import pandas as pd
from datetime import datetime
import numpy as np

"""
    http://www.ine.cn/data/dailydata/js/js20210514.dat?temp2=1621241910624?rnd=0.5497482307020969
"""
class ContractMaintaner(object):
    apis = {
        'czce': 'http://www.czce.com.cn/cn/DFSStaticFiles/Future/{year}/{ds_nodash}/FutureDataReferenceData.csv',
        'dce': 'http://www.dce.com.cn/publicweb/businessguidelines/exportFutAndOptSettle.html',
        'shfe': 'http://www.shfe.com.cn/data/instrument/Settlement{ds_nodash}.dat',
        'ine': 'http://www.ine.com.cn/data/instrument/Settlement{ds_nodash}.dat',
        # 'cffex': 'http://www.cffex.com.cn/sj/jscs/{ms_nodash}/{day}/{ds_nodash}_1.csv'
    }

    def __init__(self, ds_nodash) -> None:
        self.ds_nodash = int(ds_nodash)
        super().__init__()

    def process_czce(self):
        r = requests.get(self.apis['czce'].format(
            year=self.ds_nodash//10000,
            ds_nodash=self.ds_nodash,
        ))
        m = pd.read_csv(StringIO(r.content.decode('utf8')))
        m[['合约代码', '产品代码', '交易所', '到期时间', '最小变动价位', '最小变动价值', 
       '最大下单量', '日持仓限额', '上市周期', '交割通知日',
       '第一交易日', '最后交易日', '交割结算日',
       '合约交割月份', '交易保证金率', '涨跌停板', '平今仓手续费']]

        """去掉第一行. 没有的信息"""
        m.drop([0], inplace=True)
        return m

    def process_dce(self):
        ds_nodash_d = datetime.strptime(str(self.ds_nodash), '%Y%m%d')
        r = requests.post(self.apis['dce'], data={
            'exportFlag': 'excel',
            'day': ds_nodash_d.day,
            'month': ds_nodash_d.month-1, # FIXME: 很奇怪, 月份参数需要-1
            'trade_type': 0,
            'variety': 'all',
            'year': ds_nodash_d.year,
        })
        m = pd.read_excel(BytesIO(r.content))
        print(m.columns)
        """
            ['品种', '合约代码', '结算价', '开仓手续费', '平仓手续费', '短线开仓手续费', '短线平仓手续费', '手续费收取方式',
            '投机买保证金率', '投机卖保证金率', '套保买保证金率', '套保卖保证金率'],
            手续费：对于收取方式为“绝对值”的品种为元/手，对于收取方式为“比例值”的品种为交易额的万分之几
        """
        m[
            ['合约代码', '结算价', '开仓手续费', '平仓手续费', '短线开仓手续费', '短线平仓手续费', '手续费收取方式',
            '投机买保证金率', '投机卖保证金率']
        ]
        m.loc[:, 'market'] = 'DCE'
        return m

    def process_shfe(self):
        r = requests.get(self.apis['shfe'].format(
            ds_nodash=self.ds_nodash
        ))
        j = r.json()
        m = pd.DataFrame(j['Settlement'])
        m.columns = [i.lower() for i in m.columns]
        """
            ['合约代码','结算价','交易手续费率(‰)','交易手续费额(元/手)',
            '投机买保证金率(%)','投机卖保证金率(%)','平今折扣率(%)
            ]
        """
        m.loc[:, 'market'] = 'SHFE'
        m.loc[:, 'instrumentid'] = m.instrumentid.str.strip()
        m = m.astype({
            'settlementprice': np.float64,
            'tradefeeration': np.float64,
            'tradefeeunit': np.float64,
            'spec_longmarginratio': np.float64,
            'spec_shortmarginratio': np.float64,
            'discountrate': np.float64,
        }).rename(columns={
            'instrumentid': 'iid',
        })
        return m[
            ['market', 'iid', 'settlementprice', 'tradefeeration', 'tradefeeunit', 
            'spec_longmarginratio', 'spec_shortmarginratio', 'discountrate']
        ]

    def process_ine(self):
        r = requests.get(self.apis['ine'].format(
            ds_nodash=self.ds_nodash
        ))
        j = r.json()
        m = pd.DataFrame(j['Settlement'])
        m.columns = [i.lower() for i in m.columns]
        """
            ['合约代码','结算价','交易手续费率(‰)','交易手续费额(元/手)',
            '投机买保证金率(%)','投机卖保证金率(%)','平今折扣率(%)
            ]
        """
        m.loc[:, 'market'] = 'SHFE'
        m.loc[:, 'instrumentid'] = m.instrumentid.str.strip()
        m = m.astype({
            'settlementprice': np.float64,
            'tradefeeration': np.float64,
            'tradefeeunit': np.float64,
            'spec_longmarginratio': np.float64,
            'spec_shortmarginratio': np.float64,
            'discountrate': np.float64,
        }).rename(columns={
            'instrumentid': 'iid',
        })
        return m[
            ['market', 'iid', 'settlementprice', 'tradefeeration', 'tradefeeunit', 
            'spec_longmarginratio', 'spec_shortmarginratio', 'discountrate']
        ]
       
