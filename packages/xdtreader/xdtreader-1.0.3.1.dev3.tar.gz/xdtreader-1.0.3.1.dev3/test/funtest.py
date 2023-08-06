import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import talib
import tushare as ts
from tools.conn import *
from tools.str import *
from tools.times import *


def Load_hdb_csv_sql(csvfile='20070104.csv'):
    # print(os.getcwd())
    df = pd.read_csv(csvfile,
                     converters={"date": lambda x: StringToDatetime(str(x))},
                     usecols=lambda x: len(x) > 1,
                     dtype={"variety": str})
    # print(df.columns[0])
    df = df.drop(columns=['Unnamed: 0'])
    # print(df.dtypes)
    print(df.shape)
    print(csvfile + '---->>>>>>|')
    return df
    # SaveToSql(df)


def Load_SubDir(subdirpath):
    filenames = []
    listdir(subdirpath, filenames)

    dfall = pd.DataFrame()
    for fileitem in filenames:
        df = Load_hdb_csv_sql(fileitem)

        # print(df.tail())
        dfall = dfall.append(df, ignore_index=True)
        print(dfall.shape)

        if dfall.shape[0] > 50000:
            try:
                callback = SaveToSql(dfall, 'akfutures')
                print(callback)
                dfall = pd.DataFrame()
            except Exception as e:
                print(e)


def Load_hdb_zip_sql(csvfile='cffex2021.zip'):
    # print(os.getcwd())

    df = pd.read_csv(csvfile,
                     compression="zip",
                     converters={"date": lambda x: StringToDatetime(str(x))},
                     usecols=lambda x: len(x) > 1,
                     dtype={"variety": str})
    # print(df.columns[0])
    df = df.drop(columns=['Unnamed: 0'])
    # print(df.dtypes)
    print(df.shape)
    print(csvfile + '---->>>>>>|')
    return df
    # SaveToSql(df)


def ziptest():
    from zipfile import ZipFile
    import pandas as pd
    myzip = ZipFile('cffex2021.zip')
    dfall = pd.DataFrame()
    print(myzip.namelist())
    num = 0
    for zipfile in myzip.namelist():
        f = myzip.open('%s' % zipfile)
        # df=pd.read_csv(f)
        df = pd.read_csv(f,
                         converters={"date": lambda x: StringToDatetime(str(x))},
                         usecols=lambda x: len(x) > 1,
                         dtype={"variety": str})
        df = df.drop(columns=['Unnamed: 0'])
        # print(df.shape)
        dfall = dfall.append(df, ignore_index=True)
        print(dfall.shape)
        num = num + 1
        print('%s->>>>>>>--%s->>>>>>' % (f.name, num))
        f.close()
    myzip.close()


if __name__ == '__main__':
    # Load_hdb_csv_sql()
    subdirpath = '.\\db\\'
    # Load_SubDir(subdirpath)
    # Load_hdb_zip_sql('cffex2021.zip')
    ziptest()
