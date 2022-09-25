import datetime

import akshare as ak
import pandas as pd
import json
import sys
import datetime as dt

pd.set_option('display.max_rows', None)

print("正在初始化")

data = ak.fund_open_fund_daily_em()
all_put = 0.0
all_last = 0.0

path = sys.argv[0][:-5]
selected_fund_id = -1


class Tools:
    @staticmethod
    def file_writer(filepath, info, mode):
        """
        :param filepath: 写入的文件路径
        :param info: 写入的信息
        :param mode: 写入模式，0新增，1覆写
        :return: 无
        """
        pass

    @staticmethod
    def file_reader(filepath, mode):
        pass

    @staticmethod
    def change_percent_to_float(p: str):
        return float(p.strip('%')) / 100


class SourceTool:

    @staticmethod
    def get_fund(fund_code: str):
        return ak.fund_open_fund_info_em(fund_code)

    @staticmethod
    def get_fund_name(fund_code: str):
        return data.loc[data[data['基金代码'] == str(fund_code)].index, ['基金简称']].iloc[0, 0]

    @staticmethod
    def get_fund_fare(fund_code: str):
        return Tools.change_percent_to_float(
            data.loc[data[data['基金代码'] == str(fund_code)].index, ['手续费']].iloc[0, 0])


class Fund:
    name = ""
    info = ""
    fare = 0.0
    put = 0.0
    last = 0.0
    # TODO 卖出手续费
    under_seven_money = []
    under_thirty_money = []
    under_one_hundred_eighty_money = []
    no_fare_money = []

    code = ""
    control_info = []
    day_money_info = []
    start_date = datetime.date.today()

    def __init__(self, fund_code):
        self.info = SourceTool.get_fund(fund_code)
        self.name = SourceTool.get_fund_name(fund_code)
        self.fare = SourceTool.get_fund_fare(fund_code)
        self.code = fund_code

    def get_date_control_money(self, date: datetime.date):
        for i in self.control_info:
            if i[0] == date:
                return i[1]
            return 0

    def get_fund_date_net_value(self, date: datetime.date):
        return self.info.loc[self.info[self.info['净值日期'] == date].index, ['单位净值']].iloc[0, 0]

    def calc_day_money_info(self, d):
        # TODO 初始化d当天
        i = [
            self.start_date,  # d当天
            (self.control_info[0][1] if len(self.control_info) > 0 else 0),#
            (self.control_info[0][1] if len(self.control_info) > 0 else 0),
            0,
            0,
            0
        ]


'''         for i in range(1, len(self.info) - self.info[self.info['净值日期'] == self.start_date].index):
            today = self.info.loc[self.info[self.info['净值日期'] == self.start_date].index + i, ['净值日期']].iloc[
                0, 0]
            if self.get_date_control_money(today) > 0:
                z = self.get_date_control_money(today) * self.fare/100
            else:
                # TODO 卖出手续费
                pass
            self.day_money_info.append([
                today,
                self.day_money_info[i - 1][1] + self.get_date_control_money(today) - z,
                self.day_money_info[i - 1][2] / self.get_fund_date_net_value(
                    self.day_money_info[i - 1][0]) * self.get_fund_date_net_value(today),
                self.day_money_info[i - 1][2] / self.get_fund_date_net_value(
                    self.day_money_info[i - 1][0]) * self.get_fund_date_net_value(today) - self.day_money_info[i - 1][
                    2],
                self.info.loc[self.info[self.info['净值日期'] == today].index, ['日增长率']].iloc[0, 0],
                self.day_money_info[i - 1][2] / self.get_fund_date_net_value(
                    self.day_money_info[i - 1][0]) * self.get_fund_date_net_value(today) - self.day_money_info[i - 1][
                    1] + self.get_date_control_money(today)
            ])
        self.put = self.day_money_info[len(self.day_money_info)-1][1]
        self.last = self.day_money_info[len(self.day_money_info)-1][2]'''

Funds = []


class Command:
    @staticmethod
    def add_fund():
        try:
            fund_code = input("请输入基金代码")
            Funds.append(Fund(fund_code))
            print("添加 " + SourceTool.get_fund_name(fund_code) + " 成功")
        except:
            print("请输入正确的基金代码")

    @staticmethod
    def list_fund():
        if len(Funds) == 0:
            print("当前未添加基金，请先添加新基金")
            raise Exception("当前未添加基金")
        else:
            count = 0
            for i in Funds:
                print(
                    str(count) +
                    " " +
                    i.name +
                    " 总投入:" +
                    str(i.put) +
                    "元 当前持有:" +
                    str(i.last) +
                    "元 利润:" +
                    str(i.last - i.put) +
                    "元 收益率:" +
                    (str((i.last - i.put) / i.put * 100) if i.put != 0 else "0") +
                    "%"
                )
                count += 1

    @staticmethod
    def select_fund():
        global selected_fund_id
        if selected_fund_id != -1:
            print("当前选择的基金是 " + Funds[selected_fund_id].name)

        print("请从已添加的基金列表中选择操作基金")
        try:
            Command.list_fund()
        except:
            return
        selected_id = int(input("请输入基金序号(非基金代码)"))
        if 0 <= selected_id < len(Funds):
            selected_fund_id = selected_id
            print("选择基金 " + Funds[selected_fund_id].name + " 成功")
        else:
            print("请输入一个存在的基金序号")

    @staticmethod
    def control_fund():
        global selected_fund_id
        if selected_fund_id != -1:
            print("当前选择的基金是 " + Funds[selected_fund_id].name)
        else:
            print("请先选择基金")
            return
        datey = int(input("请输入投资年(yyyy)"))
        datem = int(input("请输入投资月(mm)"))
        dated = int(input("请输入投资日(dd)"))
        try:
            date = datetime.date(datey, datem, dated)
            t = Funds[selected_fund_id].info.loc[
                Funds[selected_fund_id].info[Funds[selected_fund_id].info['净值日期'] == date].index, ['单位净值']
            ].iloc[0, 0]
        except Exception as e:
            print("输入的日期不合法，原因是:" + e)
            return

        money = float(input("请输入投资的金额(买入为正，卖出为负，按照购买日期当日净值计算)"))
        if date < Funds[selected_fund_id].start_date:
            if money > 0:
                Funds[selected_fund_id].start_date = date
                Funds[selected_fund_id].control_info.append((date, money))
                Funds[selected_fund_id].control_info.sort(key=lambda x: x[0])
                Funds[selected_fund_id].calc_day_money_info()
            else:
                print("投资金额不合法(最早的投资金额应该大于0)")
                return
        else:
            if Funds[selected_fund_id].day_money_info[(date - Funds[selected_fund_id].start_date).days][2] + money >= 0:
                Funds[selected_fund_id].control_info.append((date, money))
                Funds[selected_fund_id].control_info.sort(key=lambda x: x[0])
                Funds[selected_fund_id].calc_day_money_info()
            else:
                print("投资金额不合法(任何一天的结算金额都应该大于0)")
                return


def cmd(command: str):
    if command == 'h' or command == 'help':
        print("有如下命令：添加基金，列出添加的基金，操作基金，选择基金")
    elif command == '列出添加的基金':
        Command.list_fund()
    elif command == '添加基金':
        Command.add_fund()
    elif command == '选择基金':
        Command.select_fund()
    elif command == '操作基金':
        Command.control_fund()
    else:
        print("请输入正确的命令，帮助提示请输入help或者h")


def start():
    print("当前保存目录为" + path)
    print("初始化完成,等待命令中")


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    start()
    while True:
        try:
            cmd(input('>>>'))
        except:
            pass
