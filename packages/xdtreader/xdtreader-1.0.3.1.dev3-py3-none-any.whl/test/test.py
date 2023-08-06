import pandas as pd
import wget
from tools.conn import *
from tools.str import *
from urllib.request import urlopen


def ExchangeType(df=None):
    data = pd.DataFrame(
        columns=['Contract', 'Date', 'Presettle', 'Open', 'High', 'Low', 'Close', 'Settle', 'ch1', 'ch2', 'Volume',
                 'Amount', 'OI', 'OIch', 'Delta', 'IV', 'EA'])
    # df = pd.read_excel("./test/202108.xls", header=3, dtype={'Date':str})
    df = df[:len(df) - 5]
    df['Contract'] = df['Contract'].fillna(method='ffill')

    # df = df.apply(pd.to_numeric, errors='ignore')
    df.Date = df.Date.apply(pd.to_datetime, errors='ignore')

    try:
        data['Contract'] = df['Contract']
        data['Date'] = df['Date']
        data['Presettle'] = df['Pre settle']
        data['Open'] = df['Open']
        data['High'] = df['High']
        data['Low'] = df['Low']
        data['Close'] = df['Close']
        data['Settle'] = df['Settle']
        data['ch1'] = df['ch1']
        data['ch2'] = df['ch2']
        data['Volume'] = df['Volume']

        data['Amount'] = df['Amount']
        data['OI'] = df['OI']
    except Exception as e:
        print(e)

    # data['Date'] = df['Date']
    # data['Presettle']=  pd.DataFrame(convert_currency(pd.DataFrame(df['Presettle'])))

    # data['Open'] =      pd.DataFrame(convert_currency(pd.DataFrame(df['今开盘'])))
    # data['High'] =      pd.DataFrame(convert_currency(pd.DataFrame(df['最高价'])))
    # data['Low']=        pd.DataFrame(convert_currency(pd.DataFrame(df['最低价'])))
    # data['Close'] =     pd.DataFrame(convert_currency(pd.DataFrame(df['今收盘'])))

    # data['Settle'] =    pd.DataFrame(convert_currency(pd.DataFrame(df['今结算'])))

    # df['涨跌1'] = pd.Series(df['涨跌1'])
    # df['涨跌2'] = pd.Series(df['涨跌2'])
    # data['ch1'] =       pd.DataFrame(convert_currency(pd.DataFrame(df['涨跌1'])))
    # data['ch2'] =       pd.DataFrame(convert_currency(pd.DataFrame(df['涨跌2'])))
    # data['Volume']=     pd.DataFrame(convert_currency(pd.DataFrame(df['成交量(手)'])))
    # data['Amount'] =    pd.DataFrame(convert_currency(pd.DataFrame(df['成交额(万元)'])))

    # data['OIch'] =      pd.DataFrame(convert_currency(pd.DataFrame(df['增减量'])))
    # 'Delta','IV','EA'

    try:
        data['OIch'] = df['OIch']
        data['Delta'] = pd.DataFrame(convert_currency(pd.DataFrame(df['DELTA'])))
        data['IV'] = pd.DataFrame(convert_currency(pd.DataFrame(df['隐含波动率'])))
        data['EA'] = pd.DataFrame(convert_currency(pd.DataFrame(df['行权量'])))

    except Exception as e:
        print(e)
        data['OIch'] = 0
        data['Delta'] = 0
        data['IV'] = 0
        data['EA'] = 0

    return data
    # SaveToSql(dk,'czce')


def shfeFutures(start=2020, end=2021):
    all = pd.DataFrame()
    for year in range(start, end + 1):
        for month in range(1, 13):
            if year > 2020 and month < 10: month = '0' + str(month)
            filename = '所内合约行情报表%s.%s.xls' % (year, month)
            print(filename)
            df = pd.read_excel(filename, header=3, dtype={'Date': str})
            df = ExchangeType(df)
            print(df.shape)
            # SaveToSql(df, 'czcefutures%s'%year)
            print(df.tail())
            SaveToSql(df, 'shfefutures')


def run():
    # CzceOpt(start=2017,end=2020)
    shfeFutures(start=2021, end=2021)
    # test()
    # urldown("https://www.python.org")


if __name__ == '__main__':
    run()
