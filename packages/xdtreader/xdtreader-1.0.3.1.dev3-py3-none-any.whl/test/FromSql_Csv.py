import pandas as pd
import time
from tools.conn import *
from tqdm import tqdm


def FuturesSql_Csv(exchange='cffex'):
    conn = GetLocalConn('hdb')
    sql = 'select distinct Contract from %sfutures' % exchange
    syms = pd.read_sql(sql, conn)

    print(syms.head())

    for sym in tqdm(syms['Contract']):
        try:
            sql = "select * from %sfutures where Contract='%s'" % (exchange, sym)
            # print(sql)
            # sql=sqlt
            df = pd.read_sql(sql, conn)
            csvname = './db/%s/%s.csv' % (exchange, sym)
            # print(csvname)
            df.to_csv(csvname, index=False)
            time.sleep(0.1)
        except Exception as e:
            print(e)


if __name__ == '__main__':

    for exchange in ['dce', 'ine', 'shfe']:
        try:
            FuturesSql_Csv(exchange)
        except Exception as e:
            print(e)
