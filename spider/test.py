import requests

url = 'http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code=005267&topline=50&year=2020'

r = requests.get(url)
r.encoding = 'utf-8'
print(r.text)
