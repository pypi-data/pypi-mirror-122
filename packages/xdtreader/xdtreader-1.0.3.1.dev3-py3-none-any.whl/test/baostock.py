import akshare as ak
import numpy as np
import pandas as pd
import time

### 第一步_获取所有股票的代码

# 深证A指
all_sz = ak.stock_info_sz_name_code(indicator="A股列表")
# 上证指数
all_sh1 = ak.stock_info_sh_name_code(indicator="主板A股")
all_sh2 = ak.stock_info_sh_name_code(indicator="主板B股")
# 次新股
all_new = ak.stock_zh_a_new()

df1 = 'sz' + all_sz.A股代码
df2 = 'sh' + all_sh1.COMPANY_CODE
df3 = 'sh' + all_sh2.COMPANY_CODE
df4 = all_new.symbol

t1 = np.array(df1)
t2 = np.array(df2)
t3 = np.array(df3)
t4 = np.array(df4)

stock_sz = np.hstack([t1, 'sz399107'])
stock_sh = np.hstack([t2, t3, 'sh000001'])
stock_new = t4

stock_item = {'深证A指': stock_sz, '上证指数': stock_sh}
stock_item = {'次新股': stock_new}

print(stock_item)
