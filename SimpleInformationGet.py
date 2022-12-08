import akshare as ak
import pandas as pd
import datetime as dt
import Tools
import time

start = time.time()
data = ak.fund_open_fund_daily_em()
end = time.time()
print(end-start)


class Source:
    # 获取基金净值实时数据
    @staticmethod
    def get_fund(fund_code: str):
        return ak.fund_open_fund_info_em(fund_code)

    # 通过基金代码获取基金名称
    @staticmethod
    def get_fund_name(fund_code: str):
        return data.loc[data[data['基金代码'] == str(fund_code)].index, ['基金简称']].iloc[0, 0]

    # 通过基金代码获取基金手续费百分比
    @staticmethod
    def get_fund_fare(fund_code: str):
        return Tools.change_percent_to_float(
            data.loc[data[data['基金代码'] == str(fund_code)].index, ['手续费']].iloc[0, 0])


if __name__ == '__main__':
    start = time.time()
    print(Source.get_fund_name('014207'))
    end = time.time()
    print(end-start)
