# 我们将实时行情落地，在hive中保存5个表，并保持实时更新，最早历史数据为20140701。数据都在8网段hive中，他们的名字及查询方法如下：

### 上交所实时行情表。该行情数据，每三秒钟更新一次，三秒内无数据则不发送个股行情，三秒内有数据则以最后一次委托（这点可探讨）时间作为时间戳

数据表：db_quotation.tb_level1_realtime_shanghai

查询方法：select * from db_quotation.tb_level1_realtime_shanghai where dw_trade_date=20180705 limit 10;

### 上交所证券信息表，每天早晨9点更新一次

数据表：db_quotation.tb_level1_security_info_shanghai

查询方法：select * from db_quotation.tb_level1_security_info_shanghai where dw_trade_date=20180705 limit 10;

### 深交所实时行情表。该行情数据，每三秒内如果有数据，则以3秒的整数倍时间戳发送数据，如果无数据则不发。但每分钟一定发送一次数据

数据表：db_quotation.tb_level1_realtime_shenzhen

查询方法：select * from db_quotation.tb_level1_realtime_shenzhen where dw_trade_date=20180705 and date_time>'201807050930000' limit 10;

### 深交所证券信息表，每天早晨9点更新一次

数据表：db_quotation.tb_level1_security_info_shenzhen

查询方法：select * from db_quotation.tb_level1_security_info_shenzhen where dw_trade_date=20180705 limit 10;

### 深交所指数信息表，每天早晨9点更新一次

数据表：db_quotation.tb_level1_index_info_shenzhen

查询方法：select * from db_quotation.tb_level1_index_info_shenzhen where dw_trade_date=20180705 limit 10;

# 各个表字段名称、中文解释、特别说明及举例

### 上交所实时行情数据db_quotation.tb_level1_realtime_shanghai

| 序号 | 字段类型      | 字段名称         | 中文解释                         | 股票举例          | 国债举例          | 基金举例          | 指数举例          | 备注                                                         |
| ---- | ------------- | ---------------- | -------------------------------- | ----------------- | ----------------- | ----------------- | ----------------- | ------------------------------------------------------------ |
| 1    | string        | date_time        | 当前时间,格式为yyyyMMddHHmmssSSS | 20180614100000170 | 20180614095547410 | 20180614095942900 | 20180614095959800 |                                                              |
| 2    | string        | remarked         | 特殊标记,恒值为空                |                   |                   |                   |                   |                                                              |
| 3    | string        | securityId       | 证券代码                         | 600031            | 010303            | 501029            | 000001            |                                                              |
| 4    | string        | symbol           | 证券简称                         | 三一重工          | 03国债⑶           | 红利基金          | 上证指数          |                                                              |
| 5    | decimal(11,3) | prevClosePrice   | 昨日收盘价                       | 8.680             | 98.700            | 1.022             | 3049.7965         |                                                              |
| 6    | decimal(11,3) | openPrice        | 今日开盘价                       | 8.620             | 98.710            | 1.020             | 3038.0704         |                                                              |
| 7    | decimal(16,2) | totalValueTrade  | 成交总金额                       | 147785227.00      | 12428526.00       | 1021989.00        | 36643183122.70    |                                                              |
| 8    | decimal(11,3) | highestPrice     | 最高价                           | 8.720             | 98.740            | 1.027             | 3065.8221         |                                                              |
| 9    | decimal(11,3) | lowestPrice      | 最低价                           | 8.590             | 98.610            | 1.019             | 3035.7931         |                                                              |
| 10   | decimal(11,3) | nowPrice         | 最新价                           | 8.690             | 98.690            | 1.027             | 3064.9989         |                                                              |
| 11   | decimal(11,3) | buyPrice1        | 申买价一                         | 8.680             | 98.690            | 1.026             |                   |                                                              |
| 12   | decimal(11,3) | sellPrice1       | 申卖价一                         | 8.690             | 98.740            | 1.027             |                   |                                                              |
| 13   | decimal(16,0) | totalVolumeTrade | 成交数量                         | 17061217          | 12591             | 1000000           | 26814044          |                                                              |
| 14   | decimal(8,3)  | pe               | 市盈率，恒值为空                 |                   |                   |                   |                   |                                                              |
| 15   | decimal(12,0) | buyVolume1       | 申买量一                         | 103569            | 148               | 473300            |                   |                                                              |
| 16   | decimal(11,3) | buyPrice2        | 申买价二                         | 8.670             | 98.680            | 1.025             |                   |                                                              |
| 17   | decimal(12,0) | buyVolume2       | 申买量二                         | 109400            | 33                | 996700            |                   |                                                              |
| 18   | decimal(11,3) | buyPrice3        | 申买价三                         | 8.660             | 98.670            | 1.024             |                   |                                                              |
| 19   | decimal(12,0) | buyVolume3       | 申买量三                         | 59800             | 786               | 677500            |                   |                                                              |
| 20   | decimal(12,0) | sellVolume1      | 申卖量一                         | 26000             | 379               | 647100            |                   |                                                              |
| 21   | decimal(11,3) | sellPrice2       | 申卖价二                         | 8.700             | 98.750            | 1.028             |                   |                                                              |
| 22   | decimal(12,0) | sellVolume2      | 申卖量二                         | 42000             | 50                | 1010200           |                   |                                                              |
| 23   | decimal(11,3) | sellPrice3       | 申卖价三                         | 8.710             | 98.760            | 1.029             |                   |                                                              |
| 24   | decimal(12,0) | sellVolume3      | 申卖量三                         | 236600            | 100               | 591900            |                   |                                                              |
| 25   | decimal(11,3) | buyPrice4        | 申买价四                         | 8.650             | 98.660            | 1.023             |                   |                                                              |
| 26   | decimal(12,0) | buyVolume4       | 申买量四                         | 237600            | 29                | 31800             |                   |                                                              |
| 27   | decimal(11,3) | buyPrice5        | 申买价五                         | 8.640             | 98.650            | 1.022             |                   |                                                              |
| 28   | decimal(12,0) | buyVolume5       | 申买量五                         | 74000             | 9                 | 2200              |                   |                                                              |
| 29   | decimal(11,3) | sellPrice4       | 申卖价四                         | 8.720             | 98.790            | 1.030             |                   |                                                              |
| 30   | decimal(12,0) | sellVolume4      | 申卖量四                         | 322400            | 116               | 101500            |                   |                                                              |
| 31   | decimal(11,3) | sellPrice5       | 申卖价五                         | 8.730             | 98.800            | 1.031             |                   |                                                              |
| 32   | decimal(12,0) | sellVolume5      | 申卖量五                         | 152500            | 1126              | 20800             |                   |                                                              |
| 33   | string        | mdStreamId       | 行情数据类型                     | MD002             | MD003             | MD004             | MD001             | 参考数据类别                                                 |
| 34   | decimal(11,3) | closePrice       | 今日收盘价                       | 0.000             | 0.000             | 0.000             | 0.0000            |                                                              |
| 35   | string        | tradingPhaseCode | 产品所处的交易阶段代码           | T111              | T111              | T111              | T                 | "第0位：'P'表示停牌 'C'开盘集合竞价'T'连续竞价 详细解释：第 0 位：     S=启动（开市前）（深圳、上海）     O=开盘集合竞价（深圳、上海的C）     T=连续竞价（深圳、上海）     B=休市（深圳、上海）     C=收盘集合竞价（深圳）     E=已闭市（深圳、上海）     H=临时停牌（深圳、上海的P）     A=盘后交易（深圳）     V=波动性中断（深圳）     M=可恢复交易的熔断时段（上海）     N=不可恢复交易的熔断时段（上海）     D=开盘集合竞价阶段结束到连续竞价阶段开始之前的时段（上海）第 1 位：     0=正常状态（深圳，上海的1）     1=全天停牌（深圳） |
| 36   | string        | timestampOfDay   | 时间戳,HH:MM:SS.000              | 10:00:00.170      | 09:55:47.410      | 09:59:42.900      | 09:59:59.800      |                                                              |
| 37   | bigint        | time_stamp       | 时间戳,timestamp                 | 1528941600170     | 1528941347410     | 1528941582900     | 1528941599800     |                                                              |
| 38   | decimal(11,3) | preCloseIOPV     | 基金T-1日收盘时刻IOPV            |                   |                   | 0.000             |                   |                                                              |
| 39   | decimal(11,3) | iopv             | 基金IOPV                         |                   |                   | 0.000             |                   |                                                              |
| 40   | biging        | dw_trade_date    | 分区字段，日期                   |                   |                   |                   |                   |                                                              |

### 上交所证券信息表db_quotation.tb_level1_security_info_shanghai

| 序号 | 字段类型      | 字段名称             | 中文解释             | 股票举例      | 国债举例      | 基金举例      |      |                                                              |
| ---- | ------------- | -------------------- | -------------------- | ------------- | ------------- | ------------- | ---- | ------------------------------------------------------------ |
| 1    | String        | securityId           | 证券代码             | 600031        | 010303        | 501029        |      |                                                              |
| 2    | String        | isin                 | ISIN代码             |               |               |               |      |                                                              |
| 3    | String        | time                 | 记录更新时间HH:MM:SS | 17:30:44      | 17:30:44      | 17:30:44      |      |                                                              |
| 4    | String        | symbol               | 中文证券名称         | 三一重工      | 03国债⑶       | 红利基金      |      |                                                              |
| 5    | String        | englishSymbol        | 英文证券名称         |               |               |               |      |                                                              |
| 6    | String        | code                 | 基础证券代码         |               |               |               |      |                                                              |
| 7    | String        | marketType           | 市场种类             | ASHR          | ASHR          | ASHR          |      |                                                              |
| 8    | String        | category             | 证券类别             | ES            | D             | EU            |      |                                                              |
| 9    | String        | subCategory          | 证券子类别           | ASH           | GBF           | LOF           |      |                                                              |
| 10   | String        | currencyType         | 货币种类             | CNY           | CNY           | CNY           |      |                                                              |
| 11   | decimal(11,3) | price                | 面值                 | 0.000         | 100.000       | 0.000         |      |                                                              |
| 12   | Bigint        | countOffMarket       | 可流通证券未上市数量 |               |               |               |      |                                                              |
| 13   | String        | lastTradeDate        | 最后交易日期YYYYMMDD |               |               |               |      |                                                              |
| 14   | Bigint        | openDate             | 上市日期             | 1212595200000 | 1212595200000 | 1486915200000 |      |                                                              |
| 15   | Bigint        | setNo                | 产品集SET编号        | 4             | 4             | 6             |      |                                                              |
| 16   | Bigint        | buyCountUnit         | 买数量单位           | 100           | 1             | 100           |      |                                                              |
| 17   | Bigint        | sellCountUnit        | 卖数量单位           | 1             | 1             | 1             |      |                                                              |
| 18   | Bigint        | applyCountMin        | 申报数量下限         | 1             | 1             | 1             |      |                                                              |
| 19   | Bigint        | applyCountMax        | 申报数量上限         | 1000000       | 100000        | 1000000       |      |                                                              |
| 20   | decimal(11,3) | previousClosePrice   | 前收盘价格           | 8.680         | 98.700        | 1.022         |      |                                                              |
| 21   | decimal(11,3) | priceUnit            | 价格档位             | 0.010         | 0.010         | 0.001         |      |                                                              |
| 22   | String        | priceLimitType       | 涨跌幅限制类型       | N             | R             | N             |      |                                                              |
| 23   | decimal(11,3) | riseLimitPrice       | 涨幅上限价格         | 9.550         | 108.570       | 1.124         |      |                                                              |
| 24   | decimal(11,3) | fallLimitPrice       | 跌幅下限价格         | 7.810         | 88.830        | 0.920         |      |                                                              |
| 25   | decimal(17,6) | exRightRatio         | 除权比例             | 0.000000      | 0.000000      | 0.000000      |      |                                                              |
| 26   | decimal(17,6) | exDividendsAmount    | 除息金额             | 0.020000      | 0.000000      | 0.030000      |      |                                                              |
| 27   | String        | marginTradingSubject | 融资标的标志         | T             | F             | F             |      |                                                              |
| 28   | String        | shortSellingSubject  | 融券标的标志         | T             | F             | F             |      | /**         该字段为20位字符串，每位表示允许对应的业务，无定义则填空格。         第0位对应：‘N’表示首日上市。         第1位对应：‘D’表示除权。         第2位对应：‘R’表示除息。         第3位对应：’D’表示国内主板正常交易产品，’S’表示股票风险警示产品，’P’表示退市整理产品，’T’表示退市转让产品，’U’表示优先股产品。         第4位不启用。         第5位对应：’L’表示债券投资者适当性要求类，’M’表示债券机构投资者适当性要求类。         */ |
| 29   | String        | status               | 产品状态标志         | D             | D             | D             |      | 第0位第1位：'D' 是否除权，是第2位：'R' 是否除息，是第3位：'S' 是否风险警示产品，是             'P' 是否退市整理产品，是 |
| 30   | String        | remark               | 备注                 |               |               |               |      |                                                              |

### 深交所实时行情db_quotation.tb_level1_realtime_shenzhen

| 序号 | 字段类型      | 字段名称         | 中文解释                                                     | 股票举例          | 债券举例          | 基金举例          | 指数举例          | 成交量举例        | 港股举例          | 盘后交易举例      | 备注                                                         |
| ---- | ------------- | ---------------- | ------------------------------------------------------------ | ----------------- | ----------------- | ----------------- | ----------------- | ----------------- | ----------------- | ----------------- | ------------------------------------------------------------ |
| 1    | string        | date_time        | 当前时间,格式为yyyyMMddHHmmssSSS                             | 20180614100000000 | 20180614100000000 | 20180614095918000 | 20180614100000000 | 20180614100000000 | 20180614100003000 | 20180614150500000 |                                                              |
| 2    | string        | remarked         | 特殊标记,恒值为空                                            |                   |                   |                   |                   |                   |                   |                   |                                                              |
| 3    | string        | securityId       | 证券代码                                                     | 000001            | 100303            | 160119            | 399001            | 395001            | 00001             | 000001            |                                                              |
| 4    | string        | symbol           | 证券简称,恒值为空,值在证券信息中                             |                   |                   |                   |                   |                   |                   |                   |                                                              |
| 5    | decimal(11,3) | prevClosePrice   | 昨日收盘价                                                   | 9.95              | 98.67             | 1.4               | 10161.6484        | 0                 | 89.5              | 9.95              |                                                              |
| 6    | decimal(11,3) | openPrice        | 今日开盘价                                                   | 9.95              | 98.453            | 1.393             | 10124.7628        |                   | 89.15             |                   | 港股中，此项表示Price 按盘价，按盘价，是港股的特殊交易方式，通过委托而不是成交计算出按盘价 |
| 7    | decimal(11,3) | nowPrice         | 最新价                                                       | 10.12             | 98.666            | 1.409             | 10208.0739        | 463               | 89.15             |                   | 成交量类型数据中，此项表示某类股票数量。                     |
| 8    | decimal(16,0) | totalVolumeTrade | 成交数量                                                     | 28301034          | 630               | 13400             | 1344992378        | 1025227524        | 555770            | 0                 |                                                              |
| 9    | decimal(17,3) | totalValueTrade  | 成交总金额                                                   | 284674939.94      | 62146.71          | 18722.6           | 17968246190.48    | 11362926687.25    | 49541403.124      | 0                 |                                                              |
| 10   | decimal(16,0) | numTrades        | 成交笔数                                                     | 7985              | 41                | 12                | 966291            | 628416            | 0                 | 0                 |                                                              |
| 11   | decimal(11,3) | highestPrice     | 最高价                                                       | 10.15             | 98.695            | 1.409             | 10213.7923        |                   | 89.6              |                   |                                                              |
| 12   | decimal(11,3) | lowestPrice      | 最低价                                                       | 9.92              | 98.453            | 1.393             | 10108.9241        |                   | 88.9              |                   |                                                              |
| 13   | decimal(7,2)  | pe1              | 市盈率1，恒值为空                                            |                   |                   |                   |                   |                   |                   |                   |                                                              |
| 14   | decimal(7,2)  | pe2              | 市盈率2，恒值为空                                            |                   |                   |                   |                   |                   |                   |                   |                                                              |
| 15   | decimal(9,3)  | priceChange1     | 价格升跌1，恒值为空                                          |                   |                   |                   |                   |                   |                   |                   |                                                              |
| 16   | decimal(9,3)  | priceChange2     | 价格升跌2，恒值为空                                          |                   |                   |                   |                   |                   |                   |                   |                                                              |
| 17   | decimal(12,0) | contractHold     | 合约持仓量，恒值为空                                         |                   |                   |                   |                   |                   |                   |                   |                                                              |
| 18   | decimal(11,3) | sellPrice5       | 申卖价五                                                     | 10.17             | 98.694            | 1.415             |                   |                   |                   |                   |                                                              |
| 19   | decimal(12,0) | sellVolume5      | 申卖量五                                                     | 23590             | 2                 | 1420              |                   |                   |                   |                   |                                                              |
| 20   | decimal(11,3) | sellPrice4       | 申卖价四                                                     | 10.16             | 98.693            | 1.414             |                   |                   |                   |                   |                                                              |
| 21   | decimal(12,0) | sellVolume4      | 申卖量四                                                     | 42090             | 1                 | 300               |                   |                   |                   |                   |                                                              |
| 22   | decimal(11,3) | sellPrice3       | 申卖价三                                                     | 10.15             | 98.692            | 1.411             |                   |                   |                   |                   |                                                              |
| 23   | decimal(12,0) | sellVolume3      | 申卖量三                                                     | 110153.5          | 3                 | 500               |                   |                   |                   |                   |                                                              |
| 24   | decimal(11,3) | sellPrice2       | 申卖价二                                                     | 10.14             | 98.691            | 1.41              |                   |                   |                   |                   |                                                              |
| 25   | decimal(12,0) | sellVolume2      | 申卖量二                                                     | 63500.6           | 1                 | 80                |                   |                   |                   |                   |                                                              |
| 26   | decimal(11,3) | sellPrice1       | 申卖价一                                                     | 10.13             | 98.667            | 1.409             |                   |                   | 850               | 10.07             |                                                              |
| 27   | decimal(12,0) | sellVolume1      | 申卖量一                                                     | 4000              | 1                 | 1450              |                   |                   | 850               |                   |                                                              |
| 28   | decimal(11,3) | buyPrice1        | 申买价一                                                     | 10.12             | 98.625            | 1.4               |                   |                   | 89.15             | 10.07             |                                                              |
| 29   | decimal(12,0) | buyVolume1       | 申买量一                                                     | 27520             | 3                 | 110               |                   |                   | 650               |                   |                                                              |
| 30   | decimal(11,3) | buyPrice2        | 申买价二                                                     | 10.11             | 98.624            | 1.395             |                   |                   |                   |                   |                                                              |
| 31   | decimal(12,0) | buyVolume2       | 申买量二                                                     | 18910             | 2                 | 870               |                   |                   |                   |                   |                                                              |
| 32   | decimal(11,3) | buyPrice3        | 申买价三                                                     | 10.1              | 98.623            | 1.394             |                   |                   |                   |                   |                                                              |
| 33   | decimal(12,0) | buyVolume3       | 申买量三                                                     | 65339.3           | 3                 | 4210              |                   |                   |                   |                   |                                                              |
| 34   | decimal(11,3) | buyPrice4        | 申买价四                                                     | 10.09             | 98.622            | 1.393             |                   |                   |                   |                   |                                                              |
| 35   | decimal(12,0) | buyVolume4       | 申买量四                                                     | 5230              | 1                 | 1250              |                   |                   |                   |                   |                                                              |
| 36   | decimal(11,3) | buyPrice5        | 申买价五                                                     | 10.08             | 98.621            | 1.39              |                   |                   |                   |                   |                                                              |
| 37   | decimal(12,0) | buyVolume5       | 申买量五                                                     | 10090             | 3                 | 90                |                   |                   |                   |                   |                                                              |
| 38   | bigint        | numMdEntries     | 行情条目个数                                                 | 19                | 18                | 19                | 5                 |                   | 6                 | 2                 |                                                              |
| 39   | decimal(11,3) | limitUpPrice     | 涨停价格                                                     | 10.95             | 999999999.9999    | 1.54              |                   |                   | 0.0000            |                   |                                                              |
| 40   | decimal(11,3) | limitDownPrice   | 跌停价格,价格不可以为负数的证券，1000表示无跌停下限,给其赋值0.000000 | 8.96              | 0.001             | 1.26              |                   |                   | 0.0000            |                   |                                                              |
| 41   | decimal(11,3) | bP               | 加权平均价涨跌BP                                             | 0.0000            | 0.0000            | 0.0000            |                   |                   | 0                 |                   | 港股中，此项表示noComplexEventTimes。VCM 冷静期个数0或11 表示当前处于触发 VCM 的 冷静期，下面的时间是冷静期 的开始结束时间 |
| 42   | decimal(11,3) | bPPrice          | 加权平均价格                                                 | 9.92              | 98.453            | 1.393             |                   |                   | 0.0000            |                   | 港股中，此项表示referencePrice，参考价                       |
| 43   | string        | messageType      | 消息类型                                                     | 300111            | 300111            | 300111            | 309011            | 309111            | 306311            | 300611            | int STOCK_SNAPSHOT = 300111;//集中竞价行情快照int AFTER_HOURS_SNAPSHOT = 300611;//盘后定价行情快照int INDEX_SNAPSHOT = 309011;//指数行情快照int HK_SNAPSHOT = 306311;//港股实时行情快照int VOLUME_STATISTICS = 309111;//成交量统计指标行情快照 |
| 44   | string        | channelNo        | 频道代码                                                     | 1012              | 1032              | 1024              | 10                | 10                | 5001              | 3001              |                                                              |
| 45   | string        | mdStreamId       | 行情数据类型                                                 | 010               | 010               | 010               | 900               | 910               | 630               | 060               | 010 现货(股票，基金，债券等)集中竞价交易快 照行情020 质押式回购交易快照行情030 债券分销快照行情040 期权集中竞价交易快照行情060 以收盘价交易的盘后定价交易快照行情061 以成交量加权平均价交易的盘后定价交易快 照行情630 港股实时行情900 指数快照行情910 成交量统计指标快照行情 |
| 46   | string        | securityIdSource | 证券代码源                                                   | 102               | 102               | 102               | 102               | 102               | 103               | 102               | 证券代码源102=深圳证券交易所103=香港交易所                   |
| 47   | string        | tradingPhaseCode | 产品所处的交易阶段代码                                       | T0                | T0                | T0                | T                 | T                 | T0                | A0                | * 产品所处的交易阶段代码 第 0 位： S=启动（开市前） O=开盘集合竞价 T=连续竞价 B=休市 C=收盘集合竞价 E=已闭市 H=临时停牌 A=盘后交易 V=波动性中断  第 1 位： 0=正常状态 1=全天停牌 |

### 深交所证券信息表db_quotation.tb_level1_security_info_shenzhen

| 序号 | 字段类型      | 字段名称                   | 中文解释                       | 股票举例       | 债券举例      | 基金举例         |      |      |      |      |                                                              |
| ---- | ------------- | -------------------------- | ------------------------------ | -------------- | ------------- | ---------------- | ---- | ---- | ---- | ---- | ------------------------------------------------------------ |
| 1    | String        | securityId                 | 证券代码                       | 000001         | 100303        | 160119           |      |      |      |      |                                                              |
| 2    | String        | securityIdSource           | 产品所处的交易阶段代码         | 102            | 102           | 102              |      |      |      |      |                                                              |
| 3    | String        | symbol                     | 证券简称                       | 平安银行       | 国债0303      | 南方500          |      |      |      |      |                                                              |
| 4    | String        | englishName                | 英文名字                       | PAB            |               | SOUTHERN CIS 500 |      |      |      |      |                                                              |
| 5    | String        | isin                       | ISIN代码                       | CNE000000040   |               | CNE100000J83     |      |      |      |      |                                                              |
| 6    | String        | underlyingSecurityId       | 基础证券代码                   | 000001         | 100303        | 160119           |      |      |      |      |                                                              |
| 7    | String        | underlyingSecurityIdSource | 基础证券代码源                 | 102            | 102           | 102              |      |      |      |      |                                                              |
| 8    | BigInt        | listDate                   | 上市日期                       | 663091560000   | 1137427800000 | 1231603860000    |      |      |      |      |                                                              |
| 9    | String        | securityType               | 证券类别                       | 1              | 5             | 23               |      |      |      |      | `主板 A 股 1 中小板股票 2 创业板股票 3 主板 B 股 4 国债（含地方债） 5 企业债 6 公司债 7 可转债 8 私募债 9 可交换私募债 10 证券公司次级债 11 质押式回购 12 资产支持证券 13 本市场股票 ETF 14 跨市场股票 ETF 15 跨境 ETF 16 本市场实物债券 ETF 17 现金债券 ETF 18 黄金 ETF 19 货币 ETF 20 杠杆 ETF 21（预留） 商品期货 ETF 22 标准 LOF 23 分级子基金 24 封闭式基金 25 仅申赎基金 26 权证 28 个股期权 29 ETF 期权 30 优先股 33 证券公司短期债 34 可交换公司债 35` |
| 10   | String        | currency                   | 货币种类                       | CNY            | CNY           | CNY              |      |      |      |      |                                                              |
| 11   | decimal(12,4) | qtyUnit                    | 数量单位                       | 1.00           | 1.00          | 1.00             |      |      |      |      |                                                              |
| 12   | String        | dayTrading                 | 是否支持当日回转交易           | N              | Y             | N                |      |      |      |      |                                                              |
| 13   | String        | statusList                 |                                | []             | []            | []               |      |      |      |      | 这是一个字符串，将Array 墙砖字符串/** * 证券状态代码: * 1-停牌 * 2-除权 * 3-除息 * 4-ST * 5-*ST * 6-上市首日 * 7-公司再融资 * 8-恢复上市首日 * 9-网络投票 * 10-退市整理期 * 12-增发股份上市 * 13-合约调整 * 14-暂停上市后协议转让 */SUSPENSION = 1;//停牌XR = 2;//除权DR = 3;//除息ST = 4;//STXST = 5;//*STDELISTING = 10;//退市整理期 |
| 14   | decimal(12,4) | preClosePx                 | 昨日收盘价格                   | 9.9500         | 98.6700       | 1.4000           |      |      |      |      |                                                              |
| 15   | decimal(16,2) | outstandingShare           | 总发行量                       | 17170411366.00 | 260000000.00  | 38988871.00      |      |      |      |      |                                                              |
| 16   | decimal(16,2) | publicFloatShareQuantity   | 流通股数                       | 17170246773.00 | 29000550.00   | 38988871.00      |      |      |      |      |                                                              |
| 17   | decimal(12,4) | parValue                   | 面值                           | 1.0000         | 100.0000      | 1.0000           |      |      |      |      |                                                              |
| 18   | String        | gageFlag                   | 是否可作为两融可冲抵保证金证券 | Y              | Y             | Y                |      |      |      |      |                                                              |
| 19   | decimal(12,4) | gageRatio                  | 可冲抵保证金折算率             | 0.00           | 0.00          | 0.00             |      |      |      |      |                                                              |
| 20   | String        | crdBuyUnderlying           | 是否为融资标示                 | Y              | N             | N                |      |      |      |      |                                                              |
| 21   | String        | crdSellUnderlying          | 是否为融券标示                 | Y              | N             | N                |      |      |      |      |                                                              |
| 22   | String        | priceCheckMode             | 提价检查方式                   | 1              |               |                  |      |      |      |      |                                                              |
| 23   | String        | pledgeFlag                 | 是否可质押入库                 | N              | Y             | Y                |      |      |      |      |                                                              |
| 24   | decimal(12,4) | contractMultiplier         | 回购标准券折算率               |                | 0.9600        | 0.0000           |      |      |      |      |                                                              |
| 25   | String        | regularShare               | 对应回购标准券                 |                | 131990        | 131990           |      |      |      |      |                                                              |
| 26   | String        | qualificationFlag          | 投资者适当性管理标示           | N              | N             | N                |      |      |      |      |                                                              |
| 27   | BigInt        | qualificationClass         | 投资者适当性管理分类           | 0              | 0             | 0                |      |      |      |      |                                                              |
| 28   | String        | industryClassification     | 行业种类                       | J66            |               |                  |      |      |      |      |                                                              |
| 29   | decimal(12,4) | previousYearProfitPerShare | 上年每股利润                   | 1.3000         |               |                  |      |      |      |      |                                                              |
| 30   | decimal(12,4) | currentYearProfitPerShare  | 本年每股利润                   | 0.0000         |               |                  |      |      |      |      |                                                              |
| 31   | String        | offeringFlag               | 是否处于要约收回购期           | N              | N             |                  |      |      |      |      |                                                              |
| 32   | decimal(12,4) | nav                        | 日基金净值                     |                |               | 1.3935           |      |      |      |      |                                                              |
| 33   | decimal(12,4) | couponRate                 | 票面年利率                     |                | 0.0340        |                  |      |      |      |      |                                                              |
| 34   | decimal(12,4) | issuePrice                 | 贴现发行价                     |                | 100.0000      |                  |      |      |      |      |                                                              |
| 35   | decimal(16,8) | interest                   | 每百元应记利息                 |                | 0.54958904    |                  |      |      |      |      |                                                              |
| 36   | Bigint        | interestAccrualDate        | 起息日                         |                | 1516118640000 |                  |      |      |      |      |                                                              |
| 37   | Bigint        | maturityDate               | 到期日                         |                | 1673885040000 |                  |      |      |      |      |                                                              |

### 深交所指数信息表db_quotation.tb_level1_index_info_shenzhen

| 序号 | 字段类型      | 字段名称         | 中文解释               | 指数举例             |      |      |      |      |      |      |      |
| ---- | ------------- | ---------------- | ---------------------- | -------------------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| 1    | String        | securityId       | 证券代码               | 399001               |      |      |      |      |      |      |      |
| 2    | String        | securityIdSource | 产品所处的交易阶段代码 | 102                  |      |      |      |      |      |      |      |
| 3    | String        | symbol           | 简称                   | 深证成指             |      |      |      |      |      |      |      |
| 4    | String        | englishName      | 英文名称               | SZSE COMPONENT INDEX |      |      |      |      |      |      |      |
| 5    | String        | currency         | 货币                   | CNY                  |      |      |      |      |      |      |      |
| 6    | decimal(16,5) | prevCloseIdx     | 前盘指数               | 10161.64840          |      |      |      |      |      |      |      |