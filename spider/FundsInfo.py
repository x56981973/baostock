from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


class FundsInfo:
    fund_list = []

    def __init__(self, url):
        html_doc = ""

        with open(url, encoding='UTF-8') as file:
            for i in file.readlines():
                html_doc += i

        soup = BeautifulSoup(html_doc, 'html.parser')

        body = soup.body

        table = body.find('table', id='dbtable')
        t_body = table.tbody

        for fund in t_body.find_all("tr"):
            fund_dict = {}
            item_list = fund.find_all("td")

            fund_dict['基金代码'] = item_list[2].string
            fund_dict['URL'] = item_list[2].a['href']
            fund_dict['基金名称'] = item_list[3].a['title']
            fund_dict['日期'] = item_list[4].string
            fund_dict['单位净值'] = self.to_float(item_list[5].string)
            fund_dict['累计净值'] = self.to_float(item_list[6].string)
            fund_dict['日增长率'] = self.to_float(item_list[7].string)
            fund_dict['近1周'] = self.to_float(item_list[8].string)
            fund_dict['近1月'] = self.to_float(item_list[9].string)
            fund_dict['近3月'] = self.to_float(item_list[10].string)
            fund_dict['近6月'] = self.to_float(item_list[11].string)
            fund_dict['近1年'] = self.to_float(item_list[12].string)
            fund_dict['近2年'] = self.to_float(item_list[13].string)
            fund_dict['近3年'] = self.to_float(item_list[14].string)
            fund_dict['今年来'] = self.to_float(item_list[15].string)
            fund_dict['成立来'] = self.to_float(item_list[16].string)

            self.fund_list.append(fund_dict)

    def save_to_csv(self, path):
        df = pd.DataFrame(self.fund_list)
        df.to_csv(path, encoding='UTF-8', index=False,
                  columns=['基金代码', 'URL', '基金名称', '日期', '单位净值', '累计净值', '日增长率', '近1周', '近1月', '近3月', '近6月', '近1年',
                           '近2年', '近3年', '今年来', '成立来'])

    @staticmethod
    def to_float(string):
        if string[-1] == '%':
            return float(string[:-1])
        elif string == '---':
            return np.NaN
        else:
            return float(string)


if __name__ == '__main__':
    funds = FundsInfo("C:\\Users\\Administrator.DESKTOP-IAI6IQ1\\Desktop\\开放式基金排行 _ 天天基金网.html")
    funds.save_to_csv("../data/fund_list.csv")
