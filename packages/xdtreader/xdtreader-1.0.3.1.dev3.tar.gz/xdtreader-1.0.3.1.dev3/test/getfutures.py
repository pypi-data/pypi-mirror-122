import akshare as ak
from tools.conn import *


def getday():
    df = ak.get_cffex_rank_table()
    Date = '20210922'
    for item in df.keys():
        df[item]['Date'] = '%s' % Date
        print(df[item].tail())
        SaveToSql(df[item][:-1], '20')
    print(df.dt)


if __name__ == '__main__':
    getday()
