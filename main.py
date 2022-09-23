import akshare as ak
import pandas as pd
import json
import sys

pd.set_option('display.max_rows', None)

print("正在初始化")

data = ak.fund_open_fund_daily_em()
all_put = 0.0
all_last = 0.0
Funds = []
path = sys.argv[0][:-5]
selected_fund_code = ""


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
    code = ""

    def __init__(self, fund_code):
        self.info = SourceTool.get_fund(fund_code)
        self.name = SourceTool.get_fund_name(fund_code)
        self.fare = SourceTool.get_fund_fare(fund_code)
        self.code = fund_code


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
                print(str(count) + " " + i.name + " 总投入:" + str(i.put) + "元 当前持有:" + str(i.last) + "元")
                count += 1

    @staticmethod
    def select_fund():
        global selected_fund_code
        if selected_fund_code != "":
            print("当前选择的基金是 " + SourceTool.get_fund_name(selected_fund_code))

        print("请从已添加的基金列表中选择操作基金")
        try:
            Command.list_fund()
        except:
            return
        selected_fund_code = Funds[int(input("请输入基金序号(非基金代码)"))].code
        print("选择基金 "+SourceTool.get_fund_name(selected_fund_code)+" 成功")

    @staticmethod
    def buy_fund():
        pass


def cmd(command: str):
    if command == 'h' or command == 'help':
        print("有如下命令：添加基金，列出添加的基金，买入基金，卖出基金，选择基金")
    elif command == '列出添加的基金':
        Command.list_fund()
    elif command == '添加基金':
        Command.add_fund()
    elif command == '选择基金':
        Command.select_fund()
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
            cmd(input())
        except:
            pass
