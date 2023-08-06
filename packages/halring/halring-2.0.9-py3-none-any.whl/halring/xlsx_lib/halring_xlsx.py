# -*- coding:UTF-8 -*-
"""
pip install pandas
"""
import pandas as pd


class XlsxUtil(object):
    def __init__(self, xlsxPath=None):
        self.basePath = xlsxPath
        self.df = None

    def getWbBook(self, sheet=None, header=None):
        """

        :param sheet:
        :param header: 源码里header默认是0,如果文件存在header不用传此参数,
        若文件无header,传None即可
        :return:
        """

        if sheet is not None and header is not None:
            self.df = pd.read_excel(self.basePath,keep_default_na=False, dtype=object, sheet_name=sheet, header=header)
        elif sheet is not None and header is None:
            self.df = pd.read_excel(self.basePath,keep_default_na=False, dtype=object, sheet_name=sheet)
        elif sheet is None and header is None:
            self.df = pd.read_excel(self.basePath,keep_default_na=False,dtype=object)
        elif sheet is None and header is not None:
            self.df = pd.read_excel(self.basePath,keep_default_na=False,dtype=object,  header=header)
        else:
            self.df = pd.read_excel(self.basePath,keep_default_na=False,dtype=object)
        return self.df

    def readHead(self):
        """
        读取标题行
        :return:
        """
        heads = []
        data = self.df.columns.values
        return data

    def readRow(self, rowNum):
        """
        读取某一行
        :param rowNum:
        :return:
        """
        data = self.df.iloc[rowNum].values

        return data

    def read_to_dict(self):
        """
        读取所有xlsx数据至dict
        :return: List<dict>
        """
        data = []
        for i in self.df.index.values:
            #     获取行号的索引,对其进行遍历
            row_data = self.df.loc[i, self.readHead()].to_dict()
            data.append(row_data)

        return data


if __name__ == '__main__':
    xlsxPath = "D:\\2020交易网关\\TDGW配置模板.xls"
    # 初始化对象
    excel_util = XlsxUtil(xlsxPath)
    # 初始化workbook对象
    excel_util.getWbBook(0)
    # 读取数据至dict
    data = excel_util.read_to_dict()
    print(data)

    for map in data:
        print(map['操作系统'])
