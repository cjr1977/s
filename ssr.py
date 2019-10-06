#!/usr/bin/env python3
import cfscrape
import bs4
from prettytable import PrettyTable
from ping3 import verbose_ping,ping
import os
import operator
import requests
import numpy
import json

def ping_test(ip):
    delay = []
    delay.append(ping(ip,unit="ms"))
    delay.append(ping(ip,unit="ms"))
    delay.append(ping(ip,unit="ms"))
    delay = [x for x in delay if x != None]
    if len(delay) ==0:
        return "timeout"
    else:
        return int(numpy.mean(delay))

scraper = cfscrape.create_scraper()
soup = bs4.BeautifulSoup(scraper.get("https://www.youneed.win/free-ssr").content)
content =  soup.tbody.get_text().strip("\n\n")
sslist = content.split("\n\n")

tableList = []
for text in sslist:
    text = text.strip("\n")
    tlist = text.split("\n")
    tlist.insert(0, ping_test(tlist[0]))
    tableList.append(tlist)

i = 0
table = PrettyTable(["seq","TimeDelay","ssr","ip","port","password","encryption","origin","plain",])
tableList.sort(key=operator.itemgetter(0))

for row in tableList:
    row[0] = str(row[0]) + "ms"
    row.insert(0,i)
    table.add_row(row)
    i+=1
print(table)

print("请输入要添加的ss的序号:")
ssseq = int(input())
d = {
    "ServerHost":tableList[ssseq][2],
    "ServerPort":tableList[ssseq][3],
    "Password":tableList[ssseq][4],
    "Method":tableList[ssseq][5],
    "Remark":tableList[ssseq][7],
    "PluginOptions":"",
    "Plugin":"",
}

j = json.dumps(d)
print(j)

