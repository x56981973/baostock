from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


class FundsDetails:
    def __init__(self, url, fund_code, fund_name):
        html_doc = ''
        with open(url, encoding='UTF-8') as file:
            for i in file.readlines():
                html_doc += i
        fund_dict = {'基金代码': fund_code, '基金名称': fund_name}
        soup = BeautifulSoup(html_doc, 'html.parser')

        body = soup.body

        info_of_fund = body.find(name='div', attrs={'class': 'infoOfFund'})
        for i in info_of_fund.find_all('td'):
            if i.text[:4] == '基金类型':
                fund_dict['基金类型'] = i.a.string
            elif i.text[:4] == '基金规模':
                fund_dict['基金规模'] = i.a.string
            elif i.text[:4] == '基金经理':
                fund_dict['基金经理'] = i.a.string
            elif i.text[:5] == '成 立 日':
                fund_dict['成立日'] = i.text[6:]
            elif i.text[:5] == '管 理 人':
                fund_dict['管理人'] = i.a.string

        position_shares = body.find(name='li', id='position_shares')
        count = 1
        for i in position_shares.find_all('tr')[1:]:
            j = i.find_all('td')
            a = j[0].a
            if a is not None:
                href = a['href']
                stock_code = href.split('/')[-1].split('.')[0]
                self.fund_dict['stock_code' + str(count)] = stock_code
            else:
                self.fund_dict['stock_code' + str(count)] = j[0].div['title']

            self.fund_dict['stock_shares' + str(count)] = j[1].string

            count += 1

        sum_num = position_shares.find(name='span', attrs={'class': 'end_date'}).string
        self.fund_dict['fund' + str(count)] = j[1].string


if __name__ == '__main__':
    funds = FundsDetails("C:\\Users\\Administrator.DESKTOP-IAI6IQ1\\Desktop\\162411.html", "162411", "华宝标普油气上游股票人民币A")
    print(funds.fund_dict)
