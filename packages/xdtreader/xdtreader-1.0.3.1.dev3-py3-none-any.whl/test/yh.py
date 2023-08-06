import datetime
import pandas_datareader.data as web


def a():
    start = datetime.datetime(2015, 1, 1)  # 获取数据的时间段-起始时间
    end = datetime.date.today()  # 获取数据的时间段-结束时间
    stock = web.DataReader("600797.SS", "yahoo", start, end)  # 获取浙大网新2017年1月1日至今的股票数据

    # df=pdr.get_data_yahoo('600001.SS',s)
    print(stock)


def b():
    import akshare as ak
    stock_zh_a_hist_min_em_df = ak.stock_zh_a_hist_min_em(symbol="000001", period='5', adjust='',
                                                          start_date="2021-05-01 09:32:00",
                                                          end_date="2021-09-06 09:32:00")
    print(stock_zh_a_hist_min_em_df)


if __name__ == '__main__':
    # a()
    b()
